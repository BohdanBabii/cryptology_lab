import argparse
from math import fsum
from pathlib import Path
from collections import Counter

VOCAB = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
TABLE = dict(zip(VOCAB, range(26)))


def _split_text(window: int, text: str) -> list[str]:
    text = "".join(c for c in text.upper() if c in TABLE)
    texts = []
    for i in range(window):
        column = ""
        j = 0
        while i + j * window < len(text):
            column += text[i + j * window]
            j += 1
        texts.append(column)
    return texts


def _compute_coinzidenz_index(splits: list[str]) -> float:
    coid = []
    for split in splits:
        n = len(split)
        if n < 2:
            continue
        normal_factor = 1 / (n * (n - 1))
        counts = Counter(split)
        sum = 0
        for _, count in counts.items():
            sum += count * (count - 1)
        coid.append(normal_factor * sum)

    if not coid:
        raise ValueError("The splits are to short < 2 chars.")

    return fsum(coid) / len(splits)


def _choose_windows(coids: list[float], delta: float) -> dict[int, float]:
    windows = {}
    for i in range(len(coids)):
        if coids[i] >= delta:
            windows[i + 1] = coids[i]
    return windows


def _compute_distance_to_char(
    text: str, windows: dict[int, float], char: str
) -> dict[int, list[int]]:
    if len(char) != 1:
        raise ValueError("Char has to be a single letter.")

    distance_tables: dict[int, list[int]] = {}
    for window, _ in windows.items():
        distances_in_split = []
        split = _split_text(window=window, text=text)
        for i in range(len(split)):
            counts = Counter(split[i])
            letter = max(counts, key=counts.get)
            distances_in_split.append((TABLE[letter] - TABLE[char]) % 26)
        distance_tables[window] = distances_in_split
    return distance_tables


def _reverse_distances_to_chars(distance_tables: dict[int, list[int]]) -> list[str]:
    keys = []
    for n, distances in distance_tables.items():
        key = []
        for distance in distances:
            key.append(VOCAB[distance])
        keys.append("".join(key))
    return keys


def read_file(input_path: Path) -> str:
    with open(input_path, encoding="utf-8") as f:
        return f.read()


def write_file(output_path: Path, text: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


def decode_keys(input_file: str, delta: float, char: str) -> list[str]:
    splits = []
    coids = []
    for i in range(1, 101):
        splits = _split_text(window=i, text=input_file)
        coids.append(_compute_coinzidenz_index(splits=splits))
    windows = _choose_windows(coids=coids, delta=delta)
    distance_tables = _compute_distance_to_char(
        text=input_file, windows=windows, char=char
    )
    keys = _reverse_distances_to_chars(distance_tables=distance_tables)
    return keys


def decrypt_texts(text: str, keys: list[str]) -> str:
    message = ""
    for key in keys:
        message += f"Key: {key} \n"
        message += "\n"
        msg = _decrypt_text(code=text, key=key)
        message += msg
        message += "____________________________________________________________"
        message += "\n"
    return message


def _decrypt_text(code: str, key: str) -> str:
    _validate_key(key)
    key = key.upper()
    text = []
    pos = 0
    for char in code.upper():
        if char in TABLE:
            shift = TABLE[key[pos % len(key)]]
            text.append(VOCAB[(TABLE[char] - shift) % 26])
            pos += 1
        else:
            text.append(char)
    return "".join(text)


def _validate_key(key: str) -> None:
    if not (key.isalpha() and key.isascii()):
        raise ValueError("Key has to consist of letters A-Z.")


def main(input_path: str, output_path: str, delta: float = 0.06, char: str = "E"):
    input = read_file(input_path=Path(input_path))
    keys = decode_keys(input_file=input, delta=delta, char=char)
    text = decrypt_texts(text=input, keys=keys)
    write_file(output_path=Path(output_path), text=text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vigenere decoder")
    parser.add_argument("--input-path", required=True)
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--delta", type=float, default=0.9)
    parser.add_argument("--char", default="E")
    args = parser.parse_args()
    main(args.input_path, args.output_path, args.delta, args.char)
