#!/usr/bin/env python3
"""Function to insert new document in collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """Returns the new _id"""
    return mongo_collection.insert_one(kwargs).inserted_id
