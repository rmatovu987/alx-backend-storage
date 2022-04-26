#!/usr/bin/env python3
"""Function that lists all documents in collection"""


def list_All(mongo_collection):
    """return empty list if no documents"""
    if mongo_collection.count() == 0:
        return []
    else:
        return mongo_collection.find()
