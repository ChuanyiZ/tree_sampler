import argparse
import pandas as pd 
import pickle


#Code from  https://medium.com/@PubuduSamarakoon/annotate-genes-and-genomic-coordinates-using-python-9259efa6ffc2, with minor adjustments

def main():
    parser = argparse.ArgumentParser(
        description='Getting gencode dataframe',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
    parser.add_argument('gff3_fn', action="store")
    parser.add_argument('out_fn')
    args, unknown = parser.parse_known_args()
    
    gencode = pd.read_table(args.gff3_fn, comment="#", sep = "\t", names = ['seqname', 'source', 'feature', 'start' , 'end', 'score', 'strand', 'frame', 'attribute'])
    gencode.head() 
    gencode.info()
    #get genes
    gencode_genes = gencode[(gencode.feature == "gene")][['seqname', 'start', 'end', 'attribute']].copy().reset_index().drop('index', axis=1)
    #gencode_genes["gene_name"], gencode_genes["gene_type"], gencode_genes["gene_status"], gencode_genes["gene_level"] = zip(*gencode_genes.attribute.apply(lambda x: gene_info(x)))
    gencode_genes["gene_name"], gencode_genes["gene_type"], gencode_genes["gene_level"] = zip(*gencode_genes.attribute.apply(lambda x: gene_info(x)))
    #remove duplicates
    gencode_genes = gencode_genes.sort_values(['gene_level', 'seqname'], ascending=True).drop_duplicates('gene_name', keep='first').reset_index().drop('index', axis=1)

    fh = open(args.out_fn, 'wb')
    pickle.dump(gencode_genes, fh)

def gene_info(x):
# Extract gene names, gene_type, gene_status and level
    g_name = list(filter(lambda x: 'gene_name' in x,  x.split(";")))[0].split("=")[1]
    g_type = list(filter(lambda x: 'gene_type' in x,  x.split(";")))[0].split("=")[1]
    #g_status = list(filter(lambda x: 'gene_status' in x,  x.split(";")))[0].split("=")[1]
    g_leve = int(list(filter(lambda x: 'level' in x,  x.split(";")))[0].split("=")[1])
    return (g_name, g_type, g_leve)

if __name__ == '__main__':
  main()