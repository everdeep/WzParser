import os
import logging
from datetime import datetime
from crypto import WzKey
from models import WzFile


def enable_console_logging():
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)

    # Simpler format
    formatter = logging.Formatter("%(name)-12s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)

    # add the handler to the root logger
    logging.getLogger("").addHandler(console)


def main(**kwargs):
    path = kwargs.get("path", "../data/UI.wz")
    logging_path = kwargs.get("logging_path", "../logs")
    console_log = kwargs.get("console_log", False)
    build_tree = kwargs.get("build_tree", False)
    logging_level = kwargs.get("logging_level", logging.INFO)

    if not os.path.exists(logging_path):
        os.makedirs(logging_path)

    logging.basicConfig(
        filename="{}/{:%Y-%m-%d}.log".format(logging_path, datetime.now()),
        level=logging_level,
        format="[%(asctime)s][%(levelname)s] {%(filename)s:%(lineno)d} %(message)s",
        datefmt="%H:%M:%S",
    )

    if console_log:
        enable_console_logging()

    wz_file = WzFile(path, WzKey()).parse(build_tree=build_tree)
    print(f"Done parsing {wz_file.name}")
    return wz_file


if __name__ == "__main__":
    main()
