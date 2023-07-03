from flask import Flask, session, abort

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'

    
    from .views import views
    
    app.register_blueprint(views,url_prefix='/')

    return app