from flask import Flask, jsonify, render_template, request
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

global res, soup
soup = ''



@app.route('/')
def index():
    return render_template('search.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    global soup
    get_question = []
    res = requests.get("https://stackoverflow.com/questions")
    soup = BeautifulSoup(res.text, 'html.parser')
    questions = soup.select(".question-summary")
    count = 0
    for que in questions:
        count += 1
        q = que.select_one('.question-hyperlink').getText()
        votes_count = que.select_one('.vote-count-post').get_text()
        views = que.select_one('.views').attrs['title']
        description = que.select_one('.excerpt').getText()
        get_question.append({"id":count,
                            'votes':votes_count,
                            'views':views,
                            'question':q,
                            "description":description})
    # return jsonify({"Result": get_question, "count":1})
    return render_template('search.html', data = get_question, count = 1, questions_fetched=count)


@app.route('/next', methods=['POST', 'GET'])
def nextpage():
    global soup
    get_question = []
    next_questions = soup.select(".question-summary")
    count = 0
    for que in next_questions:
        count += 1
        q = que.select_one('.question-hyperlink').getText()
        votes_count = que.select_one('.vote-count-post').get_text()
        views = que.select_one('.views').attrs['title']
        description = que.select_one('.excerpt').getText()
        get_question.append({"id":count,
                            'votes':votes_count,
                            'views':views,
                            'question':q,
                            "description":description})
    # return jsonify({"Result": get_question, "count":1})
    return render_template('search.html', data = get_question, count = 1, questions_fetched=count)




if __name__ == "__main__":
    app.run(debug=True)