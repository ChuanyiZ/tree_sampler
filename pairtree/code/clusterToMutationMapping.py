#!/usr/bin/env python2
from __future__ import print_function

import argparse
import pickle

import pandas as pd
import os

def main():
    parser = argparse.ArgumentParser(
        description='Create mapping from clusters to mutations',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('cluster_fn', action="store")
    parser.add_argument('pairtree_ssm_fn', action= "store")
    parser.add_argument('out_fn', action= "store")
    args, unknown = parser.parse_known_args()
    clusterDf = pd.read_csv(args.cluster_fn, sep='\t')
    mutationDf = pd.read_csv(args.pairtree_ssm_fn, sep='\t')

    #since mutation IDs are in order, to get from mutation#-> chrom, pos mapping, use:
    #mutationDf['id'][mutationNumber]

    clusterMutationMap = dict()
    for idx, row in clusterDf.iterrows():
        clusterID = row['cluster_id']
        mutationNumber = row['mutation_id']
        mutationNumber = int(float(mutationNumber[1:]))
        chromPos = mutationDf['name'][mutationNumber] #note, assuming mutationNumber can be used to index
        if clusterID in clusterMutationMap.keys():
            clusterMutationMap[clusterID].append(chromPos)
        else:
            clusterMutationMap[clusterID] = [chromPos]

    fh = open(args.out_fn, 'wb')
    pickle.dump(clusterMutationMap, fh)


if __name__ == '__main__':
  main()