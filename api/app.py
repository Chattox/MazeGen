""" Flask API to generate mazes from a front end """
from flask import Flask
from mazegen.maze import gen_maze

app = Flask(__name__)

@app.route("/")
def get_maze():
    """ Return completed maze from given height and width """
    return gen_maze(15, 15)
