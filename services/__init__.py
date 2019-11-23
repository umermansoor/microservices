import os
import json
from flask import make_response


def root_dir():
    """ Returns root directory for this project """
    return os.path.dirname(os.path.realpath(__file__ + '/..'))


def nice_json(argument):
	""" Formats json data nicely """
    response = make_response(json.dumps(argument, sort_keys = True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response