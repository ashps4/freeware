#!/usr/bin/env python3
import argparse, json, re, urllib.request
from pathlib import Path

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "PS4-Ghidra-AIO"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--tag", required=True)
    p.add_argument("--match", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    release = get_json(f"https://api.github.com/repos/{a.repo}/releases/tags/{a.tag}")
    rx = re.compile(a.match, re.I)
    assets = [x for x in release.get("assets", []) if rx.search(x.get("name", ""))]
    if len(assets) != 1:
        raise SystemExit("Expected one matching release asset. Available: " +
                         ", ".join(x.get("name", "") for x in release.get("assets", [])))
    req = urllib.request.Request(assets[0]["browser_download_url"],
                                 headers={"User-Agent": "PS4-Ghidra-AIO"})
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=180) as r, out.open("wb") as f:
        f.write(r.read())
    print("Downloaded:", assets[0]["name"], "->", out)

if __name__ == "__main__":
    main()
