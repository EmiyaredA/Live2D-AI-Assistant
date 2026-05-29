#!/usr/bin/env python3
"""Link bundled Live2D models from a local Open-LLM-VTuber checkout."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OLV = ROOT.parent / "Open-LLM-VTuber"
TARGET_DIR = ROOT / "live2d-models"
MODEL_NAMES = ("mao_pro", "shizuku")


def link_models(source_root: Path, force: bool) -> int:
    source_models = source_root / "live2d-models"
    if not source_models.is_dir():
        print(f"错误：未找到目录 {source_models}", file=sys.stderr)
        return 1

    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    linked = 0

    for name in MODEL_NAMES:
        src = source_models / name
        dst = TARGET_DIR / name

        if not src.is_dir():
            print(f"跳过：{name} 在源目录中不存在")
            continue

        if dst.exists() or dst.is_symlink():
            if force:
                if dst.is_symlink() or dst.is_file():
                    dst.unlink()
                elif dst.is_dir() and not dst.is_symlink():
                    print(f"跳过：{dst} 已是真实目录，请手动删除后重试")
                    continue
            else:
                print(f"已存在：{dst}")
                continue

        os.symlink(src, dst, target_is_directory=True)
        print(f"已链接：{dst} -> {src}")
        linked += 1

    if linked == 0:
        print("没有新建链接。若需覆盖已有链接，请加 --force")
    else:
        print(f"\n完成，共链接 {linked} 个模型。重启 dev.py 后会在数据库中自动注册。")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_OLV,
        help=f"Open-LLM-VTuber 仓库路径（默认 {DEFAULT_OLV}）",
    )
    parser.add_argument("--force", action="store_true", help="覆盖已有符号链接")
    args = parser.parse_args()
    return link_models(args.source.resolve(), args.force)


if __name__ == "__main__":
    raise SystemExit(main())
