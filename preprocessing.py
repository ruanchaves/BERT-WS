import pandas as pd
import numpy as np
from multiprocessing import Pool
import csv

def read_table(filename):
    df = pd.read_csv(filename)
    return df[['assembled_sentence', 'sentence']]

def process_table(df):
    df['labels'] = df['assembled_sentence'].astype(str).combine(
        df['sentence'].astype(str), tag_sentences)
    return df[['assembled_sentence', 'labels']]

def parallelize_dataframe(df, func, n_cores=16):
    df_split = np.array_split(df, n_cores)
    pool = Pool(n_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df

def tag_sentences(assembled_sentence, sentence):
    states = ""
    for idx, character in enumerate(sentence):
        current = sentence[idx].isalpha()
        try:
            next_ = sentence[idx+1].isalpha()
        except:
            next_ = False
        if not current:
            states += 's'
            continue
        if idx:
            previous = sentence[idx-1].isalpha()
            if previous and next_:
                states += 'm'
                continue
            elif not previous and next_:
                states += 'b'
                continue
            elif previous and not next_:
                states += 'e'
                continue
            elif not previous and not next_:
                states += 's'
                continue
        else:
            if next_:
                states += 'b'
                continue
            else:
                states += 's'
                continue

    pos = []
    i = 0
    j = 0
    while True:
        try:
            if sentence[i] == assembled_sentence[j]:
                i += 1
                j += 1
            else:
                pos.append(i)
                i += 1
        except:
            break
    final_states = ""
    for idx, item in enumerate(states):
        if idx in pos:
            continue
        final_states += item
    return final_states


filenames = {
    'train': './corpus/train_ptwiki_2019_11_26.csv',
    'test': './corpus/test_ptwiki_2019_11_26.csv',
    'dev': './corpus/dev_ptwiki_2019_11_26.csv'
}

for key in filenames.keys():
    filenames[key] = read_table(filenames[key])
    filenames[key] = parallelize_dataframe(filenames[key], process_table)

for key in filenames.keys():
    filenames[key].to_csv(
        key + '.txt',
        sep='\t',
        index=False,
        header=False,
        quoting=csv.QUOTE_NONE
    )
