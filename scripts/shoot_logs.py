import sys
import random
import ast
import time
import re
import argparse

args = {
    'v': 1,
    'one': False,
    'sample': True,
} 
def get_lines(f):
    # read all lines and shoot them out
    with open(f, 'r') as f:
        lines = f.readlines()
    return lines


def print_log(out, sec):
    time.sleep(sec)
    error = out[6:-8]

    # Print error to user
    if args['v'] > 0:
        sys.stderr.write(error+'\n')
    
    # Strip error of new lines to make rebot
    # a bit efficient
    error = re.sub('\n',' ', error)
    
    # Print error to stdout for sweet rebot
    print error
    
if __name__ == '__main__':
    
    desc = "You are looking at Rebot helper CLI interface.\n"+\
           "This script keeps shooting logs till eternity."

    # Define arguments
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-o","--one",
                        help="shoot just one log to stdin",
                        action="store_true")
    parser.add_argument("-s","--sample",
                        help="keep shooting logs to stdin",
                        action="store_true")
    parser.add_argument("-v","--verbose",type=int,
                        help="pump up them verbose jargon")
    
    # Parse arguments
    a = parser.parse_args()
    
    # Perform actions
    if a.one:
        sys.stderr.write("### Just shooting one log out.\n\n\n") 
        args['one'] = True
    
    if a.sample:
        sys.stderr.write("### Going to shoot logs forever.\n\n\n") 
        args['sample'] = True

    if a.verbose > -1:
        args['verbose'] = a.verbose

    if args['one']:
        # just shoot the one log
        lines = get_lines('onelog.json')
        line = ast.literal_eval(lines[0])
        out = line['snippets']
        print_log(out,2)
        sys.exit()

    if args['sample']:
        # randomly keep shooting sample logs
        lines = get_lines('logs.json')
        _i = 0 
        while 1:
            i = random.randint(0,len(lines)-1)
            line = ast.literal_eval(lines[i])
            out = line['snippets']
            if '[ERROR]' not in out:
                print_log(out, 5)
            if args['v'] > 2:
                sys.stderr.write("#"*20)
                sys.stderr.write("#"*10+' log '+str(i)+"#"*10)
                sys.stderr.write("#"*20)
            _i += 1
