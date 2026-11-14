import argparse
from pathlib import Path
from helper import S_BOXES, IP, FP, E, P


def read_file(input_path: Path) -> str:
    with open(input_path, encoding="utf-8") as f:
        return f.read()


def write_file(output_path: Path, code: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)


def encode(file: str, keys: str, decrypt: bool) -> str:
    block = _parse_block(file)
    key = _parse_round_keys(keys)
    result = _des_block(block=block, round_keys=key, decrypt=decrypt)
    return f"{result:016X}"


def _parse_block(text: str) -> int:
    value = int(text.strip(), 16)
    if value >> 64:
        raise ValueError("Input block is longer tahn 64 bits.")
    return value


def _parse_round_keys(text: str) -> list[int]:
    keys = [int(line.strip(), 16) for line in text.splitlines() if line.strip()]
    if len(keys) != 16:
        raise ValueError(f"Keys has not the right legnth {len(keys)}")
    if any(k >> 48 for k in keys):
        raise ValueError(f"Keys longer than  48 bit, legth: {len(keys)}")
    return keys


def _des_block(block: int, round_keys: list[int], decrypt: bool = False) -> int:
    if decrypt:
        round_keys = list(reversed(round_keys))

    block = _permute(block, IP, 64)
    l = block >> 32
    r = block & 0xFFFFFFFF

    for key in round_keys:
        tmp = l ^ _f(r, key)
        l = r
        r = tmp
    res = (r << 32) | l
    return _permute(res, FP, 64)


def _permute(value: int, table: list[int], size: int) -> int:
    res = 0
    for pos in table:
        bit = _get_bit(value=value, pos=pos, size=size)
        res = (res << 1) | bit
    return res


def _get_bit(value: int, pos: int, size: int) -> int:
    shift = size - pos
    return (value >> shift) & 1


def _sbox(num: int, six_ibts: int) -> int:
    first_bit = _get_bit(six_ibts, 1, 6)
    last_bit = _get_bit(six_ibts, 6, 6)
    row = first_bit * 2 + last_bit
    column = (six_ibts >> 1) & 0b1111
    return S_BOXES[num][row][column]


def _substitute(val: int) -> int:
    res = 0
    for i in range(8):
        shift = 48 - 6 * (i + 1)
        six_bits = (val >> shift) & 0b111111
        four_bits = _sbox(i, six_ibts=six_bits)
        res = (res << 4) | four_bits
    return res


def _f(r: int, key: int) -> int:
    expand = _permute(r, E, 32)
    mixed = expand ^ key
    subs = _substitute(mixed)
    return _permute(subs, P, 32)


def main(input: str, key_path: str, output: str, d: bool):
    file = read_file(input_path=Path(input))
    keys = read_file(Path(key_path))
    code = encode(file=file, keys=keys, decrypt=d)
    write_file(output_path=Path(output), code=code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DES encoder/decoder")
    parser.add_argument("-d", action="store_true", help="decrypt") 
    parser.add_argument("inputfile")
    parser.add_argument("keyfile")
    parser.add_argument("outputfile")
    args = parser.parse_args()
    main(args.inputfile, args.keyfile, args.outputfile, args.d)
