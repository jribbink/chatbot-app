from functools import reduce
from time import sleep
import nltk
from random import randint
from nltk.corpus import wordnet
from neuralnet import NeuralNet


class Agent:
    lastname = False
    pending_responses = []

    def __init__(self, query_filters, response_filters, nltk_dependencies):
        self.neuralnet = NeuralNet()

        print("Downloading nltk dependencies")
        for dependency in nltk_dependencies:
            nltk.download(dependency)

        self.query_filters = list(map(lambda x: x(self), query_filters))
        self.response_filters = list(map(lambda x: x(self), response_filters))

    def query(self, query) -> str:
        if self.pending_responses:
            resp = self.pending_responses[0][1](query)
            self.pending_responses.pop(0)
            if self.pending_responses:
                return self.pending_responses[0][0]
            return resp

        query = reduce(
            lambda acc, x: x.parse(acc, query),
            self.query_filters,
            query,
        )

        resp = self.neuralnet.queryNN(query)
        resp = reduce(
            lambda acc, x: x.parse(acc, resp, query),
            self.response_filters,
            resp,
        )

        if self.pending_responses:
            return self.pending_responses[0][0]

        return resp

    def pos_tag(self, query):
        token = nltk.word_tokenize(query)
        tagged = nltk.pos_tag(token)

        return tagged

    ## self.synonyms(word, pos_tag) returns list of synonyms for inputted word with the pos_tag
    ## has error catching now
    def synonyms(self, word, pos_tag):
        word = word.lower()
        try:
            synonyms = set()
            synonyms.add(word)
            valid_sets = [
                s
                for s in wordnet.synsets(word, pos=pos_tag)
                if s.name().startswith(word)
            ]
            while len(synonyms) < 3 and valid_sets:
                syn_set = valid_sets.pop(0)
                print(syn_set)
                if syn_set.name().startswith(word):
                    for l in syn_set.lemmas():
                        name = l.name().replace("_", " ")
                        synonyms.add(name.lower())

            print(synonyms)

            return synonyms
        except:
            print(
                "Encountered an error; make sure you inputted a valid word to get synonyms."
            )
            return word
