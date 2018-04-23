#!/usr/bin/env python
from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)
app.config['MONGO_HOST'] = 'ds149567.mlab.com'
app.config['MONGO_PORT'] = 49567
app.config['MONGO_DBNAME'] = 'adafruite'
# user name and password should use env var instead
app.config['MONGO_USERNAME'] = 'guanqiy'
app.config['MONGO_PASSWORD'] = '2415'

mongo = PyMongo(app)

@app.route('/bestsellers')
def get_best_sellers():
    category = request.args.get('category')
    limit = request.args.get('limit', default=20, type=int)
    max_price = request.args.get('max_price')

    params = {'Availability': 'OUT OF STOCK'}
    if category:
        params['category'] = category
    if max_price:
        params['price'] = {"$lt": max_price}

    cursor = mongo.db.products.find(params).limit(limit)
    products = []
    for product in cursor:
        print(product)
        products.append(product)

    sold_out_num = len(products)
    if sold_out_num < limit:
        params['Availability'] = 'IN STOCK'
        cursor = mongo.db.products.find(params).sort([
            ("Amount", pymongo.ASCENDING)
        ]
        ).limit(limit - sold_out_num)
        for product in cursor:
            print(product)
            products.append(product)

    return jsonify(products)


if __name__ == '__main__':
    app.run(debug=True)