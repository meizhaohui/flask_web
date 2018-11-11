#!/usr/bin/python3
"""
@Author  : 梅朝辉 Meizhaohui
@Email   : mzh.whut@gmail.com

@Time    : 2018/11/11 22:16
@File    : simple_form.py
@Version : 1.0
@Interpreter: Python3.6.2
@Software: PyCharm

@Description:  使用Flask-WTF构建表单
"""

import os
# 导入Flask类
from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import flash
from flask import redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    # 用户名，不为空
    username = StringField('username', validators=[DataRequired()])
    # 密码，不为空，且长度在8-128位之间
    password = PasswordField('password',
                             validators=[DataRequired(), Length(8, 128)])
    # 是否记住用户
    remember = BooleanField('Remember me')
    # 提交
    submit = SubmitField('Log in')


# 创建类的实例，是一个WSGI应用程序
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['FLASK_DEBUG'] = True


@app.route('/')
def index():
    return render_template('index.html')


#  route()装饰器告诉Flask什么样的URL能触发函数
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        # 获取表单用户名的数据
        username = form.username.data
        # 消息闪显
        flash(f'Welcome home, {username}')
        return redirect(url_for('index'))
    return render_template('simple_form.html', form=form)


if __name__ == '__main__':
    #  run()函数让应用运行在本地服务器上
    app.run(debug=True)
