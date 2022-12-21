import logging
import requests
from flask import Flask, jsonify
from flask import request

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


@app.route("/")
def index():
    return "Hello World!"


if __name__ == "__main__":
    app.run()