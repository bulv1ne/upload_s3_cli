import argparse
import json
from pathlib import Path

import requests
from tqdm import tqdm


def read_config(path):
    with open(path, "r") as f:
        return json.load(f)


def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)


def main():
    parser = argparse.ArgumentParser("upload_s3_cli.upload_files")
    parser.add_argument("--config", type=read_config, required=True)
    parser.add_argument("file_paths", type=Path, nargs="+")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path_stack: list[Path] = []
    for path in args.file_paths:
        if path.is_dir():
            path_stack.extend(p for p in path.rglob("*") if p.is_file())
        else:
            path_stack.append(path)
    total_size = sum(path.stat().st_size for path in path_stack)

    print(f"Uploading {len(path_stack)} files, totalling {sizeof_fmt(total_size)}")
    for path in path_stack:
        print(path)

    if args.dry_run:
        return

    for path in tqdm(path_stack):
        with path.open("rb") as f:
            r = requests.post(
                args.config["url"], data=args.config["fields"], files={"file": f}
            )
            if 400 <= r.status_code:
                print(r.text)
                r.raise_for_status()


if __name__ == "__main__":
    main()
