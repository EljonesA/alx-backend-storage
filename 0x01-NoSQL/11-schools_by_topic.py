#!/usr/bin/env python3
""" function that returns the list of school having a specific topic: """


def schools_by_topic(mongo_collection, topic):
    ''' returns schools with specific topics '''
    query = {"topics": topic}
    schools = mongo_collection.find(query)
    return list(schools)
