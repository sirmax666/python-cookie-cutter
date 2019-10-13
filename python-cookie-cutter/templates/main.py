import argparse
import logging
from pathlib import Path
import sys

from lib.{{project_name_slug}} import constants as C
from lib.{{project_name_slug}} import utils


def parse_args(args):
    """
    Argument parser
    :return: Parsed arguments object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("firstarg", metavar="FIRST_ARG", type=str,
                        help="First Argument Example")
    parser.add_argument("--debug", action="store_true",
                        help="Increases verbosity")
    parser.add_argument("--silent", action="store_true",
                        help="Turns off verbose")
    return parser.parse_args(args)


def set_log(log_file_path, debug=False, silent=False):
    """
    Set log configs for logging module
    :param bool debug: True = Use Debug, False = Use INFO
    """
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO

    logging.basicConfig(level=level,
                        format=('[%(asctime)s] %(name)-8s - '
                                '%(levelname)-8s: %(message)s'),
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_file_path,
                        filemode='w')

    if not silent:
        console = logging.StreamHandler()
        console.setLevel(level)
        formatter = logging.Formatter('%(levelname)-8s : %(message)s')
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)


def main(argv, verbose=True):
    """
    Main Program Launching
    """
    args = parse_args(argv)
    config = C.get_config()

    # ----- LOGGING SETUP ------------------------
    BATCH_ID = utils.now('%Y%m%d%H%M%S')
    log_file_path = Path(C._MAIN_FOLDER, 'logs' , f'{{project_name_slug}}_{BATCH_ID}.log')
    set_log(str(log_file_path), args.debug, args.silent)
    if not verbose:
        logging.getLogger().setLevel(logging.CRITICAL)
    # --------------------------------------------

    # DEFINE GENERAL VARIABLES FROM CONFIG
    # MY_VAR = config.get('SECTION', 'OPTION')


if __name__ == '__main__':
    main(sys.argv[1:])
