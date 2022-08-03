import argparse
import pandas as pd
import pickle
import os
import sys
import numpy as np
import pysam 
import json 
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

def main():
    parser = argparse.ArgumentParser(
        description='Look at metadata',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('config')
    parser.add_argument('path')
    parser.add_argument('vcfpath')
    parser.add_argument('numTrajectories')
    parser.add_argument('maxNumMutations')
    parser.add_argument('json_fn')
    args, unknown = parser.parse_known_args()

    information = dict()

    configf = open(args.config)
    config = yaml.safe_load(configf)
    configf.close()

    for sample in config["samples"]:
        trajectories_fn = args.path + "/trajectoriesProb/" + sample + "_trajectoriesProb"
        vcf_fn = args.vcfpath + "/" + sample + ".wxs.aliquot_ensemble_masked.vcf"
        ssm_fn = args.path + "/ssm_files/" + sample + "_ssm"

        #Get out mutation list, store in json
        mutations = get_mutation_list(vcf_fn, ssm_fn)

        if len(mutations) <= int(args.maxNumMutations):

            #Get trajectory, store in json 
            trajectories = getTrajectories(trajectories_fn, int(args.numTrajectories))

            sampleInformation = dict()
            sampleInformation["Mutations"] = mutations
            sampleInformation["Trajectories"] = trajectories

            information[sample] = sampleInformation

    jsonFormattedInfo = json.dumps(information, indent=4)

    with open(args.json_fn, "w") as f:
        f.write(jsonFormattedInfo)


        



def get_mutation_list(vcf_fn, ssm_fn):
    df = pd.read_csv(ssm_fn, sep='\t')
    mutation_list = []
    for idx, row in df.iterrows():
        mutationStr = ""
        id = row['id']
        mutation = row['gene']
        chrom, pos = mutation.split('_')
        chrom = "chr" + str(chrom)
        pos = int(pos)
        reference, alt = getRefAlt(chrom, pos, vcf_fn)
        mutationStr = chrom + "_" + str(pos) + "-" + reference + "-" + alt[0]
        mutation_list.append(mutationStr)
    return mutation_list


def getRefAlt(chrom, mutation_pos, vcf_file):
    mutation_pos -= 1 #switching to 0-based indexing 

    vcf = pysam.VariantFile(vcf_file)
    variant = None
    for v in vcf:
        if v.chrom == chrom and v.start == mutation_pos:
            variant = v
            break

    reference = variant.ref
    alt = variant.alts

    return reference, alt

def getTrajectories(traj_fn, numTrajectories):
    trajectory_list = []
    fh = open(traj_fn, 'rb')
    trajectories = pickle.load(fh)
    for i in range(0, min(numTrajectories, len(trajectories))):
        trajectory_list.append(trajectories[i][0])
    return trajectory_list 

if __name__ == '__main__':
  main()