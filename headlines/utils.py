"""
headlines.utils.py
=====================

This module contains helper functions and constants used in the view logic
"""
import urllib
import json
import os
import requests
import feedparser
from flask import request, current_app


WEATHER_URL = ("http://api.openweathermap.org/data/2.5/weather?q={query}&units=metric&appid={id}")
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id={id}"

DEFAULTS = {
        'publication': 'bbc',
        'city': 'Nairobi,KE',
        'currency_from':'KES',
	    'currency_to':'USD'
        }

RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'iol':'http://www.iol.co.za/cmlink/1.640',
             'nyt':'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
             'spiegel':'http://www.spiegel.de/international/index.rss',
             'time':'http://feeds2.feedburner.com/time/topstories',
             'reuters':'http://feeds.reuters.com/reuters/topNews',
             'wsj':'https://feeds.a.dj.com/rss/RSSWorldNews.xml',
             'ft':'https://www.ft.com/?format=rss',
             'truthdig': 'https://www.truthdig.com/rss-2/',
             'mtr': 'https://www.technologyreview.com/topnews.rss',
             'ieee': 'https://spectrum.ieee.org/rss/fulltext',
             'wired':'https://www.wired.com/feed/rss'
            }

def get_weather(query='London,UK'):
    """
    Returns weather information from weather map API

    :param query: search query to be passed to the API call
    :return: A dictionary with weather information
    """
    url = WEATHER_URL.format(query=query, id=current_app.config['API_KEY'])
    weather = {}
    data = download(url)
    try:
        data = data.json()
    except:
        data = {}
    if data.get('weather'):
        weather['description'] =  data['weather'][0]['description']
        weather['temperature'] = data['main']['temp']
        weather['city'] = data['name']
        weather['country'] = data['sys']['country']
    return weather

def get_news(publication):
    """Returns top headlines from given publication.

    :param publication: name of publication from which to obtain headlines
    """
    if not publication or publication.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = publication.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    articles = feed['entries']

    return articles

def download(url):
    """
    Dowloads a url and returns a response object    
    """
    num_retries = 3
    try:
        resp = requests.get(url)
        if resp.status_code >= 400:
            print('Download error:', resp.text)
            data = None
            if num_retries and 500 <= resp.status_code < 600:
                # recursively retry 5xx HTTP errors
                num_retries -= 1
                return download(url)
    except requests.exceptions.RequestException as e:
        print('Download error:', e)
        return 
    return resp

def get_rates(frm, to):
    url = CURRENCY_URL.format(id=current_app.config['APP_ID'])
    all_currency = download(url) 
    try:
        data = all_currency.json()
    except:
        return
    data = data['rates']
    frm_rate = data.get(frm.upper())
    to_rate = data.get(to.upper())
    return to_rate / frm_rate, data.keys()

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


