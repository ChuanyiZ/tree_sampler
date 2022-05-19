import pandas as pd
import numpy as np
import json
import argparse
def main():
    parser = argparse.ArgumentParser(
        description='This file converts the clustering output of pyclone-vi to the parameters file for pairtree',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    args = parser.parse_args()
    df = pd.read_csv(args.input_file, sep='\t') #adapted from pyclone-vi
    mutations = df['mutation_id']
    clusterIDs = df['cluster_id']
    samples = df['sample_id']

    #Instead of having each mutation labeled with a cluster ID, pairtree wants an array with each cluster's mutation id's grouped together
    uniq_Z  = set(list(clusterIDs)) #from clustervars.py, convert_assignment_to_clustering function
    assert uniq_Z == set(range(len(uniq_Z)))
    clusters = [[mutations[vidx] for vidx in np.flatnonzero(clusterIDs == cidx)] for cidx in sorted(uniq_Z)]

    garbage = [] #This assumes there are no garbage mutations identified yet. Will need to switch this line if garbage mutations are identified before this point.

    params = { #adapted from pairtree
        'clusters': clusters,
        'garbage': garbage,
        'samples': samples[0], #This assumes that all samples have the same name; switch this to get each unique file name if this assumption fails to be true
    }
    with open(args.output_file, 'w') as F:
        json.dump(params, F)

if __name__ == '__main__':
    main()