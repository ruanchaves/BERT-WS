from preprocessing import read_dataframe
import pandas as pd
import numpy as np

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
    for i, row in original.iterrows():
        if i % 1000:
            print(i)
        try:
            labels_query = processed[processed['joined_ngram'] == original.at[i, 'joined_ngram']].to_dict('records')[0]['labels']
        except:
            labels_query = ''
        try:    
            prediction_query = results[results['joined_ngram'] == original.at[i, 'joined_ngram']].to_dict('records')[0]['prediction']
        except:
            prediction_query = ''
        original.at[i, 'labels'] = labels_query
        original.at[i, 'prediction'] = prediction_query

    original.to_csv("results_enwiki_2019_11_30.tsv", sep='\t')