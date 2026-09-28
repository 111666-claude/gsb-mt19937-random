"""命令行入口：打印 MT19937 序列，并与标准库对照。"""

import argparse
import random
import sys

from .mt import MTRandom, RandomError


def build_parser():
    parser = argparse.ArgumentParser(prog="mt19937-random", description="MT19937")
    parser.add_argument("--seed", type=int, default=5489, help="种子")
    parser.add_argument("--count", type=int, default=3, help="输出多少个 32 位整数")
    parser.add_argument("--compare", action="store_true", help="与标准库 random 对照")
    parser.add_argument("--state-roundtrip", action="store_true", help="验证状态存取")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        generator = MTRandom(args.seed)
        values = [generator.next_uint32() for _ in range(args.count)]
        print("values=%s" % ",".join(str(value) for value in values))
        if args.compare:
            reference = random.Random(args.seed)
            expected = [reference.getrandbits(32) for _ in range(args.count)]
            print("expected=%s" % ",".join(str(value) for value in expected))
            print("match=%s" % (values == expected))
        if args.state_roundtrip:
            state, index = generator.get_state()
            first = generator.next_uint32()
            generator.set_state(state, index)
            second = generator.next_uint32()
            print("state_roundtrip=%s" % (first == second))
    except RandomError as error:
        print("错误：%s" % error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
