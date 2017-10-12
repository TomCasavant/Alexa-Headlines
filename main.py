from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

import feedparser



app = Flask(__name__)
ask = Ask(app, "/")
articles = 0
current = 0
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
    global current
    current = next(articles)
    msg = current.title
    return question(msg)

@ask.intent('SummarizeIntent')
def summarize():
    global current
    response = current.summary
    return question(response)



@ask.intent("AMAZON.HelpIntent")
def helpme():
     return question("")

if __name__ == '__main__':
	app.run(debug=True)
