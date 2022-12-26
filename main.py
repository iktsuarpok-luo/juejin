import logging
import requests
from flask import Flask, jsonify
from flask import request
import json

app = Flask(__name__)


@app.errorhandler
def msg_error_handler(ex):
    logging.error(ex)
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.response.status_code if isinstance(ex, requests.HTTPError) else 500
    )
    return response

@app.route("/juejin/get", methods=["GET"])
def getUserInfo():
    user_id = request.args.get("user_id");
    url = "https://api.juejin.cn/user_api/v1/user/get?spider=0&user_id={}&not_self=1&need_badge=1".format(
        user_id
    )
    headers={
        "Content-Type": "application/json; charset=utf-8",
    }

    res = requests.get(url, headers=headers)
    response = jsonify(res.json())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/juejin/article_get", methods=["POST"])
def getArticles():
    params = request.form.to_dict()
    url = "https://api.juejin.cn/content_api/v1/article/query_list"
    headers={
        "Content-Type": "application/json; charset=utf-8",
    }

    req_body={
        "cursor": params.get("cursor"),
        "user_id": params.get("user_id"),
        "sort_type": 2
    }
    res = requests.post(url, json=req_body, headers=headers)
    response = jsonify(res.json())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route("/juejin/focus_get", methods=["GET"])
def getFocus():
    args = request.args
    url = "https://api.juejin.cn/user_api/v1/follow/followees?user_id={}&cursor={}&sort_type=2".format(
        args.get('user_id'), args.get('cursor')
    )
    headers={
        "Content-Type": "application/json; charset=utf-8",
    }

    res = requests.get(url, headers=headers)
    response = jsonify(res.json())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/juejin/likes_get", methods=["POST"])
def getLikes():
    params = request.form.to_dict()
    url = "https://api.juejin.cn/interact_api/v1/digg/query_page"
    headers={
        "Content-Type": "application/json; charset=utf-8",
    }

    req_body={
        "cursor": params.get("cursor"),
        "user_id": params.get("user_id"),
        "sort_type": 2,
        "item_type": 2
    }
    res = requests.post(url, json=req_body, headers=headers)
    response = jsonify(res.json())
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/")
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.run(debug = True)