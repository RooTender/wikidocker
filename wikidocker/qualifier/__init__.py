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
    with open("../../full_wiki_dump.json", "r", encoding="utf8") as my_file_read:
        file_data = json.load(my_file_read)
    my_file_read.close()
    return file_data


def create_sets(file_data_set):
    """Create train and test set of words. Create set of categories"""
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

    train_set, test_set = sklearn.model_selection.train_test_split(data_set, train_size=0.8)
    # print(f'Train len: {len(train_set)}. Test len: {len(test_set)} \n')

    classes = [dict["category"] for dict in file_data_set]

    return classes, train_set, test_set


def train_naive_bayes(train_set, classes):
    """Train naive Bayes qualifier dictionaries"""
    # Prepare train dictionaries containing counted words.
    train_dicts = [Counter([]) for _ in range(len(classes))]

    train_class_cnts = Counter([])

    for i in tqdm(range(len(train_set)), desc='Creating train counter'):
        for j in range(len(classes)):
            if train_set[i][0] == classes[j]:
                for k in range(len(train_set[i][1])):
                    train_class_cnts[train_set[i][0]] += 1
                    train_dicts[j][train_set[i][1][k]] += 1

                break

    serialize_train_dicts(train_dicts, False)

    return train_dicts, train_class_cnts


def serialize_train_dicts(train_dicts, serialize=False):
    if serialize:
        with open("../../train_dicts.json", "w") as file:
            json.dump(train_dicts, file)
        file.close()


def show_categories(stage, classes, data_class_cnts):
    """ Show size categories percentage. """
    print("\n\n### " + stage + " ###")
    for i in range(len(classes)):
        class_size_perc = (data_class_cnts[classes[i]] / sum(data_class_cnts.values())) * 100
        print("{:.3f}% of messages was {}.".format(class_size_perc, classes[i].upper()))


def qualify(article_words, all_words, classes, train_dicts):
    """return class of article"""
    alpha = 0.001
    prob_vector = np.zeros(len(classes))

    for j in range(len(classes)):
        for word in article_words:
            prob_vector[j] += train_dicts[j][word]

        words_number_class = sum(train_dicts[j].values())
        prob_vector[j] += alpha
        prob_vector[j] = prob_vector[j] / (words_number_class + (all_words * alpha))

    max_class_index, _ = max(enumerate(prob_vector), key=operator.itemgetter(1))

    return classes[max_class_index]


def qualify_test_set(test_set, train_dicts, classes):
    """Qualify test set"""

    all_words = sum([sum(train_dicts[i].values()) for i in range(len(classes))])
    test_class_cnts = Counter([])
    corr_ans = 0

    for i in tqdm(range(len(test_set))):

        article_class = qualify(test_set[i][1], all_words, classes)
        if test_set[i][0] == article_class:
            corr_ans += 1
        test_class_cnts[test_set[i][0]] += 1

    return test_class_cnts, corr_ans


def qualify_article(train_dicts, classes):
    """qualifies article - the content of article is scan from console"""
    # """qualifies article - the content of article is in file: 'custom_dump.json'"""
    # with open("../../custom_dump.json", "r", encoding="utf8") as my_file_read:
    #     article = json.load(my_file_read)
    # my_file_read.close()

    article = input("Enter your article: ")

    tokenizer = RegexpTokenizer(r'\w+')
    snowball = SnowballStemmer(language='english')

    tokenized_msg = tokenizer.tokenize(article)
    stemmed_msg = [snowball.stem(token) for token in tokenized_msg]
    data_set = set(stemmed_msg)

    all_words = sum([sum(train_dicts[i].values()) for i in range(len(classes))])

    article_class = qualify(data_set, all_words, classes, train_dicts)

    print('\nArticle was qualified as: ' + article_class)


if __name__ == '__main__':

    file_data_set = read_data()

    classes, train_set, test_set = create_sets(file_data_set)

    train_dicts, train_class_cnts = train_naive_bayes(train_set, classes)

    show_categories('TRAINING', classes, train_class_cnts)

    test_class_cnts, corr_ans = qualify_test_set(test_set, train_dicts, classes)

    show_categories('TEST', classes, test_class_cnts)

    print("\n### CORRECTNESS ###\n{:.3f}% of articles was qualified correctly.".format((corr_ans/len(test_set))*100))

    qualify_article(train_dicts, classes)
