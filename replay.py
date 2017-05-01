import argparse
from datetime import datetime
import time


def buildArgParser():
    parser = argparse.ArgumentParser(
        prog='replay', description='replay znc logs')
    parser.add_argument(
        '--file', required=True, help='Log file to replay')
    parser.add_argument(
        '--double', required=False, help='Double the speed I should playback the logs', action='store_true')
    parser.add_argument("--start", required=False, help='Where to start the replay')
    parser.add_argument("--stop", required=False, help='Where to stop the replay')
    parser.add_argument(
        '--verbose', required=False, help='Print a bit more information', action='store_true')
    return parser.parse_args()


def get_file_contents(_file):
    with open(_file) as file:
        return file.readlines()


def print_delay(_log, _delay=0):
    if args.double:
        _delay = _delay / 2
    time.sleep(_delay)
    print(_log)

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

for log in logs:
    cur_time = datetime.strptime(log[1:9], '%H:%M:%S')

    # check to see if logstop is defined.  if so, we want to use this to know when to stop processing
    try:
        logstop
    except:
        logstop='99:99:99'
    else:
        if log[1:9] > logstop:
            # print(log)
            endtime = datetime.now()
            print("END", endtime - starttime)
            print("We will stop where you said to: %s" % args.stop)
            exit(0)

    # check to see if prev has been set yet
    try:
        prev_time
    # prev is not set... so our first run
    except:
        # print("no prev")
        pass
    else:
        # print("setting sleep_sec")
        sleep_sec = (cur_time - prev_time).total_seconds()

    # check to see if logstart is defined.  if so, we want to use this to know when to start processing logs
    try:
        logstart
    except:
        logstart = '00:00:00'
        prev_time = cur_time
        print_delay(log)
    else:
        if log[1:9] >= logstart:
            prev_time = cur_time
            # print("trying sleep_sec")

            try:
                sleep_sec
            except:
                # print("no sleep")
                print(log)
            else:
                print_delay(log, sleep_sec)

endtime = buildArgParser()

exit(0)