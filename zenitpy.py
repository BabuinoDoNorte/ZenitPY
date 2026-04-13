#!/usr/bin/env python3
import sys
import argparse

def build_translation_table(key_string):
    table = {}
    parts = [p.strip() for p in key_string.upper().split("-")]
    for part in parts:
        if len(part) != 2:
            raise ValueError(f"Invalid pair: '{part}'. Each segment must have exactly 2 letters.")
        a, b = part[0], part[1]
        if not (a.isalpha() and b.isalpha()):
            raise ValueError(f"Pair '{part}' contains a non-alphabetic character.")
        if a == b:
            continue
        table[a] = b
        table[b] = a
    return table

def build_default_table():
    return build_translation_table("ZP-EO-NL-IA-TR")

def apply_cipher(text, table):
    result = []
    for char in text:
        upper = char.upper()
        if upper in table:
            substitute = table[upper]
            result.append(substitute.lower() if char.islower() else substitute)
        else:
            result.append(char)
    return "".join(result)

def parse_args():
    parser = argparse.ArgumentParser(
        prog="zenitpy",
        description=(
            "╔══════════════════════════════════════╗\n"
            "║  ZENIT POLAR — Substitution Cipher   ║\n"
            "╚══════════════════════════════════════╝\n\n"
            "Encrypts and decrypts text using symmetric substitution.\n"
            "Applying the cipher twice returns the original text.\n"
            "ZERO LOGS: no data is ever saved to disk."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  zenitpy --text 'Hello World'\n"
            "  echo 'Secret' | zenitpy\n"
            "  zenitpy --key 'HF-AE-CS-KT' --text 'Hello'\n"
            "  zenitpy --text 'TENIS'   # -> ROTAS\n"
            "  zenitpy --text 'ROTAS'   # -> TENIS\n"
        ),
    )
    parser.add_argument("--text", "-t", metavar="TEXT", help="Text to process.")
    parser.add_argument("--key", "-k", metavar="KEY", default=None, help="Custom key in format 'AB-CD-EF'. Default: ZENIT POLAR (ZP-EO-NL-IA-TR).")
    parser.add_argument("--show-table", action="store_true", help="Display active substitution table and exit.")
    parser.add_argument("--version", "-v", action="version", version="zenitpy 1.0.0")
    return parser.parse_args()

def display_table(table, key_name):
    print(f"\nActive substitution table: {key_name}")
    print("─" * 32)
    seen = set()
    for a, b in table.items():
        if a not in seen and b not in seen:
            print(f"  {a}  ↔  {b}")
            seen.add(a)
            seen.add(b)
    print("─" * 32)
    print("Unlisted letters remain unchanged.\n")

def main():
    args = parse_args()
    if args.key:
        try:
            table = build_translation_table(args.key)
            key_name = f"custom ({args.key.upper()})"
        except ValueError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)
    else:
        table = build_default_table()
        key_name = "ZENIT POLAR (default)"

    if args.show_table:
        display_table(table, key_name)
        sys.exit(0)

    if args.text is not None:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read().rstrip("\n")
    else:
        print("[ERROR] Provide text via --text 'TEXT' or via stdin.\n        Use --help for examples.", file=sys.stderr)
        sys.exit(1)

    print(apply_cipher(text, table))

if __name__ == "__main__":
    main()
