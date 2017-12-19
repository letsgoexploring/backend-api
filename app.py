from hashlib import sha256
from collections import OrderedDict

from flask import Flask, abort, jsonify, request, render_template
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix
from werkzeug.contrib.cache import SimpleCache

import models


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app, resources=r'/api/*')

cache = SimpleCache()


def get_cache_key(data):
    values = ['{}:{}'.format(k, v) for k, v in data.items()]
    return sha256(','.join(values).encode('utf-8')).hexdigest()


@app.route('/api/v1/centralized-rbc-with-labor-simulation/')
def centralized_rbc_with_labor_simulation():
    keys = ['alpha', 'beta', 'delta', 'eta', 'phi',
            'rhoa', 'sigma', 'sige', 'A', 'periods']
    # ordered so that the cache key is consistent
    data = OrderedDict()
    # require all the keys
    for k in keys:
        value = request.args.get(k)
        if value is None:
            abort(400)
        if k == 'periods':
            cast = int
        else:
            cast = float

        data[k] = cast(value)

    cache_key = get_cache_key(data)
    result = cache.get(cache_key)
    if result is None:
        result = models.centralized_rbc_with_labor_simulation(data)
        cache.set(cache_key, result, timeout=3600)  # 1 hour

    return jsonify(result)


@app.route('/')
def main():
    return render_template('index.html')


@app.after_request
def add_header(response):
    response.cache_control.max_age = 3600
    response.cache_control.public = True
    return response


if __name__ == '__main__':
    app.run()
