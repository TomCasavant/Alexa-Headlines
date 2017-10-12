"""An Amazon Alexa skill that retrieves and summarizes news articles from the New York Times"""
from flask import Flask, render_template
from flask_ask import Ask, statement, question

import feedparser


app = Flask(__name__)
ask = Ask(app, "/")
articles = 0
current = 0


@ask.launch
def new_ask():
    """Returns a welcome message when skill is turned on"""
    welcome = render_template('welcome')

    return question(welcome)


@ask.on_session_started
def new_session():
    """When sessions started create a global variable with all New York Times articles"""
    global articles
    articles = article_generator()


def article_generator():
    """Creates a generator that contains all the articles from NYT rss feeds"""
    feed = feedparser.parse(
        'http://rss.nytimes.com/services/xml/rss/nyt/US.xml')
    for article in feed.entries:
        yield article


@ask.intent("GetArticlesIntent")
def get_articles():
    """When asked to get articles, get articles"""
    global articles
    msg = next(articles).title
    return question(msg)


@ask.intent('SummarizeIntent')
def summarize():
    """Gets summary of current article"""
    global articles
    response = articles.current.summary
    return question(response)


@ask.intent("AMAZON.HelpIntent")
def helpme():
    """Returns help commands for Alexa Skill"""
    return question("")


if __name__ == '__main__':
    app.run(debug=True)
