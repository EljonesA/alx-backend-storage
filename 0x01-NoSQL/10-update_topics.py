#!/usr/bin/env python3
""" Updating a specific document in a collection """


def update_topics(mongo_collection, name, topics):
    ''' Updates all docs matching filter criteria '''
    result = mongo_collection.update_many(
            {"name": name},  # filter criteria
            {"$set": {"topics": topics}}
    )
    return None
