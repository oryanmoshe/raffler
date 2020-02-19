import logging

import azure.functions as func
import redis
import json
import os
import re

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    r = redis.Redis(
        host=os.environ["REDIS_HOST"],
        port=os.environ["REDIS_PORT"], 
        password=os.environ["REDIS_PASS"])

    email = req.params.get('email')
    if not email:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            email = req_body.get('email')


    if not EMAIL_REGEX.match(email):
        return func.HttpResponse(
             json.dumps({
                 "error": "invalid email"
             }),
             status_code=400, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "Get, Post, Options"}
        )
    if email:
        r.sadd(os.environ['REDIS_SET_NAME'], email)
        return func.HttpResponse(json.dumps({
            "body": "ok"
        }), status_code=200, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "Get, Post, Options"})
    else:
        return func.HttpResponse(
             "Please pass a email on the query string or in the request body",
             status_code=400, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "Get, Post, Options"}
        )
