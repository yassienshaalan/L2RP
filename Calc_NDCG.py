# File Name : score_ranking.py
# Description : computes NDCG score
# Usage : python score_ranking.py  ref_tsv  hyp_tsv
# Creation Date : 20-11-2015
# Last Modified : Sat 21 Nov 2015 09:32:04 PM PST
# Author : Hao Fang

from __future__ import division
import os
import sys
import argparse
import pandas as pd
import numpy as np


def nDCGScoresBased(pred, true, k):
    # pred: predicted rank *score* of the authors
    # - must be non-negative
    # - 0 means non-CEP
    # - the larger rank score, the better
    # true: ground truth log-score of the author
    # - pred and true should be aligned
    # k: number of ground truth CEPs
    assert len(pred) == len(true)
    assert len(true) >= k

    # NOTE(hfang): ignore negative scores
    true = np.array(true)
    true[true < 0] = 0
    assert sum(true > 0) >= k

    # compute ideal DCG
    true_sorted = sorted(true, reverse=True)
    IDCGk = 0
    for r, x in enumerate(true_sorted[:k]):
        IDCGk += x / np.log2(r + 2)

    # compute actual DCG
    pred = np.array(pred)
    m = min(sum(pred != 0), k)
    assert sum(pred < 0) == 0
    temp = pred.argsort()[::-1]
    rank_pred = np.empty(len(pred), int)
    rank_pred[temp] = np.arange(len(pred))
    assert (pred[rank_pred < m] > 0).all()
    predscore_with_rank = sorted(zip(rank_pred, true), key=lambda x: x[0])
    DCGk = 0
    for r, x in predscore_with_rank[:m]:
        DCGk += x / np.log2(r + 2)

    score = DCGk / IDCGk
    return score


def main():
    # NOTE IMPORTANT: When the author has been predicted as a non-CEP, please assign a rank of 0.
    pa = argparse.ArgumentParser(description='score NDCG')
    pa.add_argument('--reverse', '-r', default=False, action='store_true', help='if set, higher rank score means better ranking; otherwise, the lower the better except 0')
    pa.add_argument('ref_tsv', help='ref file')
    pa.add_argument('hypo_tsv', help='hypo file')
    args = pa.parse_args()

    hypo_df = pd.read_csv(args.hypo_tsv, sep='\t', index_col=['post_id', 'author_id'])
    ref_df = pd.read_csv(args.ref_tsv, sep='\t', index_col=['post_id', 'author_id'])

    hypo_df = ref_df.join(hypo_df, how='left')
    if hypo_df.isnull().any().any():
        # missing ref items in hypo
        print >> sys.stderr, hypo_df.ix[hypo_df.isnull().any(axis=1), :]
        exit(1)

    hypo_df.reset_index(drop=False, inplace=True)
    list_ndcg = []
    for post_id, df_for_post in hypo_df.groupby('post_id'):
        k = (df_for_post.author_label == 1).sum()
        if k == 0:
            # skip the post if no CEP predicted
            continue
        df = df_for_post.copy()
        if not args.reverse:
            l = df.rank_score.max() + 1
            assert l >= 0
            mask_pos = (df.rank_score > 0)
            list_rank_score = df.ix[mask_pos, 'rank_score'].apply(lambda x: l - x).tolist()
            df.ix[mask_pos, 'rank_score'] = list_rank_score
        assert (df.rank_score < 0).sum() == 0
        ytrue = np.array(df.logscore.tolist())
        ypred = np.array(df.ix[:, 'rank_score'].tolist())

        list_ndcg.append(nDCGScoresBased(ypred, ytrue, k))

    ndcg = np.array(list_ndcg).mean()
    print ('NDCG:', ndcg)


#if __name__ == '__main__':
 #   main()
