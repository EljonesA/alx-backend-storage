#!/usr/bin/env python3
'''function that inserts a new document in a collection based on kwargs '''


def insert_school(mongo_collection, **kwargs):
    """
    Inserts new document into the provided MongoDB collection.
    Args:
        mongo_collection: The pymongo collection object.
        **kwargs: Key-value pairs to insert as a new document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
