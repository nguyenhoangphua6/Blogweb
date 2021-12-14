from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
#generate_password_hash : tạo băm mật khẩu
#check_password_hash : kiểm tra băm mật khẩu

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():                                                            #Hàm login với 2 phương thức lấy và đăng
    if request.method == 'POST':                                        # yêu cầu phương thức đăng
        email = request.form.get("email")                               # lấy emmal
        password = request.form.get("password")                         # lấy password

        user = User.query.filter_by(email=email).first()                # lấy user với email xem thử có user hay ko
        if user:                                                        # nếu ng dùng tồn tại 
            if check_password_hash(user.password, password):            # kiểm tra pass
                flash("Đăng nhập thành công!", category='success')      # nếu đúng pass thì in ra thông báo đăng nhập thành công
                login_user(user, remember=True)                         # đăng nhập thành công = user và nhớ user ấy
                                                                        # điều này làm cho ta xác định phiên của user
                                                                        # xem là người nào ở trong phiên      
                return redirect(url_for('views.home'))                  # trả về url về home 
            else:
                flash('Mật khẩu không đúng.', category='error')         # nếu sai pass in thông báo mk k đúng
        else:
            flash('Email không tồn tại.', category='error')             # k có user thì in ra thông báo email k tồn tại

    return render_template("login.html", user=current_user)#trả về user hiện tại(đã đn) ở login


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():                                                          # hàm đăng ký 
    if request.method == 'POST':                                        # yêu cầu vs phương thức đăng
        email = request.form.get("email")                               # lấy email
        username = request.form.get("username")                         # lấy username  
        password1 = request.form.get("password1")                       # lấy pass1
        password2 = request.form.get("password2")                       # lấy pass2

        email_exists = User.query.filter_by(email=email).first()        #lấy email trong db
        username_exists = User.query.filter_by(username=username).first()   #lấy user trong db

        if email_exists:
            flash('Email đã được sử dụng.', category='error')           # email tồn tại - in ra thông báo đỏ
        elif username_exists:   
            flash('Tên người dùng đã được sử dụng.', category='error')  # người dùng tồn tại - in ra thông báo đỏ
        elif password1 != password2:
            flash('Mật khẩu không giống nhau!', category='error')       # pass khác - in ra thông báo đỏ
        elif len(username) < 2:
            flash('Tên người dùng quá ngắn.', category='error')         # user nhỏ hơn 2 ký tự - in ra thông báo đỏ
        elif len(password1) < 6:
            flash('Mật khẩu quá ngắn.', category='error')               # pass < 6 ký tự - in ra thông báo đỏ
        elif len(email) < 4:
            flash("Email không hợp lệ.", category='error')              # email < 4 ký tự - in ra thông báo đỏ
        else:                                                           # tạo user mới
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))                            # tạo mật khẩu với bảng băm (hash là bảng băm) và băm theo phương thức sha256
                                                                        # với email là email, user là user name
            db.session.add(new_user)                                    # thêm new user vào db
            db.session.commit()                                         # lưu db
            login_user(new_user, remember=True)                         # đăng nhập thành công = new user và nhớ user ấy
                                                                        # điều này làm cho ta xác định phiên của user
                                                                        # xem là người nào ở trong phiên  
            flash('Người dùng đã tạo!')                                 # thông báo người dùng tạo xong
            return redirect(url_for('views.home'))                      # trả về url home

    return render_template("signup.html", user=current_user) #trả về user hiện tại(đã đn)


@auth.route("/logout")
@login_required                                                         # yêu cầu bắt buộc đăgn nhập
def logout():
    logout_user()                                                       # đăng xuất   
    return redirect(url_for("views.home"))                              #
