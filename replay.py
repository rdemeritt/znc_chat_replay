import argparse
from datetime import datetime
import time
import colorize_nick as cn


def buildArgParser():
    parser = argparse.ArgumentParser(
        prog='replay', description='replay znc logs')
    parser.add_argument(
        '--file', required=True, help='Log file to replay')
    parser.add_argument(
        '--double', required=False, help='Double the speed I should playback the logs', action='store_true')
    parser.add_argument('--start', required=False, help='Where to start the replay')
    parser.add_argument('--stop', required=False, help='Where to stop the replay')
    parser.add_argument('--no_time', required=False, help='If set we will not display the time when replaying logs',
                        action='store_true')
    parser.add_argument(
        '--verbose', required=False, help='Print a bit more information', action='store_true')
    return parser.parse_args()


def get_file_contents(_file):
    with open(_file) as file:
        return file.readlines()


def print_delay(_log, _delay=0):
    # see if we should speed things up
    if args.double:
        _delay = _delay / 2

    # see if we need to omit the timestamp
    if args.no_time:
        _log = _log[11:]

    time.sleep(_delay)
    try:
        print(_log)
    except:
        return False
    else:
        return True


args = buildArgParser()

starttime = datetime.now()

if args.start and args.stop:
    print (args.stop, args.start)
    start = datetime.strptime(args.start, '%H:%M:%S')
    stop = datetime.strptime(args.stop, '%H:%M:%S')
    print("BEGIN", stop - start)

if args.start:
    logstart = args.start

if args.stop:
    logstop = args.stop

if args.file:
    try:
        logs = get_file_contents(args.file)
    except Exception as err:
        print(err)
        exit(1)

nick_dict = cn.build_nick_dict_from_znc_logs(logs)

for log in logs:
    try:
        cur_time = datetime.strptime(log[1:9], '%H:%M:%S')
    except Exception as err:
        continue

    # check to see if logstop is defined.  if so, we want to use this to know when to stop processing
    try:
        logstop
    except:
        pass
    else:
        if log[1:9] > logstop:
            endtime = datetime.now()
            print("END", endtime - starttime)
            exit(0)

    # check to see if prev has been set yet
    try:
        prev_time
    # prev is not set... so our first run
    except:
        pass
    else:
        sleep_sec = (cur_time - prev_time).total_seconds()

    # check to see if logstart is defined.  if so, we want to use this to know when to start processing logs
    try:
        logstart
    except:
        logstart = '00:00:00'
        prev_time = cur_time
        print_delay(cn.colorize_nick_in_string(log, nick_dict))
    else:
        if log[1:9] >= logstart:
            prev_time = cur_time

            try:
                sleep_sec
            except:
                # sleep_sec not set...  should be our first log
                print(cn.colorize_nick_in_string(log, nick_dict))
            else:
                print_delay(cn.colorize_nick_in_string(log, nick_dict), sleep_sec)

endtime = buildArgParser()

exit(0)