import json
import os
import collections
import networkx as nx
from boto3.dynamodb.conditions import Key, Attr

class DynamoDBController:
    def __init__(self, ddb):
        self._ddb = ddb
        table_name = os.environ["RECIPE_COMMENTS_TABLE"]
        self._recipes_metadata_table = self._ddb.Table(table_name)

    def get_comments(self, recipe_id):
        response = self._recipes_metadata_table.query(
            KeyConditionExpression=Key('recipeId').eq(recipe_id),
            ScanIndexForward=False
        )
        items = response['Items']
        self._add_child_comments_to_parent_comments(items)
        return items

    def add_comment_to_recipe(self, request_data):
        threadId = self._get_thread_id(request_data)
        item_data = {
            'recipeId': request_data['recipeId'],
            'author': request_data['author'],
            'commentedAt': request_data['commentedAt'],
            'message': request_data['message'],
            'threadId': threadId
        }
        if 'parentId' in request_data:
            item_data['parentId'] = request_data['parentId']
        response = self._recipes_metadata_table.put_item(
           Item=item_data
        )
        return response

    def _add_child_comments_to_parent_comments(self, flat_comments):
        comments_graph = nx.DiGraph()
        roots = set()
        items = flat_comments
        for item in items:
            prereq = int(item["parentId"])
            target = int(item["threadId"])
            if item["parentId"] == -1:
                roots.add(item["parentId"])
            else:
                comments_graph.add_edge(prereq, target, item=item)

        for item in items:
            if item["parentId"] == -1 and comments_graph.has_node(item["threadId"]):
                bfs_edges = list(nx.bfs_edges(comments_graph, item["threadId"]))
                comments_data_n = {}
                i = 0
                parent_item = item
                parent_item["childComments"] = []
                while i < len(bfs_edges):
                  parent = bfs_edges[i][0]
                  child = bfs_edges[i][1]
                  if parent_item["threadId"] == parent:
                    parent_item["childComments"].append(self._get_item(items, child))
                  else:
                    parent_item = self._get_item(items, parent)
                    parent_item["childComments"] = []
                    parent_item["childComments"].append(self._get_item(items, child))
                  i = i + 1            

    def _get_item(self, items, thread_id):
        for item in items:
            if(item["threadId"] == thread_id):
                return item

    def _get_thread_id(self,request_data):
        response = self._recipes_metadata_table.query(
            KeyConditionExpression=Key('recipeId').eq(request_data['recipeId'])
        )
        if response['Count'] == 0:
            threadId = 0
        else:
            threadId = response['Items'][-1]["threadId"] + 1
        return threadId

def main():
    pass

if __name__ == "__main__":
    main()
