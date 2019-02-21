#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
##
# Distributed under terms of the MIT license.

"""
generate bioasq answer
"""

import codecs
import json


def load_json_file(file_name):
    with open (file_name, 'r') as f:
        data = json.load(f)
    return data


def generate_answer_file(file1_name, json_data, id_trans_file_name, file2_name):
    id_dict = {}
    with codecs.open (id_trans_file_name, 'r', 'utf8') as f:
        for line in f:
            if not line:
                break
            line = line.strip('\n')
            line = line.split('\t')
            if len(line) == 2:
                if line[1] not in id_dict:
                    id_dict[line[1]] = line[0]
    
    with codecs.open (file1_name, 'r', 'utf8') as f:
        temp_dict = {}
        for line in f:
            if not line:
                break
            line = line.strip('\n')
            line = line.split('\t')
            if len(line) == 7:
                # qid = id_dict[line[0]]
                # answer_id = id_dict[line[2]]
                qid = line[0]
                answer_id = line[2]
                if qid not in temp_dict:
                    temp_dict[qid] = []
                if line[3] in [str(x) for x in range(0, 10)]:
                    temp_dict[qid].append(answer_id)
    
    pref = "http://www.ncbi.nlm.nih.gov/pubmed/"
    for j in range(len(json_data['questions'])):
        qid = json_data['questions'][j]['id']
        try:
            doc_list = [pref + x for x in temp_dict[qid]]
        except:
            continue
        json_data['questions'][j]['documents'] = doc_list
    
    with codecs.open(file2_name, 'w', 'utf8') as f:
        json.dump(json_data, f, indent=2)


if __name__ == '__main__':
    src_dir = './'
    dst_dir = './'
    input_json_file = 'phaseA_6b_05.json'
    out_json_file = src_dir + 'source_data/' + 'phaseA_6b_05_mvlstm_answer_trec.json'
    predict_file = dst_dir + '../../predict.test.mvlstm.bioasq6b05trec.txt'
    id_trans_file = src_dir + 'id_trans.txt'
    json_data = load_json_file(src_dir + 'source_data/' + input_json_file)
    print("begin to generate answer file...")
    generate_answer_file(predict_file, json_data, id_trans_file, out_json_file)
    print("Done...")
