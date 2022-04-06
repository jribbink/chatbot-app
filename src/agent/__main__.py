import sys
from plugins.pos_tag import PosTag
from plugins.spellcheck import SpellCheck
from plugins.entity_recognition import EntityRecognition
from plugins.sentiment_analysis import SentimentAnalysis
from agent import Agent
from message_handler import MessageHandler

from ipc.ipc_pipe import IPCPipe

socket_address = sys.argv[1]

plugins = [SpellCheck, PosTag, EntityRecognition, SentimentAnalysis]

nltk_dependencies = ["popular", "vader_lexicon"]

agent = Agent(plugins, nltk_dependencies)
message_handler = MessageHandler(agent)

pipe = IPCPipe(socket_address, message_handler)
