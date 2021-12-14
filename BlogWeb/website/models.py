from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):                        # class user kế thừa từ model và từ usermixin
    id = db.Column(db.Integer, primary_key=True)        # cột id
    email = db.Column(db.String(150), unique=True)      # cột email
    username = db.Column(db.String(150), unique=True)   # cột username
    password = db.Column(db.String(150))                # cột pass
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())    # ngày tạo 
    posts = db.relationship('Post', backref='user', passive_deletes=True)       #Tạo các mối quan hệ 
    comments = db.relationship('Comment', backref='user', passive_deletes=True) #Giữa User-Post và User-Comment
    # dòng này tạo ra một mối quan hệ (relationship) giúp từ người dùng có thể truy cập đến tất cả bài post của user đó
    #backref: tham chiếu ngược. Điều này cho phép rằng thay vì sử dụng author(của Post) để truy cập ID của user
    # (p.user)Điều đó cho phép chúng ta truy cập tất cả các thuộc tính của user(class phía trên) trong khi (p.id) cung cấp 1 số tài nguyên mà k phải chính user thực tế phía trên
    #passive_deletes: cho phép bài post đó đc xóa bởi chính user hiện tại


class Post(db.Model):       
    id = db.Column(db.Integer, primary_key=True)                                # cột id
    text = db.Column(db.Text, nullable=False)                                   # cột văn bản, bắt buộc phải có văn bản, k thể k có văn bản 
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())    # cột ngày giờ, ngày mà văn bản tạo
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)                         # cột tác giả, bắt buộc phải có tác giả, k thể k có tác giả
    comments = db.relationship('Comment', backref='post', passive_deletes=True) #Tạo các mối quan hệ Post-Comment


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)                            # thêm 1 bình luân bằng 1 văn bản (text) với tối đa 200 ký tự
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())    # ngày tạo dòng comment đó
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)                         # tác giả (người dùng) nào viết comment đó
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)                         #id của bài post đó -> đây là khóa ngoại
        # dòng author còn có 1 chức năng là đảm bảo rằng tác giả của bài post đã thực sự tồn tại, chứ k phải là tài khoản ko tồn tại
