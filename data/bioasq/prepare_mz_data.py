#!/usr/bin/env python
# coding: utf-8

from __future__ import  print_function

import os
import sys
import random
random.seed(49999)
import numpy
numpy.random.seed(49999)

sys.path.append('../../matchzoo/inputs/')
sys.path.append('../../matchzoo/utils/')

from preparation import Preparation
from preprocess import Preprocess, NgramUtil


if __name__ == '__main__':
    prepare = Preparation()
    base_dir = './'
    dst_dir = './'
    corpus, rels = prepare.run_with_one_corpus(base_dir + 'original_data.txt', '<<-->>')
    print('total corpus : %d ...' % (len(corpus)))
    print('total relations : %d ...' % (len(rels)))
    prepare.save_corpus(base_dir + 'corpus.txt', corpus)

    '''rel_train, rel_valid, rel_test = prepare.split_train_valid_test(rels, (0.6, 0.2, 0.2))
    prepare.save_relation(base_dir + 'relation_train.txt', rel_train)
    prepare.save_relation(base_dir + 'relation_valid.txt', rel_valid)
    prepare.save_relation(base_dir + 'relation_test.txt', rel_test)
    print('total relation-train : %d ...' % (len(rel_train)))
    print('total relation-valid : %d ...' % (len(rel_valid)))
    print('total relation-test  : %d ...' % (len(rel_test)))
    print('Preparation finished ...')

    print('Preprocess begin ...')
    preprocessor = Preprocess(word_stem_config={'enable': False}, word_filter_config={'min_freq': 2})
    dids, docs = preprocessor.run(dst_dir + 'corpus.txt')
    preprocessor.save_word_dict(dst_dir + 'word_dict.txt', True)
    preprocessor.save_words_stats(dst_dir + 'word_stats.txt', True)

    fout = open(dst_dir + 'corpus_preprocessed.txt', 'w')
    for inum, did in enumerate(dids):
        fout.write('%s %s %s\n' % (did, len(docs[inum]), ' '.join(map(str, docs[inum]))))
    fout.close()
    print('Preprocess finished ...')'''
