from __future__ import annotations

import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRONTEND_PORT = 5173


def _port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def _find_pids_on_port(port: int) -> list[int]:
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return []
        return [int(pid) for pid in result.stdout.strip().splitlines() if pid.strip()]
    except (FileNotFoundError, ValueError):
        return []


def _load_backend_port() -> int:
    from backend.core.settings import get_settings

    return get_settings().assistant_port


def _ensure_port_available(port: int) -> None:
    if not _port_in_use(port):
        return

    pids = _find_pids_on_port(port)
    pid_hint = f" (PID: {', '.join(map(str, pids))})" if pids else ""
    print(
        f"\n错误：端口 {port} 已被占用{pid_hint}。\n"
        f"可先结束占用进程，例如：\n"
        f"  lsof -ti :{port} | xargs kill\n"
        f"或在 .env 中改用其他端口：\n"
        f"  ASSISTANT_PORT=8001\n",
        file=sys.stderr,
    )
    sys.exit(1)


def start_backend(port: int) -> subprocess.Popen:
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.app:app",
            "--host",
            "0.0.0.0",
            "--port",
            str(port),
            "--reload",
        ],
        cwd=ROOT,
    )


def start_frontend(port: int) -> subprocess.Popen | None:
    frontend_dir = ROOT / "frontend"
    if not (frontend_dir / "package.json").exists():
        return None

    env = {**subprocess.os.environ, "ASSISTANT_PORT": str(port)}
    return subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", str(FRONTEND_PORT)],
        cwd=frontend_dir,
        env=env,
    )


def main() -> None:
    backend_port = _load_backend_port()
    _ensure_port_available(backend_port)

    if _port_in_use(FRONTEND_PORT):
        pids = _find_pids_on_port(FRONTEND_PORT)
        pid_hint = f" (PID: {', '.join(map(str, pids))})" if pids else ""
        print(
            f"\n错误：前端端口 {FRONTEND_PORT} 已被占用{pid_hint}。\n"
            f"可先结束占用进程，例如：\n"
            f"  lsof -ti :{FRONTEND_PORT} | xargs kill\n",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Starting backend on http://localhost:{backend_port}")
    print(f"Starting frontend on http://localhost:{FRONTEND_PORT}")

    procs: list[subprocess.Popen] = [start_backend(backend_port)]
    frontend_proc = start_frontend(backend_port)
    if frontend_proc:
        procs.append(frontend_proc)
    else:
        print("frontend/package.json not found — starting backend only")

    try:
        for proc in procs:
            proc.wait()
    except KeyboardInterrupt:
        for proc in procs:
            proc.terminate()


if __name__ == "__main__":
    main()
