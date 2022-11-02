from operator import le
from flask import Blueprint, render_template, session, request
from markdown import markdown
from bson.objectid import ObjectId

main = Blueprint('main', __name__)

from ..extensions import mongo
qna_database = mongo.db.QnA

@main.route("/")
def HomePage():
    return render_template('Home/about.html', name='about')


@main.route("/xhrreq", methods=['POST',"GET"])
def xhrreq():
    if request.method == "POST":
        text = request.get_data()
        return markdown(text.decode())

@main.route("/xhrincrement/que/<que_id>")
def xhrincrement(que_id):
    que = qna_database.find_one({'_id': ObjectId(que_id)})
    like = que['like']
    if session['username'] not in like:
        que['like'].append(session['username'])
        qna_database.update_one({'_id': ObjectId(que_id)}, {'$set': {'like': que['like']}})
        return str(len(que['like']))
    else:
        return str('-1')


@main.route("/xhrincrement/comment/<id>")
def xhrincrement_(id):
    ans = qna_database.find_one({"comments._id": ObjectId(id)})
    comments = ans['comments']
    for comment in comments:
        if comment['_id'] == ObjectId(id):
            if session['username'] not in comment['like']:
                comment['like'].append(session['username'])
                break
            else:
                return str(-1)
    qna_database.update_one({"comments._id": ObjectId(id)}, {'$set': {"comments":comments}})
    return str(len(comment['like']))