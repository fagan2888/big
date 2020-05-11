# coding=utf-8

import argparse
import json
from collections import Counter

def main(path):
    data = json.load(open(path, 'r', encoding='utf-8'))
    max_id = max(max(data['ind_type']['G']), max(data['ind_type']['L']))

    assert max_id + 1 == len(list(Counter(data['ind_type']['G']+data['ind_type']['L']).keys())), '信号id存在重复'
    assert max_id + 1 == len(data['ind_type']['G']) + len(data['ind_type']['L']) - 2, '信号数量不对'

    min_len = 10000000
    max_len = 0
    for item in data['data']:
        seqlen = len(item['open_prices'])
        min_len = min(min_len, seqlen)
        max_len = max(max_len, seqlen)
        assert seqlen == len(item['close_prices']), '长度不一致'
        assert seqlen == len(item['inds']), '长度不一致'
        

        for i in range(seqlen):
            assert item['inds'][i][0] == 0, '不是恒定的False'
            assert item['inds'][i][1] == 1, '不是恒定的True'
            assert max_id + 1 == len(item['inds'][i]), '信号数量不对'
            assert item['close_prices'][i] > 1e-2, '收盘价价格不对 %.2f'%item['close_prices'][i]
            assert item['open_prices'][i] > 1e-2, '开盘价价格不对 %.2f'%item['open_prices'][i]

    assert min_len == max_len
    print('Check success.')


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=None, type=str, required=True)
    args = parser.parse_args()
    main(args.path)