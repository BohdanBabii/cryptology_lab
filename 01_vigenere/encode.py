import argparse
from pathlib import Path

VOCAB = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
TABLE = dict(zip(VOCAB, range(26)))


def read_file(input_path: Path) -> str:
    with open(input_path, encoding="utf-8") as f:
        return f.read()


def write_file(output_path: Path, code: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)


def encode(input_file: str, key: str) -> str:
    _vaildate_key(key)
    key = key.upper()
    code = []
    pos = 0
    for char in input_file.upper():
        if char in TABLE:
            shift = TABLE[key[pos % len(key)]]
            char_code = VOCAB[(TABLE[char] + shift) % 26]
            code.append(char_code)
            pos += 1
        else:
            code.append(char)
    return "".join(code)


def _vaildate_key(key: str):
    if not (key.isalpha() and key.isascii()):
        raise ValueError("Key has to consists of uppercase letters A-Z.")


def main(input: str, key: str, output: str):
    file = read_file(input_path=Path(input))
    code = encode(input_file=file, key=key)
    write_file(output_path=Path(output), code=code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vigenère encoder")
    parser.add_argument("--input-path", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--output-path", required=True)
    args = parser.parse_args()
    main(args.input_path, args.key, args.output_path)
