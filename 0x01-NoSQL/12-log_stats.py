#!/usr/bin/env python3
"""Python script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient()
    nginx_collection = client.logs.nginx
    num_docs = nginx_collection.count_documents({})
    print(f'{num_docs} logs')
    print('Methods:')
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    method_get_status_count = nginx_collection.count_documents({"method": "GET",
                                                         "path": "/status"})
    print(f"{method_get_status_count} status check")
