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

def get_array_window(array, pos):
    if pos >= len(array):
        current = False
    else:
        current = array[pos]
    if pos == 0:
        previous = False
    else:
        previous = array[pos-1]
    if pos + 1 >= len(array):
        next_ = False
    else:
        next_ = array[pos+1]
    return Window(previous, current, next_)

def tag_sentences(joined_sentence, sentence):

    pair = Pair(joined_sentence, sentence)
    pair.joined_sentence.build()
    pair.sentence.build()
    pair.tag_pair()
    return pair.joined_sentence.get_labels()

class Character(object):

    def __init__(self, char, idx):
        self.char = char
        self.idx = idx

class Window(object):

    def __init__(self, previous, current, next_):
        self.previous = previous
        self.current = current
        self.next = next_

class Sentence(object):

    def __init__(self, string):
        self.string = string
        self.forbidden_pos = []
        self.labels = ['' for x in range(len(string)) ]
        self.pointer = 0
        self.chars = []

    def set_forbidden_pos(self, pos):
        self.forbidden_pos = pos
        for item in pos:
            self.labels[item] = 'X'

    def set_label(self, idx, label):
        self.labels[idx] = label

    def get_labels(self):
        return ''.join(self.labels)

    def next(self):
        while True:
            if self.pointer in self.forbidden_pos:
                self.pointer += 1
            else:
                break
        if self.pointer >= len(self.string):
            return False
        else:
            character = self.string[self.pointer]
            character_object = Character(character, self.pointer)
            self.pointer += 1
            return character_object

    def reset(self):
        self.labels = len(self.string) * '.'
        self.pointer = 0
        self.chars = []

    def build(self):
        while True:
            next_char = self.next()
            if next_char:
                self.chars.append(next_char)
            else:
                break


class Pair(object):

    def __init__(self, joined_sentence, sentence):
        self.joined_sentence = Sentence(joined_sentence)
        self.sentence = Sentence(sentence)

        joined_sentence_no_space = joined_sentence.replace(" ", "")
        sentence_no_space = sentence.replace(" ", "")
        i = 0 
        j = 0
        diff = []
        
        while True:
            try:
                if joined_sentence_no_space[i] == sentence_no_space[j]:
                    i += 1
                    j += 1
                else:
                    diff.append(i)
                    i += 1
            except:
                break
        
        counter = 0
        pos = []
        for idx, char in enumerate(joined_sentence):
            if char.isspace():
                continue
            else:
                if counter in diff:
                    pos.append(idx)
                counter += 1
            
        self.joined_sentence.set_forbidden_pos(pos)

    def tag_pair(self):
        joined_sentence_pos = 0
        sentence_pos = 0
        while True:

            chosen_label = 's'

            joined_sentence_char_window = get_array_window(self.joined_sentence.chars, joined_sentence_pos)
            sentence_char_window = get_array_window(self.sentence.chars, sentence_pos)
            
            if not joined_sentence_char_window.current or not sentence_char_window.current:
                break

            if joined_sentence_char_window.current.char != sentence_char_window.current.char:
                sentence_pos += 1
                continue

            if not sentence_char_window.current.char.isalnum():
                self.joined_sentence.set_label(joined_sentence_char_window.current.idx, chosen_label)
                sentence_pos += 1
                joined_sentence_pos += 1
                continue
            
            if sentence_char_window.previous and sentence_char_window.next:
                if not sentence_char_window.previous.char.isalnum() and sentence_char_window.next.char.isalnum():
                    chosen_label = 'b'
                elif sentence_char_window.previous.char.isalnum() and sentence_char_window.next.char.isalnum():
                    chosen_label = 'm'
                elif sentence_char_window.previous.char.isalnum() and not sentence_char_window.next.char.isalnum():
                    chosen_label = 'e'
                elif not sentence_char_window.previous.char.isalnum() and not sentence_char_window.next.char.isalnum():
                    chosen_label = 's'
            elif not sentence_char_window.previous and sentence_char_window.next:
                if sentence_char_window.next.char.isalnum():
                    chosen_label = 'b'
                else:
                    chosen_label = 's'
            elif sentence_char_window.previous and not sentence_char_window.next:
                if sentence_char_window.previous.char.isalnum():
                    chosen_label = 'e'
                else:
                    chosen_label = 's'
            elif not sentence_char_window.previous and not sentence_char_window.next:
                chosen_label = 's'

            self.joined_sentence.set_label(joined_sentence_char_window.current.idx, chosen_label)

            sentence_pos += 1
            joined_sentence_pos += 1


if __name__ == '__main__':
    filenames = {
        'train': './oracle/loyola_train.csv',
        'test': './oracle/loyola_test.csv',
        'dev': './oracle/loyola_dev.csv'
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
