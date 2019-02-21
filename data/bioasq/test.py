#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Distributed under terms of the MIT license.

"""
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


def get_doc_by_id(doc_id, doc_data):
    """get text from train_docs by doc id"""
    if doc_id in doc_data:
        return doc_data[doc_id]['title'] + doc_data[doc_id]['abstractText']
    else:
        print(doc_id + 'not found')
        return ''


def load_json_data(file_name):
    with open (file_name, 'r') as f:
        data = json.load(f)
    return data


def generate_answer_file(file_name, data, docs, json_data):
    pref = "http://www.ncbi.nlm.nih.gov/pubmed/"
    temp_dict = {}
    for i in range(len(data['queries'])):
        qid = data['queries'][i]['query_id']
        doc_list = []
        bm25_retrieved_doc = data['queries'][i]['retrieved_documents']
        for j in range(len(bm25_retrieved_doc)):
            item = bm25_retrieved_doc[j]
            if item['rank'] in [x for x in range(1, 11)]:
                doc_id = pref + item['doc_id']
                doc_list.append(doc_id)
                print(doc_id)
        temp_dict[qid] = doc_list
        # print(temp_dict)
    for j in range(len(json_data['questions'])):
        qid = json_data['questions'][j]['id']
        try:
            json_data['questions'][j]['documents'] = temp_dict[qid]
        except:
            print(qid + " not fonud!")
    
    with codecs.open(file_name, 'w', 'utf8') as f:
        json.dump(json_data, f, indent=2)


def generate_gold_answer(file_name, data, docs, json_data):
    pref = "http://www.ncbi.nlm.nih.gov/pubmed/"
    temp_dict = {}
    for i in range(len(data['queries'])):
        qid = data['queries'][i]['query_id']
        doc_list = [pref + x for x in data['queries'][i]['relevant_documents']]
        temp_dict[qid] = doc_list
    for j in range(len(json_data['questions'])):
        qid = json_data['questions'][j]['id']
        try:
            json_data['questions'][j]['documents'] = temp_dict[qid]
        except:
            print(qid + " not found!")

    with codecs.open(file_name, 'w', 'utf8') as f:
        json.dump(json_data, f, indent=2)

if __name__ == '__main__':
    src_dir = './'
    dst_dir = './'
    input_file = 'phaseA_5b_01.json'
    out_file = src_dir + 'source_data/' + 'phaseA_5b_01_golden.json'
    train_data, train_docs = load_train_data(src_dir)
    json_data = load_json_data(src_dir + 'source_data/' + input_file)
    generate_gold_answer(out_file, train_data, train_docs, json_data)
