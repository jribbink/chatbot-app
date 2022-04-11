import auto_flush

import sys
from filters.response_filters.google_places import GooglePlaces
from filters.query_filters.spellcheck import SpellCheck
from filters.response_filters.entity_recognition import EntityRecognition
from filters.response_filters.sentiment_analysis import SentimentAnalysis
from agent import Agent
from message_handler import MessageHandler

from ipc.ipc_pipe import IPCPipe


socket_address = sys.argv[1]

front_plugins = [SpellCheck]
back_plugins = [EntityRecognition, SentimentAnalysis, GooglePlaces]

nltk_dependencies = ["popular", "vader_lexicon"]

agent = Agent(front_plugins, back_plugins, nltk_dependencies)
message_handler = MessageHandler(agent)

pipe = IPCPipe(socket_address, message_handler)
