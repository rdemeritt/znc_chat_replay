import argparse
import re
from random import choice
from colorama import init, Fore, Back


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

    backgrounds = [Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN]
    foregrounds = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

    for log in _znc_logs:
        primary_nick = re.search(primary_nick_re, log)

        if primary_nick is None:
            continue
        else:
            primary_nick = primary_nick.group(0)[1:-1]

        if not primary_nick in nick_dict:
            nick_dict[primary_nick] = choice(foregrounds)
    return nick_dict


def print_colored_logs(_logs, _dict):
    for log in _logs:
        primary_nick = re.search(primary_nick_re, log)
        # target_nick = re.search(target_nick_re, log)

        if primary_nick is None:
            print(log.strip('\n'))
            continue
        else:
            primary_nick = primary_nick.group(0)[1:-1]

        print(log.replace(primary_nick, (_dict[primary_nick] + primary_nick + Fore.RESET)).strip('\n'))
    return True


def colorize_nick_in_string(_string, _dict):
    primary_nick = re.search(primary_nick_re, _string)
    # target_nick = re.search(target_nick_re, _string)
    # quit_nick = re.search(quit_nick_re, _string)

    if primary_nick is None:
        return(_string.strip('\n'))
    else:
        primary_nick = primary_nick.group(0)[1:-1]

    try:
        colored_string = _string.replace(primary_nick, (_dict[primary_nick] + primary_nick + Fore.RESET))
        # colored_string = _string.replace(target_nick, (_dict[target_nick] + target_nick + Fore.RESET))
    except Exception as err:
        return(_string)
    else:
        return colored_string.strip('\n')


primary_nick_re = '\<[a-zA-Z0-9_\-\`]+\>'
target_nick_re = '(\> [a-zA-Z0-9_\-\`]+\:'
quit_nick_re = ' Quits\: [a-zA-Z0-9_\-\`]+ '

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
    print_colored_logs(logs, nick_dict)
    # print(nick_dict[''])


if __name__ == '__main__':
    main()