from __future__ import print_function

import argparse
import pickle

import pandas as pd
import re

import fcntl

def main():
    parser = argparse.ArgumentParser(
        description='Create mapping from clusters to mutations',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('cluster_fn', action="store")
    parser.add_argument('pairtree_ssm_fn', action= "store")
    parser.add_argument('gff3_fn')
    parser.add_argument('clusterGeneIDMap_fn', action= "store")
    parser.add_argument('mutationsList_fn')
    parser.add_argument('geneIDList_fn')
    parser.add_argument('log_fn')

    args, unknown = parser.parse_known_args()
    clusterDf = pd.read_csv(args.cluster_fn, sep='\t')
    mutationDf = pd.read_csv(args.pairtree_ssm_fn, sep='\t')

    #since mutation IDs are in order, to get from mutation#-> chrom, pos mapping, use:
    #mutationDf['id'][mutationNumber]

    no_match_list = []
    multiple_match_list = dict()
    mutationGeneIDMap = dict()
    clusterGeneIDMap = dict()
    mutationList = []
    geneIDList = []
    gff3_fh = open(args.gff3_fn, 'rb')
    gencode = pickle.load(gff3_fh)

    #Getting out mutations, finding corresponding GeneID and adding to both mutationGeneIDMap and clusterGeneIDMap
    for idx, row in clusterDf.iterrows():
        clusterID = row['cluster_id']
        mutationNumber = row['mutation_id']
        mutationNumber = int(float(mutationNumber[1:]))
        chromPos = mutationDf['name'][mutationNumber] #note, assuming mutationNumber can be used to index
        chromPos_split = chromPos.split("_")
        chromosome = "chr" + chromPos_split[0]
        positionNumber = int(chromPos_split[1])

        gene_list = getGenID(chromosome, positionNumber, gencode, args.log_fn)

        mutationGeneIDMap[chromPos] = gene_list 

        #Getting data about mutations with 0 or multiple gene matches to include in the log
        #if len(gene_list) == 0:
        #    no_match_list.append(chromPos)
        #if len(gene_list) > 1:
        #    multiple_match_list[chromPos] = gene_list

        #Addng geneID into the clusterGeneID map
        if clusterID in clusterGeneIDMap.keys():
            clusterGeneIDMap[clusterID].append(gene_list)
        else:
            clusterGeneIDMap[clusterID] = [gene_list]

        #Adding geneID into the states list 
        mutationList.append(chromPos)
        geneIDList.append(gene_list)

    #with open(args.log_fn, "a") as file:
    #    file.write(clusterGeneIDMap)
    #    file.write("no match\n")
    #    file.write(no_match_list)
    #    file.write("multiple match\n")
    #    file.write(multiple_match_list)

    fh = open(args.clusterGeneIDMap_fn, 'wb')
    pickle.dump(clusterGeneIDMap, fh)
    fh.close()

    with open(args.mutationsList_fn, "a") as g:
        fcntl.flock(g, fcntl.LOCK_EX)
        for mutation in mutationList:
            g.write(mutation + ",")
        fcntl.flock(g, fcntl.LOCK_UN)

    with open(args.geneIDList_fn, "a") as h:
        fcntl.flock(h, fcntl.LOCK_EX)
        for genelist in geneIDList:
            for gene in genelist:
                h.write(gene + ",")
        fcntl.flock(h, fcntl.LOCK_UN)

    

def getGenID(chrom, pos, gencode, log_fn):
    chromosomePortionOfGencode = gencode[gencode["seqname"] == chrom]
    gene_list = []
    #Considering the mutation to correspond to the gene_id on the same chromosome, where the position of the mutation is between (inclusive) the start
    #and end positions of the gene.
    #Mutliple gene_id matches are permitted
    for idx, row in chromosomePortionOfGencode.iterrows():
        if int(row["start"]) <= pos and int(row["end"]) >= pos:
            with open(log_fn, "a") as file:
                file.write(chrom + "\n")
                file.write(str(pos) + "\n")
                file.write(row["attribute"])
            attribute = row["attribute"]
            g = re.search(r'gene_id=(.*);gene_type', attribute) #dealing with regexp to get out gene_id
            start = g.start() + 8
            end = g.end() - 10
            gene_id = attribute[start:end]
            gene_list.append(gene_id)
    return gene_list


if __name__ == '__main__':
  main()