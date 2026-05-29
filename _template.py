"""
dev.py 参考模板（不参与运行）。

职责：一键启动后端与前端开发服务，可选进程监督与热重载。
复制要点到 dev.py 后按本机路径调整。
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_PORT = 8000
FRONTEND_PORT = 5173


def start_backend() -> subprocess.Popen:
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "backend.app:app",
            "--host",
            "0.0.0.0",
            "--port",
            str(BACKEND_PORT),
            "--reload",
        ],
        cwd=ROOT,
    )


def start_frontend() -> subprocess.Popen:
    return subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", str(FRONTEND_PORT)],
        cwd=ROOT / "frontend",
    )


def main() -> None:
    procs = [start_backend(), start_frontend()]
    try:
        for proc in procs:
            proc.wait()
    except KeyboardInterrupt:
        for proc in procs:
            proc.terminate()


if __name__ == "__main__":
    main()
