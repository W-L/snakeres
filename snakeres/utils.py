import argparse
from pathlib import Path
from importlib.metadata import version


def parse_args() -> argparse.Namespace:
    '''
    Parse the command line arguments
    :return: parsed arguments in a namespace object
    '''
    parser = argparse.ArgumentParser(
        description="Generate a workflow profile from a snakefile")
    parser.add_argument(
        "--input",
        help="Path to snakefile"
    )
    parser.add_argument(
        "--output-profile",
        default="profile.yaml",
        help="Output profile file (default: profile.yaml)"
    )
    parser.add_argument(
        "--output-smk",
        default="snakefile_cleaned",
        help="Output snakefile without the directives (default: snakefile_cleaned)"
    )
    args = parser.parse_args()

    # convert arguments to Path objects
    args.input = Path(args.input)
    args.output_profile = Path(args.output_profile)
    args.output_smk = Path(args.output_smk)
    # check that the input file exists
    assert Path.is_file(args.input)
    return args



def init_logger(args: argparse.Namespace) -> None:
    """
    Initialize the logger with the given logfile and log the arguments.

    :param logfile: The path to the logfile.
    :param args: The arguments to log.
    """
    import logging
    logging.basicConfig(format='%(asctime)s %(message)s',
                        level=logging.INFO,
                        handlers=[logging.StreamHandler()])

    logging.info(f"snakeres {version('snakeres')}")
    logging.info('')
    logging.info('Arguments:')
    for a, aval in args.__dict__.items():
        logging.info(f'  {a}{aval}')
    logging.info('')



def try_convert_to_int(value) -> int | str:
    '''
    Try to convert a value to an integer, otherwise return the value as is.
    :param value: input value to convert
    :return: either converted or original value
    '''
    try:
        value_conv = int(value)
        return value_conv
    except ValueError:
        return value
    except TypeError:
        return value

