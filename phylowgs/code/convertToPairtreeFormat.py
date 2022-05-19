import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description='Adjust ssm file from pyclone-vi format to fit pairtree',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('ssm_fn')
    parser.add_argument('new_ssm_fn')
    args = parser.parse_args()
    df = pd.read_csv(args.ssm_fn, sep='\t')
    #changing column names from the pyclone-vi names to the pairtree names
    df.rename(columns={'mutation_id': 'id', 'gene': 'name', 'ref_counts': 'ref_reads', 'alt_counts': 'var_reads', 'total_counts': 'total_reads'}, inplace=True)
    df.to_csv(args.new_ssm_fn, sep='\t')

if __name__ == '__main__':
    main()