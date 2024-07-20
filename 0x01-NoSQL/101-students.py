#!/usr/bin/env python3
""" Python function that returns all students sorted by average score """

from pymongo import MongoClient

def top_students(mongo_collection):
    ''' Returns a list of students sorted by average score '''
    # Aggregate the students with their average scores
    pipeline = [
            {
                "$project": {
                    "name": 1,
                    "averageScore": {
                        "$avg": "$topics.score"
                    }
                }
            },
            {
                "$sort": {
                    "averageScore": -1
                }
            }
    ]

    # Execute the aggregation pipeline
    students = list(mongo_collection.aggregate(pipeline))

    return students
