import sys
import argparse

def build_translation_table(key_string: str) -> dict:
    """
    Recebe uma string no formato "ABC-DEF" ou "ABCDEF" e constrói um
    dicionário de substituição bidirecional (simétrico).

    Regras de parsing da chave:
      - Pares são separados por "-" (hífen).
      - Cada par deve ter exatamente 2 letras.
      - A substituição é case-insensitive, mas o case original é preservado
        na saída (tratado em apply_cipher).

    Exemplo: "ZENIT-POLAR" → Z↔P, E↔O, N↔L, I↔A, T↔R

    A simetria é garantida porque para cada par (A, B) adicionamos
    tanto A→B quanto B→A na tabela. Aplicar a cifra duas vezes
    retorna o texto original.
    """
    table = {}
    parts = [p.strip() for p in key_string.upper().split("-")]

    for part in parts:
        if len(part) != 2:
            raise ValueError(
                f"Par de substituição inválido: '{part}'. "
                "Cada segmento entre hífens deve ter exatamente 2 letras. "
                "Exemplo correto: --key 'AB-CD-EF'"
            )
        a, b = part[0], part[1]
        if not (a.isalpha() and b.isalpha()):
            raise ValueError(
                f"Par '{part}' contém caractere não-alfabético. "
                "Apenas letras são permitidas na chave."
            )
        if a == b:
            continue
        table[a] = b
        table[b] = a

    return table


def build_default_table() -> dict:
    """
    Constrói a tabela padrão ZENIT POLAR:
      Z↔P  E↔O  N↔L  I↔A  T↔R
    """
    return build_translation_table("ZP-EO-NL-IA-TR")

def apply_cipher(text: str, table: dict) -> str:
    """
    Percorre o texto caractere a caractere. Para cada letra:
      1. Converte para uppercase para consultar a tabela.
      2. Se encontrar substituto, aplica-o mantendo o case original.
      3. Se não encontrar, mantém o caractere inalterado.

    Caracteres não-alfabéticos (espaços, pontuação, números) passam
    sem modificação.

    A simetria é intrínseca: como a tabela é bidirecional (A→B e B→A),
    cifrar o texto cifrado retorna o original.
    """
    result = []
    for char in text:
        upper = char.upper()
        if upper in table:
            substituto = table[upper]
            if char.islower():
                result.append(substituto.lower())
            else:
                result.append(substituto)
        else:
            result.append(char)
    return "".join(result)

def parse_args():
    parser = argparse.ArgumentParser(
        prog="zenitpolar",
        description=(
            "╔══════════════════════════════════════╗\n"
            "║  ZENIT POLAR — Cifra de Substituição ║\n"
            "╚══════════════════════════════════════╝\n\n"
            "Encripta e decripta texto usando substituição simétrica.\n"
            "Aplicar a cifra duas vezes retorna o texto original.\n"
            "ZERO LOGS: nenhum dado é salvo em disco."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "exemplos de uso:\n"
            "  zenitpolar --text 'Ola Mundo'\n"
            "  echo 'Segredo' | zenitpolar\n"
            "  zenitpolar --key 'HACK-FEST' --text 'Ola Mundo'\n"
            "  zenitpolar --text 'TENIS'   # → ROTAS\n"
            "  zenitpolar --text 'ROTAS'   # → TENIS\n\n"
            "formato da chave customizada:\n"
            "  Pares de letras separados por hífen: 'AB-CD-EF'\n"
            "  Cada par define uma troca bidirecional (A↔B, C↔D, F↔E).\n"
        ),
    )

    parser.add_argument(
        "--text", "-t",
        metavar="TEXTO",
        help="Texto a ser processado (alternativa ao stdin).",
    )

    parser.add_argument(
        "--key", "-k",
        metavar="CHAVE",
        default=None,
        help=(
            "Chave de substituição customizada no formato 'AB-CD-EF'.\n"
            "Se omitida, usa o padrão ZENIT POLAR (ZP-EO-NL-IA-TR)."
        ),
    )

    parser.add_argument(
        "--show-table",
        action="store_true",
        help="Exibe a tabela de substituição ativa e encerra.",
    )

    parser.add_argument(
        "--version", "-v",
        action="version",
        version="zenitpolar 1.0.0",
    )

    return parser.parse_args()

def display_table(table: dict, key_name: str):
    """Imprime a tabela de substituição de forma legível no stdout."""
    print(f"\nTabela de substituição ativa: {key_name}")
    print("─" * 30)
    seen = set()
    for a, b in table.items():
        if a not in seen and b not in seen:
            print(f"  {a}  ↔  {b}")
            seen.add(a)
            seen.add(b)
    print("─" * 30)
    print("Letras não listadas permanecem inalteradas.\n")

def main():
    args = parse_args()

    if args.key:
        try:
            table = build_translation_table(args.key)
            key_name = f"customizada ({args.key.upper()})"
        except ValueError as e:
            print(f"[ERRO] {e}", file=sys.stderr)
            sys.exit(1)
    else:
        table = build_default_table()
        key_name = "ZENIT POLAR (padrão)"
    if args.show_table:
        display_table(table, key_name)
        sys.exit(0)
    if args.text is not None:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read().rstrip("\n")
    else:
        print(
            "[ERRO] Forneça o texto via --text 'TEXTO' ou via stdin (pipe).\n"
            "       Use --help para ver exemplos de uso.",
            file=sys.stderr,
        )
        sys.exit(1)
    resultado = apply_cipher(text, table)
    print(resultado)


if __name__ == "__main__":
    main()
