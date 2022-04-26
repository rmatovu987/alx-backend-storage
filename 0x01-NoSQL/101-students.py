#!/usr/bin/env python3
"""
Function that returns all students sorted by
their average score.
"""


def top_students(mongo_collection):
    """Returns all students sorted by average score using aggregation."""
    return mongo_collection.aggregate([
        {
            "$project":
                {
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
    ])
