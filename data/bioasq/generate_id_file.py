#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
##
# Distributed under terms of the MIT license.

"""
generate bioasq id to MatchZoo id
"""

import pickle
import codecs


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

def generate_id_dict(file_name, dictionary):
    with open(file_name, 'r') as f:
        for line in f:
            if not line:
                break
            line = line.split(' ')
            idx = line[0]
            text = ' '.join(line[1:])
            if text in dictionary:
                print(idx)


def generate_id_file(file_name, data, docs):
    dictionary = {}
    with codecs.open (file_name, 'r', 'utf-8') as f:
        for i in range(len(data['queries'])):
            qid = data['queries'][i]['query_id']
            qtext = data['queries'][i]['query_text']
            if qtext not in dictionary:
                dictionary[qtext] = qid
            rel_doc = data['queries'][i]['relevant_documents']
            for item in rel_doc:
                doc_text = get_doc_by_id(item, docs)
                if doc_text not in dictionary:
                    dictionary[doc_text] = item
            bm25_retrieved_doc = data['queries'][i]['retrieved_documents']
            for j in range(len(bm25_retrieved_doc)):
                item = bm25_retrieved_doc[j]
                if item['is_relevant'] is False:
                    doc_id = item['doc_id']
                    doc_text = get_doc_by_id(doc_id, docs)
                    if doc_text not in dictionary:
                        dictionary[doc_text] = doc_id
    print("dict length: " + str(len(dictionary)))
    return dictionary


if __name__ == '__main__':
    src_dir = './'
    dst_dir = './'
    out_id_file = dst_dir + 'bioasq_id2match_zoo_id.txt'
    match_zoo_file = src_dir + 'corpus.txt'
    train_data, train_docs = load_train_data(src_dir)
    print("begin to build dict...")
    dictionary = generate_id_file(match_zoo_file, train_data, train_docs)
    generate_id_dict(out_id_file, dictionary)
    print("Done...")
