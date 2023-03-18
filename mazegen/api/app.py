""" Flask API to generate mazes from a front end """
from flask import Flask, request
from flask_cors import CORS, cross_origin
from maze.HuntAndKill import HuntAndKill

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/get-maze", methods=["GET"])
@cross_origin()
def get_maze():
    """ Return completed maze from given height and width """
    maze = HuntAndKill(int(request.args['height']), int(request.args['width']))
    maze.generate()
    maze.print_maze()
    return maze.export_maze()
