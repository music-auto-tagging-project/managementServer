import requests
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import get_music_tag_list

assert os.environ.get("DB_HOST") is not None, "should register DB account in environment variables."
assert os.environ.get("DB_USER") is not None, "should register DB account in environment variables."
assert os.environ.get("DB_NAME") is not None, "should register DB account in environment variables."
assert os.environ.get("DB_PASSWORD") is not None, "should register DB account in environment variables."

host = os.environ.get("DB_HOST")
user = os.environ.get("DB_USER")
db = os.environ.get("DB_NAME")
password = os.environ.get("DB_PASSWORD")

app = Flask (__name__)
CORS(app)

@app.route('/music/tag/all',methods=["GET"])
def all_tag_list():
    music_tag_list = get_music_tag_list(host,user,db,password) # [(tag_id,music_id,tag_rank),..]
    return jsonify({"musicTagList":music_tag_list})


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)