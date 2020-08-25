from flask import Flask           # import flask
from flask import request
import json


class game:
    def __init__(self):
        self.board = [[0 for i in range(5)] for i in range(5)]

    def getBoard(self):
        return self.board


app = Flask(__name__)
instane = game()


@app.route("/", methods=['GET'])
def hello():
    return "Hello World!"


@app.route("/board")
def getBoard():
    a = instane.getBoard()
    print(a)
    return json.dumps(a)


@app.route("/team/<int:team_id>", methods=['POST'])
def submitFile(team_id):
    print("Get info from team", team_id)
    if request.method == 'POST':
        print("send from client:", request.form['funny'])
    return "ok"


if __name__ == "__main__":

    app.run()
