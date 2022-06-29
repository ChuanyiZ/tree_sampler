#!/usr/bin/env python2
from __future__ import print_function

import argparse
import pandas as pd
import os

def main():
    parser = argparse.ArgumentParser(
        description='Adjust ssm file output from phylowgs parser to fit pyclone-vi input format',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('ssm_fn')
    parser.add_argument('new_ssm_fn')
    #Note: once CNV data is available from create_phylowgs_inputs.py, add that file as an input argument
    args = parser.parse_args()
    df = pd.read_csv(args.ssm_fn, sep='\t')
    #adding sample_id field
    #Currently, the filename (minus the path & extension) is considered to be the sample_id. This will need to be changed
    #if a different sample_id is identified, or if multiple samples are in each file
    fileNameBase = os.path.basename(args.ssm_fn) #using fileNameBase as sample_id AH 7/26
    fileNameBase = fileNameBase.split('.vcf')[0] #Assuming the files come from .vcf files, so the .vcf and anything appended is assumed to not be
    #part of the sample_id
    df['sample_id'] = fileNameBase
    #adding in default copy numbers - assuming no copy number information is available.
    #This assumes a major/minor/normal copy number of 1/1/2, with a var_read_prob of .5 for autosomes or female X chromosomes- which are assumed to have a mu_v of .499, and
    #copy numbers of 1/0/1, with a var_read_prob of 1 for male sex chromosomes - which are assumed to have a mu_v of .001.
    #These assumptions may not be valid and should be checked once female data is identified.

    #Note: Once copy number data is available, change 'major_cn', 'minor_cn', and 'normal_cn' to be the major_cn, minor_cn, and normal_cn columns
    #in the cnv text file output from create_phylowgs_inputs
    df['major_cn'] = 1
    df['minor_cn'] = 1
    autosomal = df['mu_v'] == .499
    maleSexChromosome = df['mu_v'] == .001
    df.loc[autosomal, 'normal_cn'] = 2
    df.loc[maleSexChromosome, 'normal_cn'] = 1
    df.loc[maleSexChromosome, 'minor_cn'] = 0
    #adding in default variant read probabilities

    #Note: Once CNV data is available, change 'var_read_prob' to be dependent upon major_cn, minor_cn, and normal_cn columns
    df.loc[autosomal, 'var_read_prob'] = .5
    df.loc[maleSexChromosome, 'var_read_prob'] = 1

    #changing column names to be compatible with pyclone-vi
    df.rename(columns={'a': 'ref_counts', 'd': 'total_counts', 'id': 'mutation_id'}, inplace=True)
    df['alt_counts'] = df['total_counts'] - df['ref_counts']
    df.to_csv(args.new_ssm_fn, sep='\t')

if __name__ == '__main__':
  main()
