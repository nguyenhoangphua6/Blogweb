from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")                                       # hiển thị trang chủ
@login_required                                             # Bắt buộc Phải đăng nhập đã
def home():
    posts = Post.query.all()                                # hiển thị tất cả bài đăng
    return render_template("home.html", user=current_user, posts=posts)
                                                            # hiển thị trang chủ vs ng dùng hiện tại
                                                            

@views.route("/create-post", methods=['GET', 'POST'])       # phương thức lấy và đăng
@login_required                                             # Bắt buộc Phải đăng nhập đã
def create_post():                                          # tạo bài viết
    if request.method == "POST":                            # nếu phương thức là đăng        
        text = request.form.get('text')                     # Lấy ra nội dung bài đăng bở vào text

        if not text:                                        # Nếu nội dung text là rỗng
            flash('Bài đăng không được để trống', category='error') #In ra bài đăng k đc để trống
        else:
            post = Post(text=text, author=current_user.id)  # bài đăng với text là text, tác giả là người dùng hiện tại
            db.session.add(post)                            # thêm bài đăng vào db
            db.session.commit()                             # lưu db
            flash('Đã tạo bài đăng!', category='success')   # in ra đã tạo bài đăng thành công, với trạng thái màu xanh
            return redirect(url_for('views.home'))          # chuyển tới trang home

    return render_template('create_post.html', user=current_user)
                                                            # Chuyển tới trang tạo bài viết với ng dùng là ng dùng hiện tại


@views.route("/delete-post/<id>")                           # id là id bài viết
@login_required                                             # Bắt buộc Phải đăng nhập đã
def delete_post(id):                                    
    post = Post.query.filter_by(id=id).first()              # lấy bài đăng với id             
    if not post:
        flash("Bài đăng không tồn tại.", category='error')  # nếu bài dăng k có in ra Bài đăng không tồn tại
    else:   
        db.session.delete(post)                             # xóa bài đăng trong db với id
        db.session.commit()                                 # lưu db
        flash('Đã xóa bài đăng.', category='success')       # in ra  đã xóa bài đăng 

    return redirect(url_for('views.home'))                  # trở vè trang chủ


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Không có người dùng với tên người dùng đó đã tồn tại.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts                                      # lấy tất cả bài đăng của user thông qua class user ở models.py
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/create-comment/<post_id>", methods=['POST']) # Tạo bình luận của cái bài đăng có id là post_id
@login_required                                             # Bắt buộc Phải đăng nhập thì mới tạo bình luận được
def create_comment(post_id):                                # Tạo bình luận của cái bài đăng có id là post_id
    text = request.form.get('text')                         # Văn bản bình luận đc lấy ra bằng get 

    if not text:                                            # Nếu văn bản bình luận không có thì in ra Nhận xét không được để trốn.
        flash('Bình luận không được để trống.', category='error') 
    else:                                                   # Nếu ta có văn bản bình luận thì   
        post = Post.query.filter_by(id=post_id)             # Phải đảm bảo bài viết cần bình luận có tồn tại, thông qua post_id
        if post:                                            # Nếu có bài đăng (bài đăng tồn tại)
            comment = Comment(text=text, 
            author=current_user.id, post_id=post_id)        # Tạo 1 bình luận, với text(văn bản bình luận), 
                                                            # current_user.id (tác giả của bình luận), post_id (id của bài viết) 
            db.session.add(comment)                         # Thêm bình luận vào db
            db.session.commit()                             # Lưu dữ liệu của db
        else:                                               # Nếu không có bài đăng ko tồn tại thì in ra Post does not exist.
            flash('Bài đăng không tồn tại.', category='error')

    return redirect(url_for('views.home'))                  # Chuyển tới trang home cho dù là có bình luận hay k có bình luận


@views.route("/delete-comment/<comment_id>")                # Xóa bình luận với đầu vào là id của bình luận
@login_required                                             # Bắt buộc Phải đăng nhập đã
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()# lấy ra bình luận có bình luận id  đầu tiên

    if not comment:
        flash('Bình luận không tồn tại.', category='error')  # kiểm tra có bình luận hay ko, nếu k có thì in ra 
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('Bạn không có quyền xóa nhận xét này.', category='error')
                                                            # nếu không phải là tác giả của bình luận hoặc là tác giả của bài đăng

    else:
        db.session.delete(comment)                          # xóa bình luận trong db
        db.session.commit()                                 # Lưu dữ liệu của db 

    return redirect(url_for('views.home'))                  # Chuyển tới trang home
