from flask import Flask, jsonify
from constants import RESULT_PATH, SCHOOLS_PATH
from container import parse_manager
from utils import load_from_json, save_data_to_json, remove_excessive_data

# ------------------------------------------------------------------------
app = Flask(__name__)
# ------------------------------------------------------------------------


@app.route('/')
def main_page():
    schools = load_from_json(RESULT_PATH)
    return jsonify(remove_excessive_data(schools))


@app.route('/refresh/')
def refresh_page():
    schools = load_from_json(SCHOOLS_PATH)
    refreshed = parse_manager.parse_all(schools)
    save_data_to_json(refreshed, RESULT_PATH)

    return jsonify(remove_excessive_data(refreshed))


if __name__ == '__main__':
    app.run()