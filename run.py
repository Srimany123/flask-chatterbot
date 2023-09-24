#!/usr/env/bin python
from chatterbot import ChatBot
#from gtts import gTTS
#from playsound import playsound
import os
language='en'
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from chatterbot.utils import get_response_time as grt
from flask import Flask, render_template, request
#from chatterbot.comparisons import LevenshteinDistance
import spacy

app = Flask(__name__)

'''def LevenshteinDistance(s1,s2):
    n=spacy.load("en_core_web_lg")
    n1=n(f'\\u{s1}')
    n2=n(f'\\u{s2}')
    return n1.similarity(n2)
print('done')'''
chatbot = ChatBot("supra mk4",
                  
                  #storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  
                  #statement_comparison_function=LevenshteinDistance,
                  
                  preprocessors=[
                      'chatterbot.preprocessors.clean_whitespace'
                    ],
                  
                  logic_adapters=[{
                       'import_path':'chatterbot.logic.SpecificResponseAdapter',
                       'input_text':'clap back',
                       'output_text':'clapping!'
                    },
                    {
                      'import_path':'chatterbot.logic.Mathematicalevalutaion',
                      'import_path':'chatterbot.logic.TimeLogicAdapter',
                      'import_path':'chatterbot.logic.BestMatch',
                      'default_response':'i am sorry i don\'t find any related response.',
                      'maximum_similarity_threshold':0.80
                    }
                ],
                  
                filters=[
                    'filters.get_recent_repeated_responses'
                    ]
        )

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
'''trainer = ListTrainer(chatbot)
trainer.train(["Hi","Hey! Sup?",])
trainer.train(["How is the weather today","its pretty good",])
trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train("chatterbot.corpus.english")'''
exit_conditions = (":q", "quit" "exit")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    query = request.args.get('msg')
    if query in exit_conditions:
        return 'quitted'
    else:
        resp_time=grt(chatbot,statement=f'{query}')
        print(f"{chatbot.get_response(query)}")
        print(f"<response time: {resp_time:.2f}sec>")
        return str(chatbot.get_response(query))

if __name__ == "__main__":
    app.run()
