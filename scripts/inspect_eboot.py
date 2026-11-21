#!/usr/bin/env python3
"""Report eboot.bin signature/container clues without attempting decryption."""
import hashlib
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: inspect_eboot.py <eboot.bin>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        first = stream.read(64)
        digest.update(first)
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)

    print(f"File: {path}")
    print(f"Size: {path.stat().st_size} bytes")
    print(f"SHA-256: {digest.hexdigest()}")
    print(f"First 64 bytes: {first.hex(' ')}")

    if first.startswith(b"\x7fELF"):
        print("Detection: ELF magic at offset 0; this is a directly readable ELF container.")
        print("Note: ELF magic alone does not validate every segment or relocation.")
    elif first.startswith(b"SCE\x00"):
        print("Detection: SCE/SELF-style container header.")
        if len(first) >= 16:
            program_type = first[8:16]
            print(f"Program type bytes at offset 0x08: {program_type.hex(' ')}")
            if first[8] == 0x01 and first[9] == 0x01:
                print("Hint: type bytes are consistent with the fSELF marker used by homebrew toolchains.")
                print("This is a format clue, not cryptographic proof that every segment is plaintext.")
            elif first[8] == 0x01 and (first[9] & 0x0F) == 0x04:
                print("Hint: type bytes are consistent with an NPDRM SELF used for retail game executables.")
                print("Do not assume the executable payload is plaintext just because the file was extracted.")
            else:
                print("Hint: SELF subtype is not classified by this small inspection script.")
        else:
            print("The header is too short to inspect the program-type field.")
    else:
        print("Detection: unknown header. The file is neither a plain ELF nor a recognized SCE header by this check.")

    print("Important: downloading, extracting, or placing the file in a runner does not decrypt it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
