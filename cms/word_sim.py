# coding: utf-8
import cms.jp_wordnet as JPWN

"""
類似度計算モジュール
"""

class WordSim(JPWN.JapaneseWordNetCorpusReader):
    def __init__(self):
        JPWN.JapaneseWordNetCorpusReader.__init__(self)

    def similarity(self, a, b):
        "類似度の計算"
        jsyn_a = self.synset(a)
        jsyn_b = self.synset(b)
        if jsyn_a and jsyn_b:
            sim = jsyn_a.path_similarity(jsyn_b)
        else:
            sim = None
        return sim
