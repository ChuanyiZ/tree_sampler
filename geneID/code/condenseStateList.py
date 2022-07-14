from __future__ import print_function

import argparse


def main():
    parser = argparse.ArgumentParser(
        description='Condense state list',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('stateList_fn')
    parser.add_argument('uniqueStateList_fn')
    args, unknown = parser.parse_known_args()

    f = open(args.stateList_fn)
    g = open(args.uniqueStateList_fn, "w")
    with open(args.stateList_fn) as f:
        listOfStates = f.readline()
        print(listOfStates)
        listOfStates = listOfStates.split(sep=',')
        print(listOfStates)
        listOfUniqueStates = set(listOfStates)
        for state in listOfUniqueStates:
            g.write(state + ",")
    g.close()

if __name__ == '__main__':
  main()
    
