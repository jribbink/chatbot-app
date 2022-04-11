from random import randint
from filters.response_filter import ResponseFilter
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentAnalysis(ResponseFilter):
    def parse(self, current_repsonse, original_response, query):
        sentiment = SentimentIntensityAnalyzer().polarity_scores(query)["compound"]

        if sentiment < -0.5:
            oh_nos = [
                "I'm sorry to hear that! ",
                "That doesn't sound very good. ",
                "I'm sorry you feel this way. ",
                "I hope I can help you feel better! ",
                "Hold on, we'll get you feeling better in no time! ",
                "I'll work my hardest to help you feel better. ",
            ]
            current_repsonse = oh_nos[randint(0, len(oh_nos) - 1)] + current_repsonse

        return current_repsonse
