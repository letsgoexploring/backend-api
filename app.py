from flask import Flask, abort, jsonify, request
from werkzeug.contrib.fixers import ProxyFix
# from werkzeug.contrib.cache import SimpleCache

from models import get_equilibrium_values


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# TODO add caching
# cache = SimpleCache()


# TODO better URL
@app.route('/api/first-example/', methods=['POST'])
def first_example():
    data = request.get_json()
    if not data:
        abort(400)

    # require all the keys
    keys = ['alpha', 'beta', 'delta', 'rhoa', 'sigma', 'A']
    for k in keys:
        if k not in data:
            abort(400)
        data[k] = float(data[k])

    return jsonify(get_equilibrium_values(data))
