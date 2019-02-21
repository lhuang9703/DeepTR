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


def get_data_from_trec_file(file_name):
    result = {}
    idx = 'first'
    doc_list = []
    with open(file_name, 'r') as f:
        while 1:
            line = f.readline()
            if not line:
                break
            else:
                if line == '\n':
                    continue
                line_split = line.split(' ')
                if len(line_split) == 1:
                    new_idx = line_split[0].replace('\n', '')
                    if idx != new_idx:                                                                                          
                        result[idx] = doc_list
                        idx = new_idx
                        doc_list = []
                else:
                    doc = line_split[2]
                    doc_list.append(doc)
            
    del(result['first'])
    # profix = 'http://www.ncbi.nlm.nih.gov/pubmed/'
    profix = ''
    for key in result:
        for item in range(len(result[key])):
            result[key][item] = profix + result[key][item]
    
    return result


def generate_relation_file(data, file_name, json_data, id_trans_file_name):
    id_dict = {}
    with codecs.open (id_trans_file_name, 'r', 'utf8') as f:
        for line in f:
            if not line:
                break
            line = line.split('\t')
            # print(line)
            if len(line) == 2:
                if line[0] not in id_dict:
                    id_dict[line[0]] = line[1].strip('\n')

    f = codecs.open(file_name, 'w', 'utf8')
    for k in range(len(json_data['questions'])):
        idx = json_data['questions'][k]['id']
        try:
            temp = data[idx]
        except:
            continue
        if len(data[idx]) == 20:
            for i in range(len(data[idx])):
                doc_id = data[idx][i]
                try:
                    f.write('0' + '\t' + idx + '\t' + doc_id + '\n')
                except:
                    continue
    f.close()


if __name__ == '__main__':
    src_dir = './'
    dst_dir = './'
    trec_file = src_dir + 'source_data/' + 'result_20_6b_05.txt'
    input_json_file = 'phaseA_6b_05.json'
    out_relation_file = dst_dir + 'relation_6b_05_trec.txt'
    id_trans_file = src_dir + 'id_trans.txt'
    trec_data = get_data_from_trec_file(trec_file)
    json_data = load_json_file(src_dir + 'source_data/' + input_json_file)
    print("begin to generate relation file...")
    generate_relation_file(trec_data, out_relation_file, json_data, id_trans_file)
    print("Done...")
