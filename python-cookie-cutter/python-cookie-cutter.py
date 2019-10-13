# -----------------------------------------------------------------------------
# Python Cookie Cutter
# -----------------------------------------------------------------------------
# Team: DataHub
# -----------------------------------------------------------------------------
# Author: Maxime Sirois
# -----------------------------------------------------------------------------
"""Python Cookie Cutter

This module creates a full python environment based on parameters found in the
./param/project_structure.json and templates found in the templates folder. It
is possible to add additional modules and stuff with the utilities provided in
this script.

Example:
    To initialize a new project:
        $ python python-cookie-cutter.py --init

    To add a new module:
        $ python python-cookie-cutter.py --new-module module_name

Todo:
    * Everything is left to be done
"""
# -----------------------------------------------------------------------------


import argparse
import logging
from pathlib import Path
import sys

from lib.python_cookie_cutter import projectbuilder
from lib.python_cookie_cutter import constants as C
from lib.python_cookie_cutter import interface
from lib.python_cookie_cutter import utils


def parse_args(args):
    """
    Argument parser
    :return: Parsed arguments object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("location", metavar="LOCATION", type=str,
                        help="Output Location without the project name")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--init", action="store_true",
                       help="Initialize project")
    group.add_argument("--newmodule", action="store_true",
                       help="Initialize a new module (project must have) "
                            "been initialized first")
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
    # config = C.get_config()

    # -- Fail fast
    assert Path(args.location).exists()

    # ----- LOGGING SETUP ------------------------
    BATCH_ID = utils.now('%Y%m%d%H%M%S')
    log_file_path = Path(C._PROJECT_FOLDER, 'logs', f'cookiecut_{BATCH_ID}.log')
    set_log(str(log_file_path), args.debug, args.silent)
    if not verbose:
        logging.getLogger().setLevel(logging.CRITICAL)
    # --------------------------------------------

    # DEFINE GENERAL VARIABLES FROM CONFIG
    # MY_VAR = config.get('SECTION', 'OPTION')

    # ---
    # Init interface
    # ---
    inter = interface.Interface()
    # ----
    # Initialize Project
    # ---
    if args.init:
        # Call Interface to gather answers and set attributes
        inter.init_project(args.location)
        # Read Parameter File
        parameters = utils.read_param(C._STRUCTURE_FILE, inter)
        # Start the Builder
        builder = projectbuilder.Builder(inter, parameters)
        builder.start()
    elif args.newmodule:
        # Call Interface to gather answers and set attributes
        inter.init_module(args.location)
        # Start the Builder
        builder = projectbuilder.Builder(inter)
        builder.add_new_module()


if __name__ == '__main__':
    main(sys.argv[1:])
