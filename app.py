import os  # 경로설정을 위한 패키지
from flask_pymongo import PyMongo
from flask.json import jsonify
from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_url_path='/static')
app.config['MONGO_URI'] = "mongodb://localhost:27017/local"
mongo = PyMongo(app)


@app.route('/detail')
def detail():
    market_db = mongo.db.market
    market = market_db.find_one({"title": request.args.get('title')})

    return render_template('detail.html', market=market)


@app.route('/delete', methods=["post"])
def delete():
    market_db = mongo.db.market
    title = request.form.get('title')
    market = market_db.find_one({"title": title})

    market_db.delete_one({'_id': market['_id']})
    return redirect('/')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/write', methods=["post"])
def write():

    fileinfo = request.files['image']
    filepath = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(filepath, 'static')
    fileinfo.save(os.path.join(filepath, fileinfo.filename))

    market_db = mongo.db.market

    market_db.insert_one({
        "title": request.form.get('title'),
        "region": request.form.get('region'),
        "price": request.form.get('price'),
        "content": request.form.get('content'),
        "image": fileinfo.filename
    })

    return redirect('/')


@app.route('/')
def index():
    market_db = mongo.db.market
    markets = market_db.find()
    return render_template('index.html', markets=markets)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
