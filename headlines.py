import datetime
from flask import Flask, render_template, request, make_response
from utils import get_weather, RSS_FEEDS, DEFAULTS, get_news, get_rates

app = Flask(__name__)


@app.route('/')
def home():
    """
    Get customized headlines, based on user input or defaults
    """
    #: get customized headlines based on user input or default
    publication = get_value_with_fallback('publication')
    articles = get_news(publication)
    #: get customized weather based on user input or default
    city = get_value_with_fallback('city')
    weather = get_weather(city)

    #: get customized currency based on user input or default
    currency_from = get_value_with_fallback('currency_from')
    currency_to = get_value_with_fallback('currency_to')
    rate, currencies = get_rates(currency_from, currency_to)

    #: save cookies and return template
    response = make_response(
            render_template('home.html', 
            articles=articles,
            publication=publication,
            weather=weather, 
            currency_from=currency_from,
            currency_to=currency_to,
            rate=rate,
            currencies=sorted(currencies))
            )
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie('publication', publication, expires=expires)
    response.set_cookie('city', city, expires=expires)
    response.set_cookie('currency_from', currency_from, expires=expires)
    response.set_cookie('currency_to', currency_to, expires=expires)
    return response

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

if __name__ == '__main__':
    app.run(debug=True)
