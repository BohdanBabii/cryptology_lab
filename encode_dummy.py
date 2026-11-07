import argparse
from pathlib import Path

def read_file(input_path: Path) -> str:
    with open(input_path, encoding="utf-8") as f:
        return f.read()

def write_file(output_path: Path, code: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)

def encode(input_file: str, key: str) -> str:
    print(f"key: {key}")
    return input_file

def main(input: str, key: str, output: str):
    file = read_file(input_path=Path(input))
    code = encode(input_file=file, key=key)
    write_file(output_path=Path(output), code=code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vigenere encoder")
    parser.add_argument("--input-path", required=True)
    parser.add_argument("--key", required=True)
    parser.add_argument("--output-path", required=True)
    args = parser.parse_args()
    main(args.input_path, args.key, args.output_path)
