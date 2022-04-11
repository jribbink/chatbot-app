import sys
from filters.query_filters.spellcheck import SpellCheck
from filters.response_filters.entity_recognition import EntityRecognition
from filters.response_filters.sentiment_analysis import SentimentAnalysis
from agent import Agent
from message_handler import MessageHandler

from ipc.ipc_pipe import IPCPipe
import auto_flush

socket_address = sys.argv[1]

front_plugins = [SpellCheck]
back_plugins = [EntityRecognition, SentimentAnalysis]

nltk_dependencies = ["popular", "vader_lexicon"]

agent = Agent(front_plugins, back_plugins, nltk_dependencies)
message_handler = MessageHandler(agent)

pipe = IPCPipe(socket_address, message_handler)
