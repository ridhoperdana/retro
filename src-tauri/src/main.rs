#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::{
    env,
    net::{TcpStream, ToSocketAddrs, SocketAddr, Ipv4Addr},
    process::{Child, Command, Stdio},
    path::PathBuf,
    sync::Mutex,
};

use tauri::{Manager, RunEvent, State};

struct PythonServer(Mutex<Option<Child>>);

struct ServerConfig {
    host: String,
    port: u16,
    target_url: String,
}

#[tauri::command]
fn get_backend_url(cfg: State<'_, ServerConfig>) -> String {
    cfg.target_url.clone()
}

#[tauri::command]
fn check_backend_ready(cfg: State<'_, ServerConfig>) -> bool {
    // Resolve address using ToSocketAddrs to handle hostnames and IPs
    let addr_str = format!("{}:{}", cfg.host, cfg.port);
    
    // Try to resolve the address
    let socket_addrs: Vec<SocketAddr> = match addr_str.to_socket_addrs() {
        Ok(addrs) => addrs.collect(),
        Err(_) => {
            // If resolution fails, fall back to loopback
            vec![SocketAddr::new(
                std::net::IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)),
                cfg.port
            )]
        }
    };

    // Filter out unspecified addresses (0.0.0.0, ::) and find a reachable address
    let mut reachable_addr: Option<SocketAddr> = None;
    
    for addr in socket_addrs {
        // Skip unspecified addresses
        match addr {
            SocketAddr::V4(v4) => {
                if v4.ip().is_unspecified() {
                    continue;
                }
            }
            SocketAddr::V6(v6) => {
                if v6.ip().is_unspecified() {
                    continue;
                }
            }
        }
        
        // Try to connect to this address
        if TcpStream::connect_timeout(&addr, std::time::Duration::from_millis(500)).is_ok() {
            reachable_addr = Some(addr);
            break;
        }
    }

    // If no reachable address found, fall back to loopback
    let target_addr = reachable_addr.unwrap_or_else(|| {
        SocketAddr::new(
            std::net::IpAddr::V4(Ipv4Addr::new(127, 0, 0, 1)),
            cfg.port
        )
    });

    // Verify TCP connection
    if TcpStream::connect_timeout(&target_addr, std::time::Duration::from_millis(500)).is_err() {
        return false;
    }

    // Verify HTTP server is responding
    let health_url = format!("{}health", cfg.target_url);
    match ureq::get(&health_url).timeout(std::time::Duration::from_secs(2)).call() {
        Ok(resp) => resp.status() == 200,
        Err(_) => false,
    }
}

impl PythonServer {
    fn start(&self, python_cmd: &str, host: &str, port: u16) -> tauri::Result<()> {
        let mut process = self.0.lock().expect("mutex poisoned");
        if process.is_some() {
            return Ok(());
        }

        let project_root = env::var("RETRO_TAURI_PROJECT_ROOT")
            .ok()
            .map(PathBuf::from)
            .or_else(|| {
                env::current_dir()
                    .ok()
                    .and_then(|cwd| cwd.parent().map(|p| p.to_path_buf()))
            });

        let mut cmd = Command::new(python_cmd);

        // Try direct script path first, then fall back to module
        let mut used_script_path = false;
        if let Some(root) = project_root.as_ref() {
            let script_path = root.join("retro").join("web_gui.py");
            if script_path.exists() {
                cmd.arg(script_path);
                used_script_path = true;
            }
        }

        if !used_script_path {
            cmd.args(["-m", "retro.web_gui"]);
        }

        cmd.args(["--host", host, "--port", &port.to_string(), "--no-browser"])
            .env("RETRO_GUI_NO_BROWSER", "1");

        if let Some(root) = project_root {
            cmd.current_dir(&root);
            let existing = env::var("PYTHONPATH").unwrap_or_default();
            let root_str = root.to_string_lossy();
            let sep = if cfg!(windows) { ";" } else { ":" };
            let merged = if existing.is_empty() {
                root_str.to_string()
            } else {
                format!("{}{}{}", root_str, sep, existing)
            };
            cmd.env("PYTHONPATH", merged);
        }

        if cfg!(debug_assertions) {
            cmd.stdout(Stdio::inherit()).stderr(Stdio::inherit());
        } else {
            cmd.stdout(Stdio::null()).stderr(Stdio::null());
        }

        let child = cmd.spawn()?;
        *process = Some(child);
        Ok(())
    }

    fn shutdown(&self) {
        if let Some(mut child) = self.0.lock().expect("mutex poisoned").take() {
            let _ = child.kill();
            let _ = child.wait();
        }
    }
}

fn main() {
    let host = env::var("RETRO_TAURI_HOST").unwrap_or_else(|_| "127.0.0.1".to_string());
    let port: u16 = env::var("RETRO_TAURI_PORT")
        .ok()
        .and_then(|value| value.parse().ok())
        .unwrap_or(5000);
    let python_cmd = env::var("RETRO_TAURI_PYTHON").unwrap_or_else(|_| "python3".to_string());
    let target_url = format!("http://{host}:{port}/");

    let server_config = ServerConfig {
        host: host.clone(),
        port,
        target_url: target_url.clone(),
    };

    let setup_python = python_cmd;
    let setup_host = host;

    tauri::Builder::default()
        .manage(PythonServer(Mutex::new(None)))
        .manage(server_config)
        .invoke_handler(tauri::generate_handler![
            get_backend_url,
            check_backend_ready
        ])
        .setup(move |app| {
            let state = app.state::<PythonServer>();
            state.start(&setup_python, &setup_host, port)
                .map_err(|e| Box::new(e) as Box<dyn std::error::Error>)
        })
        .build(tauri::generate_context!())
        .expect("error while running tauri application")
        .run(|app_handle, event| {
            if let RunEvent::ExitRequested { .. } | RunEvent::Exit = event {
                let state = app_handle.state::<PythonServer>();
                state.shutdown();
            }
        });
}
