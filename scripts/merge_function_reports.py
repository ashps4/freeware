#!/usr/bin/env python3
import argparse, csv, html
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--reports", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--html", required=True)
    a = p.parse_args()
    files = sorted(Path(a.reports).glob("*.functions.csv"))
    rows, headers = [], None
    for file in files:
        with file.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            headers = headers or reader.fieldnames
            rows.extend(reader)
    headers = headers or ["program","name","entry_address","body_min","body_max","size","thunk","external"]
    out = Path(a.output); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers); writer.writeheader(); writer.writerows(rows)
    head = "<tr>" + "".join("<th>"+html.escape(x)+"</th>" for x in headers) + "</tr>"
    body = "".join("<tr>" + "".join("<td>"+html.escape(str(r.get(h,"")))+"</td>" for h in headers) + "</tr>" for r in rows)
    page = ("<!doctype html><html><head><meta charset='utf-8'><title>Ghidra report</title>"
            "<style>body{font:14px system-ui;margin:2rem}table{border-collapse:collapse}"
            "th,td{border:1px solid #bbb;padding:.35rem .6rem;text-align:left}</style></head><body>"
            "<h1>PS4 Ghidra function report</h1><p>Function rows: "+str(len(rows))+"</p>"
            "<table><thead>"+head+"</thead><tbody>"+body+"</tbody></table></body></html>")
    Path(a.html).write_text(page, encoding="utf-8")
    print("Exported", len(rows), "function rows")

if __name__ == "__main__":
    main()
