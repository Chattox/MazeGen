""" Flask API to generate mazes from a front end """
from flask import Flask, request
from flask_cors import CORS, cross_origin
from maze.maze import gen_maze

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/get-maze", methods=["GET"])
@cross_origin()
def get_maze():
    """ Return completed maze from given height and width """
    height = int(request.args['height'])
    width = int(request.args['width'])
    return gen_maze(height, width)
