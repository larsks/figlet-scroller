import argparse
import blessed
import itertools
import subprocess
import time
import dotenv
import os

dotenv.load_dotenv()

DEFAULT_FONT = os.getenv("FIGLET_FONT", "big")
DEFAULT_INTERVAL = os.getenv("FIGLET_INTERVAL", "0.1")


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument("-f", "--font", default=DEFAULT_FONT)
    p.add_argument("-i", "--interval", type=float, default=DEFAULT_INTERVAL)
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
            raise ValueError("inconsistent line length")

    banner = [line for line in banner if line.strip()]

    term = blessed.Terminal()

    if linelen < term.width:
        for i in range(len(banner)):
            banner[i] = " ".join([banner[i]] * (1 + (term.width // linelen)))
        linelen = len(banner[0])

    pos = itertools.cycle(range(linelen))
    with term.fullscreen():
        print(term.clear())
        while True:
            for p in pos:
                window = (p, min(linelen, p + term.width))
                remainder = term.width - (window[1] - window[0])
                for i, line in enumerate(banner):
                    print(term.move_xy(0, i) + line[window[0] : window[1]], end="")
                    if remainder > 0:
                        print(line[0:remainder], end="")
                print()

                # print(
                #     f"linelen {linelen} width {term.width} pos {p} remainder {remainder} window {window}           "
                # )

                time.sleep(args.interval)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
