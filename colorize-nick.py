import argparse


def buildArgParser():
    parser = argparse.ArgumentParser(
        prog='colorize-nick', description='try our best to give unique colors to nicks in znc chat logs')
    parser.add_argument(
        '--file', required=True, help='Log file to replay')
    parser.add_argument(
        '--verbose', required=False, help='Print a bit more information', action='store_true')
    return parser.parse_args()


def get_file_contents(_file):
    with open(_file) as file:
        return file.readlines()


def catalog_nicks(_nick_list):
    return True


args = buildArgParser()

try:
    logs = get_file_contents(args.file)
except Exception as err:
    print(err)
    exit(1)