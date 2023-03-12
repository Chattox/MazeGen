""" Flask API to generate mazes from a front end """
from flask import Flask, request
from mazegen.maze import gen_maze

app = Flask(__name__)

@app.route("/get-maze", methods=["GET"])
def get_maze():
    """ Return completed maze from given height and width """
    height = int(request.args['height'])
    width = int(request.args['width'])
    return gen_maze(height, width)
