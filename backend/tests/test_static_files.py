from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient


def test_staticfiles_follow_symlink(tmp_path: Path):
  target = tmp_path / "target"
  target.mkdir()
  (target / "hello.txt").write_text("ok")

  root = tmp_path / "root"
  root.mkdir()
  os.symlink(target, root / "linked")

  app = FastAPI()
  app.mount("/assets", StaticFiles(directory=str(root), follow_symlink=True), name="assets")

  client = TestClient(app)
  blocked = StaticFiles(directory=str(root), follow_symlink=False)
  blocked_app = FastAPI()
  blocked_app.mount("/assets", blocked, name="assets")
  blocked_client = TestClient(blocked_app)

  assert client.get("/assets/linked/hello.txt").status_code == 200
  assert blocked_client.get("/assets/linked/hello.txt").status_code == 404
