#!/usr/bin/env python2
from __future__ import print_function

import argparse
import pickle

import pandas as pd
import os

import argparse
import numpy as np
import os
import sys


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
import resultserializer
import inputparser
import util

def main():
    parser = argparse.ArgumentParser(
        description='Create mapping from clusters to mutations',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('pairtree_output')
    parser.add_argument('clusterMutationMap')
    parser.add_argument('out_fn')
    args, unknown = parser.parse_known_args()

    fh = open(args.clusterMutationMap, 'rb')
    clusterMutationMap = pickle.load(fh)

    results = resultserializer.Results(args.pairtree_output)
    data = results.get('adjm')
    trajectories = []
    for adjm in data:
        N = len(adjm)
        usedNodes = [0]
        create_tree(adjm, 0, [], trajectories, clusterMutationMap, usedNodes.copy())

    for trajectory in trajectories:
        print("**************")
        print(trajectory)

    print("***cluster Mutation Map")
    print(clusterMutationMap)

    fh = open(args.out_fn, 'wb')
    pickle.dump(trajectories, fh)


def create_tree(adjm, parentIdx, curr_list, trajectories, clusterMutationMap, usedNodes):
    leaf = True
    N = len(adjm)
    for n in range(N):
        if n not in usedNodes:
            if adjm[parentIdx][n] == 1:
                new_list = curr_list.copy()
                leaf = False
                new_list.append(clusterMutationMap[n-1]) #subtract 1 because mutations are one off
                usedNodes.append(n)
                create_tree(adjm, n, new_list.copy(), trajectories, clusterMutationMap, usedNodes.copy())
    if leaf == True:
        trajectories.append(curr_list)






if __name__ == '__main__':
  main()
