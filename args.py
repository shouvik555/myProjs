#!/opt/homebrew/bin/python3

import argparse
import sys

def getargs():
    parser = argparse.ArgumentParser(description='Tool to check')
    parser.add_argument('-a', '--all', action='store_true', help='Perform all actions')
    parser.add_argument('-c', '--check', action='store_true', help='Check the error') 
    parser.add_argument('-f', '--fix', action='store_true', help='Fix the error') 

    #Example of mutually exclusive options
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--email', action='store_true', help='Notify by email')
    group.add_argument('-s', '--slack', action='store_true', help='Notify by Slack')

    parser.add_argument('-n', '--name', type=str, required=True, help='Name of Host') 

    #If we want to display usage and exit out if no options are passed
    if (len(sys.argv)) < 2:
        parser.print_help()
        sys.exit(1)

    #If we want to enable an option if no args are passed (ONLY applies if no required args are there)
    if (len(sys.argv)) < 2:
        thisArgs=parser.parse_args()
        thisArgs.all=True
        return thisArgs
    return parser.parse_args()


if __name__ == "__main__":
    myArgs = getargs()
    print(myArgs)

    print('Host name to work on: '+myArgs.name)
    if myArgs.all:
        print('All option is selected')

    if myArgs.check:
        print('Check option is selected')

    if myArgs.fix:
        print('Fix option is selected')
