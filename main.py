from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

import feedparser
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/")
articles = 0
@ask.launch
def new_ask():
	welcome = render_template('welcome')
	
	return question(welcome)

@ask.on_session_started
def new_session():
    global articles
    articles = article_generator()
    
def article_generator():
    feed = feedparser.parse('http://rss.nytimes.com/services/xml/rss/nyt/US.xml')
    for article in feed.entries:
        yield article
        
@ask.intent("GetArticlesIntent")
def get_articles():
    global articles
    msg = next(articles).title
    return question(msg)

@ask.intent('SummarizeIntent')
def summarize();
        

@ask.intent("AMAZON.HelpIntent")
def helpme():
     return question("")

if __name__ == '__main__':
	app.run(debug=True)
