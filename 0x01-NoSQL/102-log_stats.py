#!/usr/bin/env python3
"""  script that provides some stats about Nginx logs stored in MongoDB """

from pymongo import MongoClient


def main():
    ''' Stats from a mongo database and collection '''
    # connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # total number of documents
    total_logs = collection.count_documents({})

    # count for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        method_counts[method] = collection.count_documents({"method": method})

    # Count for method=GET and path=/status
    status_check = collection.count_documents({"method": "GET", "path": "/status"})

    # Print the results
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check} status check")

    # Count occurrences of each IP
    ip_counts = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    # Print top 10 IPs
    print("IPs:")
    for ip in ip_counts:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    main()
