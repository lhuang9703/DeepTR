#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright ÃÂÃÂÃÂÃÂ© 2019 lhuang <lhuang9703@gmail.com>
#
# Distributed under terms of the MIT license.

"""
generate bioasq data from original json to MatchZoo data
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


def generate_out_file(file_name, data, docs):
    with codecs.open (file_name, 'w', 'utf-8') as f:
        for i in range(len(data['queries'])):
            qid = data['queries'][i]['query_id']
            qtext = data['queries'][i]['query_text']
            rel_doc = data['queries'][i]['relevant_documents']
            for item in rel_doc:
                doc_text = get_doc_by_id(item, docs)
                if doc_text != '':
                    f.write('1' + '<<-->>' + qid + '<<-->>' + qtext + '<<-->>' + item + '<<-->>' + doc_text + '\n')
            bm25_retrieved_doc = data['queries'][i]['retrieved_documents']
            for j in range(len(bm25_retrieved_doc)):
                item = bm25_retrieved_doc[j]
                if item['is_relevant'] is False:
                    doc_id = item['doc_id']
                    doc_text = get_doc_by_id(doc_id, docs)
                    if doc_text != '':
                        f.write('0' + '<<-->>' + qid + '<<-->>' + qtext + '<<-->>' + doc_id + '<<-->>' + doc_text + '\n')


if __name__ == '__main__':
    src_dir = './'
    dst_dir = './'
    out_file = 'original_data.txt'
    train_data, train_docs = load_train_data(src_dir)
    generate_out_file(out_file, train_data, train_docs)
