""" Flask API to generate mazes from a front end """
from flask import Flask, request
from flask_cors import CORS, cross_origin
from maze.maze import Maze

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/get-maze", methods=["GET"])
@cross_origin()
def get_maze():
    """ Return completed maze from given height and width """
    maze = Maze(request.args['height'], request.args['width'], request.args['hasCentralRoom'])
    return maze.gen_maze()
