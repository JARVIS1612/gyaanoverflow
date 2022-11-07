from flask import Flask
from flask_pymongo import PyMongo
from .extensions import mongo
from flaskext.markdown import Markdown

def create_app():
    app = Flask(__name__)
    
    # app.config['MONGO_URI'] = "mongodb://localhost:27017/"
    Markdown(app)
    # mongo.init_app(app)
    app.config['ALLOWED_HOSTS'] = ["*"]
    app.config['FLASK_ENV'] = "production"
    app.config['FLASK_RUN_PORT'] = ["*"]
    app.secret_key = 'super secret key'
    print(app.config)
    from GOF.Registration import registration
    from GOF.main import main
    from GOF.Ask_Anything import qna_
    
    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(registration, url_prefix="/registration")
    app.register_blueprint(qna_, url_prefix="/QnA")

    return app
