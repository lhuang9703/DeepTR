cd ../../

currpath=`pwd`
# train the model
python matchzoo/main.py --phase train --model_file ${currpath}/examples/bioasq/config/mvlstm_bioasq.config

# predict the model
python matchzoo/main.py --phase predict --model_file ${currpath}/examples/bioasq/config/mvlstm_bioasq.config
