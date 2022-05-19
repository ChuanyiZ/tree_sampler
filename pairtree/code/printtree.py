import argparse
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import pandas as pd


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))
import resultserializer
import inputparser
import vaf_plotter
import util


def main():
    #Code in this file adapted from Pairtree
    parser = argparse.ArgumentParser(
        description='Print results from trees in pairtree',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('results_fn')
    parser.add_argument('ssm_fn')
    parser.add_argument('out_fn')
    parser.add_argument('plot_fn')
    args = parser.parse_args()
    #Getting data out of files
    results = resultserializer.Results(args.results_fn)
    data = {K: results.get(K) for K in ( #from plottree, line 313
        'adjm',
        'struct',
        'count',
        'llh',
        'prob',
        'phi',
    )}
    data['clusters'] = results.get('clusters') #from plottree
    variants = inputparser.load_ssms(args.ssm_fn)
    clusters = data['clusters']
    clustered_vars = [[variants[vid] for vid in C] for C in clusters]

    #Creating boxplot of distributions of variant allele frequencies in clusters
    vafs = {}
    for cidx, cluster in enumerate(clustered_vars):
        vafs['Cluster ' + str(cidx)] = np.array([var['vaf'][0] for var in cluster])
    [labelsToPlot, vafToPlot] = [*zip(*vafs.items())]
    plt.boxplot(vafToPlot)
    plt.xticks(range(1, len(labelsToPlot) + 1), labelsToPlot)
    plt.ylabel("Variant Allele Frequency")
    plt.title("Distribution of Mutation VAF across Clusters")
    plt.savefig(args.plot_fn)

    #Creating file of tree adjacency matricies
    treeStructures = data['adjm']
    treeProb = data['prob']
    numberOfTreesMessage = "Number of trees = " + str(len(treeProb)) + "\n"
    with open(args.out_fn, 'a') as f:
        original_stdout = sys.stdout
        sys.stdout = f
        print(args.results_fn)
        print("\n")
        print(numberOfTreesMessage)
        print("Tree probabilities\n")
        print(treeProb)
        print("\nTreeStructures\n")
        print(treeStructures)
        print("\n")
        sys.stdout = original_stdout


if __name__ == '__main__':
    main()