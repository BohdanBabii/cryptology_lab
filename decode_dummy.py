import argparse
from pathlib import Path

def read_file(input_path: Path) -> str:
    with open(input_path, encoding="utf-8") as f:
        return f.read()

def decode(input_file: str, output_file: str) -> str:
    raise NotImplementedError

def main(input: str,  output: str):
    input = read_file(input_path=Path(input))
    output = read_file(input_path=Path(output))
    key = decode(input_file=input, output_file=output)
    print(key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vigenere encoder")
    parser.add_argument("--input-path", required=True)
    parser.add_argument("--output-path", required=True)
    args = parser.parse_args()
    main(args.input_path, args.output_path)
