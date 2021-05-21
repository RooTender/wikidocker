import json
from tqdm import tqdm
from collections import Counter
import operator
import decimal

import sklearn.model_selection
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import numpy as np

if __name__ == '__main__':
    file_data_set = {}
    data_set = []
    classes = []

    tokenizer = RegexpTokenizer(r'\w+')
    snowball = SnowballStemmer(language='english')

    with open("../../full_wiki_dump.json", "r", encoding="utf8") as my_file_read:
        file_data_set = json.load(my_file_read)

    my_file_read.close()

    """ Fill classes. """
    for dict in file_data_set:
        classes.append(dict["category"])

    for dict in tqdm(file_data_set):  # dict includes (category:"", subcategories:[])
        for subcat in dict['subcategories']:  # subcat is dictionary (name:"", articles:[])
            for article in subcat['articles']:  # article is string
                label = dict["category"]
                tokenized_msg = tokenizer.tokenize(article)
                stemmed_msg = [snowball.stem(token) for token in tokenized_msg]
                data_set.append((label, stemmed_msg))

    train_set, test_set = sklearn.model_selection.train_test_split(data_set, train_size=0.8)
    print(f'\nTrain len: {len(train_set)}. Test len: {len(test_set)} \n')

    """ Prepare train dictionaries containing counted words. """
    train_dicts = []
    for _ in range(len(classes)):
        train_dicts.append(Counter([]))

    """ Prepare counter dictionary for every word which occurred in class. """
    train_class_cnts = Counter([])

    """ Train naive Bayes qualifier dictionaries. """
    for i in tqdm(range(len(train_set))):
        for j in range(len(classes)):
            if train_set[i][0] == classes[j]:
                for k in range(len(train_set[i][1])):
                    train_class_cnts[train_set[i][0]] += 1
                    train_dicts[j][train_set[i][1][k]] += 1

                break

    """ Show size categories percentage. """
    # print("\n\n### TRAINING ###")
    # for i in range(len(classes)):
    #     class_size_perc = (train_class_cnts[classes[i]] / sum(train_class_cnts.values())) * 100
    #     print("{:.3f}% of messages was {}.".format(class_size_perc, classes[i].upper()))

    """ ------------------------------------------------------------------------------------------------ """
    alpha_values = [x / 100000.0 for x in range(1, 100, 1)]
    correctness = []
    for alpha in alpha_values:
        print("Alpha value: " + str(alpha))
        """ Prepare qualifier variables. """
        #alpha = 0.1
        test_class_cnts = Counter([])
        corr_ans = 0

        all_words = 0
        for i in range(len(classes)):
            all_words += sum(train_dicts[i].values())

        """ Qualify test messages. """
        for i in range(len(test_set)):
            prob_vector = np.zeros(len(classes))
            for j in range(len(classes)):
                for word in test_set[i][1]:
                    prob_vector[j] += train_dicts[j][word]

                words_number_class = sum(train_dicts[j].values())
                prob_vector[j] += alpha
                prob_vector[j] = prob_vector[j] / (words_number_class + (all_words * alpha))

            max_class_index, prob = max(enumerate(prob_vector), key=operator.itemgetter(1))
            if test_set[i][0] == classes[max_class_index]:
                corr_ans += 1

            test_class_cnts[test_set[i][0]] += 1

        # """ Show size categories percentage. """
        # print("\n### TEST ###")
        # for i in range(len(classes)):
        #     class_size_perc = (test_class_cnts[classes[i]] / sum(test_class_cnts.values())) * 100
        #     print("{:.3f}% of messages was {}.".format(class_size_perc, classes[i].upper()))
        #
        # print("\n### CORRECTNESS ###")
        # print("{:.3f}% of messages was qualified correctly.".format((corr_ans / len(test_set)) * 100))
        correctness.append((corr_ans / len(test_set)) * 100)

    # Find the best alpha.
    max_corr_index, corr = max(enumerate(correctness), key=operator.itemgetter(1))
    print("Maximum correctness: " + str(corr) +"% for alpha: " + str(alpha_values[max_corr_index]))
