import argparse
import blessed
import itertools
import subprocess
import time


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("-f", "--font", default="big")
    p.add_argument("-i", "--interval", type=float, default=0.1)
    p.add_argument("message")

    return p.parse_args()


def main():
    args = parse_args()
    banner = (
        subprocess.check_output(
            ["figlet", "-f", args.font, "-w", "10000", args.message]
        )
        .decode()
        .splitlines()
    )

    linelen = len(banner[0])
    for line in banner:
        if len(line) != linelen:
            raise ValueError("inconsitent line length")

    banner = [line for line in banner if line.strip()]

    term = blessed.Terminal()
    if linelen < term.width:
        for i, line in enumerate(banner):
            banner[i] = (banner[i] + "    ") * (term.width // linelen)
        linelen = len(banner[0])

    pos = itertools.cycle(range(linelen))
    while True:
        for p in pos:
            print(term.clear())
            remainder = term.width - (linelen - p)
            for line in banner:
                print(line[p : p + term.width], end="")
                if remainder > 0:
                    print(line[0:remainder], end="")
                print()
            print()

            time.sleep(args.interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
