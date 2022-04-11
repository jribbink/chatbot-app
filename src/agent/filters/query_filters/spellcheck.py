from filters.query_filter import QueryFilter
import re
import spellchecker


class SpellCheck(QueryFilter):
    def parse(self, query, original_query):
        spell = spellchecker.SpellChecker()
        spell.word_frequency.load_words(["covid"])
        spell.unknown(["COVID", "covid", "coronavirus", "covid-19"])
        wordList = re.findall(r"\w+", query)
        pattern = re.compile(r"(.)\1{2,}")

        correct_query = ""

        for word in wordList:
            word = pattern.sub(r"\1\1", word)
            correct_query += spell.correction(word) + " "

        return correct_query
