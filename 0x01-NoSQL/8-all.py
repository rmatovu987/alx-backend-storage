#!/usr/bin/env python3
"""Function that lists all documents in collection"""
from typing import List


def list_all(mongo_collection) -> List:
    """return empty list if no documents"""
    if mongo_collection is not None:
        return mongo_collection.find()
    return []
