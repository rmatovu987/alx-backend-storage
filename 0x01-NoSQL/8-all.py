#!/usr/bin/env python3
"""Function that lists all documents in collection"""
from typing import List


def list_All(mongo_collection) -> List:
    """return empty list if no documents"""
    if mongo_collection is not None:
        return mongo_collection.find()
    return []


if __name__ == '__main__':
    from pymongo import MongoClient

    list_all = __import__('8-all').list_all
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {}".format(school.get('_id'), school.get('name')))