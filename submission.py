from preprocessing import read_dataframe
import pandas as pd
import numpy as np
from pathos.multiprocessing import ProcessingPool as Pool
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class SubmissionGenerator(object):

    def __init__(self, results, processed):
        self.results = results
        self.processed = processed

    def generate(self, original):
        for i, row in original.iterrows():
            if not i % 1000:
                log.info(str(i))
            try:
                labels_query = self.processed[self.processed['joined_ngram'] == original.at[i, 'joined_ngram']].to_dict('records')[0]['labels']
            except:
                labels_query = ''
            try:    
                prediction_query = self.results[self.results['joined_ngram'] == original.at[i, 'joined_ngram']].to_dict('records')[0]['prediction']
            except:
                prediction_query = ''
            original.at[i, 'labels'] = labels_query
            original.at[i, 'prediction'] = prediction_query
        return original


def parallelize_dataframe(df, func, n_cores=16):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

if __name__ == '__main__':
    options = {
        "results" : "results.csv",
        "processed": "./corpora/wiki/en/processed/test.txt",
        "original": "./corpora/wiki/en/original/test_enwiki_2019_11_30.csv"
    }

    results = pd.read_csv(options['results'])
    results = results[['token', 'des_seg']]
    results = results.rename(columns={'token': 'joined_ngram', 'des_seg': 'prediction'})
    results = results.dropna()
    results = results.drop_duplicates(subset='joined_ngram')

    processed = read_dataframe(options['processed'], field1='joined_ngram', field2='labels')
    processed = processed.dropna()

    original = pd.read_csv(options['original'])
    original['labels'] = ''
    original['prediction'] = ''

    submission = SubmissionGenerator(results, processed)

    original = parallelize_dataframe(original, submission.generate)

    original.to_csv("results_enwiki_2019_11_30.tsv", sep='\t')