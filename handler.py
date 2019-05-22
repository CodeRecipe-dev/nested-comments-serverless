import json
import os
import boto3
import simplejson as json
from dynamo_db_controller import DynamoDBController

def get_comments(event, context):
    print("received event: {}".format(json.dumps(event)))
    if "recipe_id" in event["pathParameters"]:
        recipe_id = event["pathParameters"]["recipe_id"]
        ddb = boto3.resource('dynamodb')
        _ddb_controller = DynamoDBController(ddb)
        results = _ddb_controller.get_comments(recipe_id)
        print(results)
        response = {
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "statusCode": 200,
            "body": json.dumps(results)
        }

        return response

def post_comments(event, context):
    print("received event: {}".format(json.dumps(event)))
    request_body = json.loads(event["body"])
    ddb = boto3.resource('dynamodb')
    _ddb_controller = DynamoDBController(ddb)
    if "recipeId" in request_body:
        results = _ddb_controller.add_comment_to_recipe(request_body)
        response = {
            "headers": {
                "Access-Control-Allow-Origin": "*"
            },
            "statusCode": 200,
            "body": json.dumps(results)
        }
        return response