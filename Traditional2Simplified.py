#!/usr/bin/env python
# -*- coding: utf-8 -*-

from langconv import *


def Traditional2Simplified(sentence):
    '''
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    '''
    sentence = Converter('zh-hans').convert(sentence)
    print(sentence)

def main(argv):
    try:
        for line in sys.stdin:
            line = line.strip()
            Traditional2Simplified(line)
    except Exception:
        pass

if __name__ == "__main__":
    main(sys.argv)
