import argparse
import re
from random import choice
from colorama import init, Fore


def build_arg_parser():
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


def build_nick_dict_from_znc_logs(_znc_logs):
    nick_dict = {}
    primary_nick_re = '\<[a-zA-Z0-9]+\>'
    target_nick_re = '\> [a-zA-Z0-9]+\:'

    for log in _znc_logs:
        primary_nick = re.search(primary_nick_re, log)
        # print(primary_nick)

        if primary_nick is None:
            print(log.strip('\n'))
            continue
        else:
            primary_nick = primary_nick.group(0)[1:-1]

        if not primary_nick in nick_dict:
            nick_dict[primary_nick] = choice(foregrounds)
        print(log.replace(primary_nick, (nick_dict[primary_nick] + primary_nick + Fore.RESET)).strip('\n'))
    return nick_dict


foregrounds = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

def main():
    args = build_arg_parser()

    # configure colorama to always reset
    init(autoreset=True)

    try:
        logs = get_file_contents(args.file)
    except Exception as err:
        print(err)
        exit(1)

    nick_dict = build_nick_dict_from_znc_logs(logs)


if __name__ == '__main__':
    main()