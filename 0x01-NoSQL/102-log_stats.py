#!/usr/bin/env python3
"""15. Log stats - new version of 12-log_stats.py"""
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
    top_10_ip = nginx_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    print("IPs:")
    for ip in top_10_ip:
        print(f"\t{ip['_id']}: {ip['count']}")
