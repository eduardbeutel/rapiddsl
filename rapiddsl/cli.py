import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        required=True,
        nargs='+',
        help='Definition files paths',
        metavar='file1.json file2.yaml'
    )
    parser.add_argument(
        '-t',
        required=True,
        help='Templates directory',
        metavar='templates'
    )
    parser.add_argument(
        '-b',
        required=False,
        help='Build directory',
        metavar='build',
        default = 'build'
    )
    return parser