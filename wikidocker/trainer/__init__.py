import json
from tqdm import tqdm
from collections import Counter
import operator

import sklearn.model_selection
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import numpy as np


def read_data():
    """read json data from file"""
    with open("../../wiki_dump.json", "r", encoding="utf8") as my_file_read:
        file_data = json.load(my_file_read)
    my_file_read.close()
    return file_data


def create_sets(file_data_set):
    """Create 3 sets: train, test, categories"""
    data_set = []
    tokenizer = RegexpTokenizer(r'\w+')
    snowball = SnowballStemmer(language='english')

    for dict in tqdm(file_data_set, desc='Creating train and test set'):  # dict includes (category:"", subcategories:[])
        for subcat in dict['subcategories']:  # subcat is dictionary (name:"", articles:[])
            for article in subcat['articles']:  # article is string
                label = dict["category"]
                tokenized_msg = tokenizer.tokenize(article)
                stemmed_msg = [snowball.stem(token) for token in tokenized_msg]
                data_set.append((label, stemmed_msg))

    train_set, test_set = sklearn.model_selection.train_test_split(data_set, train_size=0.99)
    print(f'Train len: {len(train_set)}. Test len: {len(test_set)} \n')

    classes = [dict["category"] for dict in file_data_set]

    return classes, train_set, test_set


def train_naive_bayes(train_set, classes):
    """Train naive Bayes qualifier dictionaries"""
    # Prepare train dictionaries containing counted words.
    train_dicts = [Counter([]) for _ in range(len(classes))]

    train_class_cnts = Counter([])

    for i in tqdm(range(len(train_set)), desc='Creating train dictionaries'):
        for j in range(len(classes)):
            if train_set[i][0] == classes[j]:
                for k in range(len(train_set[i][1])):
                    train_class_cnts[train_set[i][0]] += 1
                    train_dicts[j][train_set[i][1][k]] += 1

                break

    return train_dicts


def serialize_obj(name, obj, serialize=False):
    if serialize:
        with open("../data_to_qualify/" + name + ".json", "w") as file:
            json.dump(obj, file)
        file.close()


if __name__ == '__main__':
    file_data_set = read_data()

    classes, train_set, test_set = create_sets(file_data_set)
    generate_files = True
    serialize_obj('classes', classes, generate_files)
    serialize_obj('test_set', test_set, generate_files)
    train_dicts = train_naive_bayes(train_set, classes)
    serialize_obj('train_dicts', train_dicts, generate_files)

