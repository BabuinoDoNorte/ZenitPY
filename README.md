# zenitpolar
╔══════════════════════════════════════╗
║  ZENIT POLAR — Substitution Cipher   ║
╚══════════════════════════════════════╝

A minimalist Linux CLI tool for substitution-based encryption.  
Runs entirely in memory. **ZERO LOGS** — no data is ever written to disk.

---

## Table of Contents

- [How it works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Flag reference](#flag-reference)
- [Custom key](#custom-key)
- [Advanced examples](#advanced-examples)
- [Security & privacy](#security--privacy)

---

## How it works

The **ZENIT POLAR** algorithm is a symmetric substitution cipher. Each mapped letter is swapped with its counterpart — and because the mapping is bidirectional, the **same operation that encrypts also decrypts**.

Default substitution table:

| Original | ↔ | Substitute |
|:--------:|:-:|:----------:|
| Z        | ↔ | P          |
| E        | ↔ | O          |
| N        | ↔ | L          |
| I        | ↔ | A          |
| T        | ↔ | R          |

Letters not listed in the table pass through unchanged. The original casing is always preserved in the output.

**Example:**
TENIS  →  ROLAS
ROLAS  →  TENIS

---

## Installation

**Requirements:** Python 3.6+ (no external dependencies).

```bash
git clone https://github.com/BabuinoDoNorte/ZenitPY.git
cd ZenitPY
chmod +x install.sh
./install.sh
```

> After install, the `zenitpolar` command is available system-wide.

---

## Usage
zenitpolar [--text TEXT] [--key KEY] [--show-table] [--version] [--help]

**1. Direct argument:**
```bash
zenitpolar --text "Hello World"
```

**2. Via stdin (pipe):**
```bash
echo "Hello World" | zenitpolar
```

---

## Flag reference

| Flag           | Short | Description                                           |
|----------------|-------|-------------------------------------------------------|
| `--text TEXT`  | `-t`  | Text to be processed.                                 |
| `--key KEY`    | `-k`  | Custom key in the format `AB-CD-EF`.                  |
| `--show-table` | —     | Display the active substitution table and exit.       |
| `--version`    | `-v`  | Show the program version.                             |
| `--help`       | `-h`  | Show help message.                                    |

---

## Custom key

```bash
zenitpolar --key "HF-AE-CS-KT" --text "HACK"
# → FEST

zenitpolar --key "HF-AE-CS-KT" --text "FEST"
# → HACK
```

Each pair defines a bidirectional swap. Key rules:
- Each segment must have exactly **2 letters**
- Only **alphabetic** characters accepted
- Case-insensitive (`ab-cd` equals `AB-CD`)

---

## Advanced examples

```bash
zenitpolar --text "MACACO"               # → MICICE
zenitpolar --text "MICICE"               # → MACACO
echo "Secret" | zenitpolar              # via pipe
cat input.txt | zenitpolar > out.txt    # process file
zenitpolar --text "MACACO" | zenitpolar  # → MACACO (double apply)
zenitpolar --show-table                 # view default table
zenitpolar --key "AB-CD-EF" --show-table
```

---

## Security & privacy

| Property            | Detail                                                        |
|---------------------|---------------------------------------------------------------|
| **ZERO LOGS**       | No file is created or modified on disk during execution.      |
| **Memory only**     | All processing occurs in local-scope variables in RAM.        |
| **Clean stdout**    | Results to `stdout`, errors to `stderr`.                      |
| **No network**      | No network connections are made.                              |
| **No dependencies** | Python 3 standard library only (`sys`, `argparse`).           |

> **Notice:** ZENIT POLAR is a substitution cipher suitable for basic obfuscation. Do not use as the sole mechanism in environments requiring strong cryptography.

---

## License

MIT — free to use, modify, and distribute.
