import json
from tqdm import tqdm
from collections import Counter
import operator
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import numpy as np


class Qualifier:

    def __init__(self):
        self.classes = self.read_data("classes.json")
        self.train_dicts = self.read_data("train_dicts.json")
        self.all_words = sum([sum(self.train_dicts[i].values()) for i in range(len(self.classes))])

    def read_data(self, filename):
        """read json data from file"""
        with open("data_to_qualify/" + filename, "r", encoding="utf8") as file:
            data = json.load(file)
        file.close()
        return data

    def qualify(self, article_words):
        """return class of article"""
        alpha = 0.001
        prob_vector = np.zeros(len(self.classes))

        for j in range(len(self.classes)):
            for word in article_words:
                if word in self.train_dicts[j]:
                    prob_vector[j] += self.train_dicts[j][word]

            words_number_class = sum(self.train_dicts[j].values())
            prob_vector[j] += alpha
            prob_vector[j] = prob_vector[j] / (words_number_class + (self.all_words * alpha))

        max_class_index, _ = max(enumerate(prob_vector), key=operator.itemgetter(1))

        return self.classes[max_class_index]

    def qualify_test_set(self):
        """Qualify test set readed from file"""
        # display proportion of categories in train set
        train_class_cnts = Counter([])
        for i in range(len(self.classes)):
            train_class_cnts[self.classes[i]] = sum(self.train_dicts[i].values())
        #self.show_categories('TRAINING', train_class_cnts)

        test_set = self.read_data("test_set.json")
        test_class_cnts = Counter([])
        corr_ans = 0

        for i in tqdm(range(len(test_set)), desc='Qualifying test set'):
            article_class = self.qualify(test_set[i][1])
            if test_set[i][0] == article_class:
                corr_ans += 1
            test_class_cnts[test_set[i][0]] += 1

        #self.show_categories('TEST', test_class_cnts)

        #print("\n### CORRECTNESS ###\n{:.3f}% of articles was qualified correctly.\n".format(
        #    (corr_ans / len(test_set)) * 100))

    def show_categories(self, stage, data_class_cnts):
        """ Show size categories percentage. """
        print("\n\n### " + stage + " ###")
        for i in range(len(self.classes)):
            class_size_perc = (data_class_cnts[self.classes[i]] / sum(data_class_cnts.values())) * 100
            print("{:.3f}% of messages was {}.".format(class_size_perc, self.classes[i].upper()))

    @staticmethod
    def process_article(article):
        """function tokenizes article and removes ending from the words"""
        tokenizer = RegexpTokenizer(r'\w+')
        snowball = SnowballStemmer(language='english')
        tokenized_article = tokenizer.tokenize(article)
        stemmed_article = [snowball.stem(token) for token in tokenized_article]
        return stemmed_article

    def qualify_article_from_console(self):
        """qualifies article scanned from console"""
        article = input("Enter your article: ")
        data_set = set(self.process_article(article))
        article_class = self.qualify(data_set)
        print('\nArticle was qualified as: ' + article_class)

    def qualify_article_from_file(self, filename):
        """qualifies article readed from file (preprocessed by Crawler)"""
        article = self.read_data(filename)
        data_set = set(self.process_article(article))
        article_class = self.qualify(data_set)
        print('\nArticle was qualified as: ' + article_class)
