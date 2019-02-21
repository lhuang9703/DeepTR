#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
##
# Distributed under terms of the MIT license.

"""
generate bioasq answer
"""

import pickle
import codecs
import json


def load_train_data(DATA_DIR):
    """load bm25 data and docs of train"""
    with open(DATA_DIR + 'bioasq6_bm25_top100.full_train.pkl', 'rb') as f:
        train_data = pickle.load(f)
    with open(DATA_DIR + 'bioasq6_bm25_docset_top100.full_train.pkl', 'rb') as f:
        train_docs = pickle.load(f)
    return train_data, train_docs


def load_json_file(file_name):
    with open (file_name, 'r') as f:
        data = json.load(f)
    return data


def get_doc_by_id(doc_id, doc_data):
    """get text from train_docs by doc id"""
    if doc_id in doc_data:
        return doc_data[doc_id]['title'] + doc_data[doc_id]['abstractText']
    else:
        print(doc_id + 'not found')
        return ''

def generate_relation_file(data, file_name, json_data, id_trans_file_name):
    id_dict = {}
    with codecs.open (id_trans_file_name, 'r', 'utf8') as f:
        for line in f:
            if not line:
                break
            line = line.split('\t')
            print(line)
            if len(line) == 2:
                if line[0] not in id_dict:
                    id_dict[line[0]] = line[1].strip('\n')

    f = codecs.open(file_name, 'w', 'utf8')
    for k in range(len(json_data['questions'])):
        idx = json_data['questions'][k]['id']
        for i in range(len(data['queries'])):
            qid = data['queries'][i]['query_id']
            if qid == idx:
                rel_doc = data['queries'][i]['relevant_documents']
                for item in rel_doc:
                    try:
                        f.write('1' + '\t' + id_dict[qid] + '\t' + id_dict[item] + '\n')
                    except:
                        pass
                bm25_retrieved_doc = data['queries'][i]['retrieved_documents']
                for j in range(len(bm25_retrieved_doc)):
                    item = bm25_retrieved_doc[j]
                    if item['is_relevant'] is False:
                        doc_id = item['doc_id']
                        try:
                            f.write('0' + '\t' + id_dict[qid] + '\t' + id_dict[doc_id] + '\n')
                        except:
                            pass
    f.close()


if __name__ == '__main__':
    src_dir = './'
    dst_dir = './'
    input_json_file = 'phaseA_5b_01.json'
    out_relation_file = dst_dir + 'relation_5b_01.txt'
    id_trans_file = src_dir + 'id_trans.txt'
    train_data, train_docs = load_train_data(src_dir)
    json_data = load_json_file(src_dir + 'source_data/' + input_json_file)
    print("begin to generate relation file...")
    generate_relation_file(train_data, out_relation_file, json_data, id_trans_file)
    print("Done...")
