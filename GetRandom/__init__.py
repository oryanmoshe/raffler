import logging

import azure.functions as func
import redis
import json
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    r = redis.Redis(
        host=os.environ["REDIS_HOST"],
        port=os.environ["REDIS_PORT"], 
        password=os.environ["REDIS_PASS"])

    random_email = r.srandmember(os.environ['REDIS_SET_NAME']).decode('utf-8')
    return func.HttpResponse(json.dumps({
            "body": json.dumps({
                "winner": random_email
            })
        }), status_code=200, headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "Get, Post, Options"})
