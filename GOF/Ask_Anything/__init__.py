from flask import Blueprint,redirect, render_template, request, session, flash
from datetime import datetime
from bson.objectid import ObjectId
import os
from werkzeug.utils import secure_filename

qna_ = Blueprint('qna', __name__)

from ..extensions import mongo
qna_database = mongo.db.QnA

from ..SearchEngine import mini_search

location = "D:\\College\\WebDev\\Fynd\\GyaanOverFlow\\GOF\\static\\files\\"

@qna_.route('/', methods = ['GET', 'POST'])
def ask_anything():
    if not session:
        flash("Please Signin First")
        return redirect('/registration/')
    questions = qna_database.find().sort('time', -1)
    if request.method == "POST":
        query = request.form.get('query')
        ques_id = mini_search(questions, query)
        questions = qna_database.find({'_id': {'$in':ques_id}})
    return render_template('QnA/QnA.html', name="ask_anything", questions=questions)

@qna_.route('/add_que', methods=['GET','POST'])
def add_que():
    if not session:
        flash("Please Signin First")
        return redirect('/registration/')
    if request.method == "POST":
        question = request.form.get('question')
        print('-> ',request.files.getlist('que_file'))
        tags = request.form.get('tags')
        file = request.files.getlist('que_file')
        if len(file[0].filename)!=0:
            file = file[0]
            file.save(os.path.join(os.path.abspath(location),secure_filename(file.filename))) 
            dict_ = {
                "user_id": session['username'],
                "question": (question),
                "tags": tags.split(','),
                "time": datetime.now(),
                "comments": [],
                "like": [],
                "file": secure_filename(file.filename)
            }
        else:
            dict_ = {
                "user_id": session['username'],
                "question": (question),
                "tags": tags.split(','),
                "time": datetime.now(),
                "comments": [],
                "like": [],
                "file" : ""
            }
        print(dict_['file'])
        flash("Question Uploaded !")
        qna_database.insert_one(dict_)
        last = qna_database.find_one({"time":dict_['time'], 'user_id':dict_['user_id']})
        return redirect("/QnA/comment/"+str(last['_id']))
    return render_template('QnA/upload_que.html', name="add_que")

@qna_.route('/add_ans/<id>', methods=["GET", "POST"])
def add_ans(id):
    if not session:
        flash("Please Signin First")
        return redirect('/registration/')
    que = qna_database.find_one({"_id": ObjectId(id)})
    if request.method == "POST":
        ans = request.form.get('comment')
        user = session['username']
        time = datetime.now()
        file = request.files.getlist('ans_file')
        if len(file[0].filename)!=0:
            file = file[0]
            file.save(os.path.join(os.path.abspath(location),secure_filename(file.filename))) 
            dict_ = {
                "_id": ObjectId.from_datetime(datetime.now()),
                "user_id": user,
                "comment": ans,
                "like": [],
                "file": secure_filename(file.filename),
                "time": time
            }
        else:
            dict_ = {
                "_id": ObjectId.from_datetime(datetime.now()),
                "user_id": user,
                "comment": ans,
                "like": [],
                "file": "",
                "time": time
            }
        que['comments'].append(dict_)
        qna_database.update_one({"_id": ObjectId(id)}, {'$set': {"comments":que['comments']}})
        flash("Answer/Comment Uploaded !!")
        return redirect("/QnA/comment/"+id)
    return render_template('QnA/upload_ans.html', name="add_ans", que=que)

@qna_.route('/comment/<que>')
def dispay_comment(que):
    if not session:
        flash("Please Signin First")
        return redirect('/registration/')
    question = qna_database.find_one({'_id': ObjectId(que)})
    return render_template('QnA/display_comments.html', name="ask_anything", que=question)


@qna_.route('/update_que/<que_id>', methods=['GET','POST'])
def update_qna(que_id):
    if not session:
        flash("Please Signin First")
        return redirect('/registration/')
    question = qna_database.find_one({'_id': ObjectId(que_id)})
    if session['username'] != question['user_id']:
        flash('Please SignIn as '+question['user_id'])
        return redirect('/')
    
    if request.method == "POST":
        que = request.form.get('question')
        print('-> ',request.files.getlist('que_file'))
        tags = request.form.get('tags')
        file = request.files.getlist('que_file')
        if len(file[0].filename)!=0:
            file = file[0]
            file.save(os.path.join(os.path.abspath(location),secure_filename(file.filename))) 
            dict_ = {
                "user_id": session['username'],
                "question": que,
                "tags": tags.split(','),
                "time": datetime.now(),
                "comments": [],
                "like": [],
                "file": secure_filename(file.filename)
            }
        else:
            dict_ = {
                "user_id": session['username'],
                "question": que,
                "tags": tags.split(','),
                "time": datetime.now(),
                "comments": [],
                "like": [],
                "file" : question['file']
            }
        qna_database.update_one({'_id':ObjectId(que_id)}, {'$set':dict_})
        flash("updated")
        return redirect('/QnA/comment/'+que_id)
    return render_template('QnA/update_que.html', name="update_que", question=question)

@qna_.route('/update_ans/<ans_id>', methods=['GET','POST'])
def update_ans(ans_id):
    if not session:
        flash("Please Signin First")
        return redirect('/registration/')
    que = qna_database.find_one({"comments._id": ObjectId(ans_id)})
    comments = que['comments']
    for comment in comments:
            if comment['_id'] == ObjectId(ans_id):
                answer = comment
    if request.method == "POST":
        for comment in comments:
            if comment['_id'] == ObjectId(ans_id):
                ans = request.form.get('comment')
                user = session['username']
                time = datetime.now()
                file = request.files.getlist('ans_file')
                if len(file[0].filename)!=0:
                    file = file[0]
                    file.save(os.path.join(os.path.abspath(location),secure_filename(file.filename))) 
                    dict_ = {
                        "_id": ObjectId.from_datetime(datetime.now()),
                        "user_id": user,
                        "comment": ans,
                        "like": [],
                        "file": secure_filename(file.filename),
                        "time": time
                    }
                else:
                    dict_ = {
                        "_id": ObjectId.from_datetime(datetime.now()),
                        "user_id": user,
                        "comment": ans,
                        "like": [],
                        "file": comment['file'],
                        "time": time
                    }
                comments.remove(comment)
                comments.append(dict_)
                break
        qna_database.update_one({"comments._id": ObjectId(ans_id)}, {'$set': {"comments":comments}})
        return redirect('/QnA/comment/'+str(que['_id']))
    return render_template('QnA/update_ans.html', name='update_ans', answer=answer)

@qna_.route('/delete_que/<que_id>')
def delete_que(que_id):
    if not session:
        flash("Please Signin First")
        return redirect('/registration/')
    flash("Successfully deleted the question")
    qna_database.delete_one({'_id': ObjectId(que_id)})
    return redirect('/QnA')
    
@qna_.route('/delete_ans/<ans_id>')
def delete_ans(ans_id):
    if not session:
        flash("Please Signin First")
        return redirect('/registration/')
    que = qna_database.find_one({"comments._id": ObjectId(ans_id)})
    comments = que['comments']
    for comment in comments:
            if comment['_id'] == ObjectId(ans_id):
                comments.remove(comment)
                break
    flash("Successfully removed comment! ")
    qna_database.update_one({"comments._id": ObjectId(ans_id)}, {'$set': {"comments":comments}})
    return redirect('/QnA/comment/'+str(que['_id']))
