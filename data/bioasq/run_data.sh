#!/bin/bash

# generate the mz-datasets
python prepare_mz_data.py

# generate word embedding
python gen_w2v.py bioasq_w2v.txt word_dict.txt embed_bioasq_d200
python norm_embed.py embed_bioasq_d200 embed_bioasq_d200_norm

# generate data histograms for drmm model
# generate data bin sums for anmm model
# generate idf file
cat word_stats.txt | cut -d ' ' -f 1,4 > embed.idf
python gen_hist4drmm.py 60
# python gen_binsum4anmm.py 20 # the default number of bin is 20

echo "Done ..."
