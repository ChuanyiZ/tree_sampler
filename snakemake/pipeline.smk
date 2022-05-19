configfile: "config.yaml"

rule all:
    input: ""

rule create_phylowgs_inputs:
    input:
        vcf_gz="/Users/m269479/Projects/pipeline/mafs/tcga_mafs/0007c172-1593-4710-a4fb-ceb1e292d19e/vcfs/0c303a91-3821-46eb-b822-9a7329d663df.wxs.aliquot_ensemble_masked.vcf.gz"
    output:
        ssm=""
        params=""
    log: ""
    container: "docker://chuanyiz/phylowgs"
    shell:
        "cd phylowgs/parser/ && "
        "python create_phylowgs_inputs.py "
        "--tumor-sample ASCProject_0047_T1_WES_1 "
        "--vcf-type sample1=mutect_smchet "
        "sample1={input.vcf_gz} "
        "--output-variants ../../example_variants.ssm "
        "--output-params ../../example_params.txt "
        "--regions all &> {log}"

