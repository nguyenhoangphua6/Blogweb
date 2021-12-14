from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()       # tạo 1 biến là db 
DB_NAME = "database.db" # đặt tên


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # đặt đường dẫn đến db của chúng ta
    #CSDL lưu trữ tất cả dữ liệu bao gồm các tài khoản(user)
    db.init_app(app)                

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Post, Comment

    create_database(app)                            # tạo csdl

    login_manager = LoginManager()                  #   thiết lập trình quản lý đăng nhập 
                                                    # đảm bảo rằng sau khi dăng nhập xong khi di chuyển ở các trnag k hỏi tk và mk nữa
                                                    # và họ sẽ k truy cập các trang nhất định khi chưa đăng nhập 
    login_manager.login_view = "auth.login"         # khi ai đó cố gắng 1 trang nhưng chưa đăng nhập thì sẽ chuyển đến trang login
    login_manager.init_app(app)

    @login_manager.user_loader                      #tải người dùng với đầu vào là id
                                                    # tạo phiên ng dùng
    def load_user(id):
        return User.query.get(int(id))              # truy vấn cái id đó ra

    return app                                      # khởi chạy app


def create_database(app):                           # tạo db với app là đầu vào
    if not path.exists("website/" + DB_NAME):       # kiểm tra xem csdl đã tạo chưa, chưa thì sẽ tạo ra nó
        db.create_all(app=app)
        print("Cơ sở dữ liệu đã tạo!")
