#!/usr/bin/env python3
"""14. Top students"""


def top_students(mongo_collection):
    """Python function that returns all students sorted by average score"""
    return mongo_collection.aggregate([
        {
            "$unwind": "$topics"
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ])
