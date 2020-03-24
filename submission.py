from preprocessing import read_dataframe
import pandas as pd

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

    original = pd.read_csv(options['original'])
    original = pd.merge(original, processed, on='joined_ngram', how='left')
    original = pd.merge(original, results, on='joined_ngram', how='left')
    original = original.drop_duplicates(subset='joined_ngram')
    original.to_csv("results_enwiki_2019_11_30.tsv", sep='\t')