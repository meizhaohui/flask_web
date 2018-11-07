#!/usr/bin/python3
"""
@Author  : 梅朝辉 Meizhaohui
@Email   : mzh.whut@gmail.com

@Time    : 2018/11/1 23:54
@File    : usesqlalchemy.py
@Version : 1.0
@Interpreter: Python3.6.2
@Software: PyCharm

@Description:  使用flask-sqlalchemy操作数据库
"""
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 数据库配置
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/flask?charset=utf8mb4'
# 该配置为True,则每次请求结束都会自动commit数据库的变动
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 不发送警告信息
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 不显示SQL执行语句
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)


# 定义表
class User(db.Model):
    # 表名user，用户表
    __tablename__ = 'user'
    # 字段id,主键，默认自增长
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 字段username，用户名，最大50位变长字符串，非空
    username = db.Column(db.String(50), nullable=False)
    # 字段email，邮箱
    email = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    # 字段is_active,是否激活
    is_active = db.Column(db.Boolean, default=True)
    role = db.relationship('Role', back_populates='users')

    def __repr__(self):
        return f"({self.id}, {self.username}, {self.email}, {self.role_id}, {self.is_active})"


class Role(db.Model):
    # 表名role，角色表
    __tablename__ = 'role'
    # 字段id,主键，默认自增长
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 字段name，角色名称，最大50位变长字符串，非空
    name = db.Column(db.String(50), nullable=False)
    # 字段is_active,是否激活
    is_active = db.Column(db.Boolean, server_default='1')
    users = db.relationship('User', back_populates='role')

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.is_active})"


@app.before_first_request
def setup_app():
    # 删除数据表
    db.drop_all()
    # 新建数据表
    db.create_all()
    # 新建数据行
    user1 = User(username='user1', email='user1@flask.com')
    user2 = User(username='user2', email='user2@flask.com')
    user3 = User(username='user3', email='user3@flask.com')
    user4 = User(username='user4', email='user4@flask.com')
    user5 = User(username='user5', email='user5@flask.com')
    role1 = Role(name='user')
    role2 = Role(name='developer')
    role3 = Role(name='admin')
    role4 = Role(name='noauth')
    # 指定用户与用户角色间的关系
    user1.role = role1
    user2.role = role2
    user3.role = role3
    role4.users = [user4, user5]
    # 向数据库中添加数据
    db.session.add_all([user1, user2, user3, role4])
    # 提交
    db.session.commit()


@app.route('/')
def index():
    # 查询
    # 查询用户信息
    users_before = User.query.all()
    print(users_before)
    # output:
    # [(1, user1, user1@flask.com, 1, True),
    #  (2, user2, user2@flask.com, 2, True),
    #  (3, user3, user3@flask.com, 3, True),
    #  (4, user4, user4@flask.com, 4, True),
    #  (5, user5, user5@flask.com, 4, True)]

    # 查询角色信息
    roles = Role.query.all()
    print(roles)
    # output:
    # [(1, user, True), (2, developer, True),
    #  (3, admin, True), (4, noauth, True)]
    # 查询某一个用户
    user1 = User.query.filter_by(username='user1').first()
    print(user1)  #output: (1, user1, user1@flask.com, 1, True)
    print(user1.username, user1.role)  #output: user1 (1, user, True)
    # 修改数据
    role_admin = Role.query.filter_by(name='admin').first()
    user1.role = role_admin
    # 提交事务
    db.session.commit()
    user1 = User.query.filter_by(username='user1').first()
    print(user1)  # output: (1, user1, user1@flask.com, 3, True)
    print(user1.username, user1.role)  # output: user1 (3, admin, True)
    # 删除数据
    user5 = User.query.filter_by(username='user5').first()
    db.session.delete(user5)
    # 提交事务
    db.session.commit()
    users_after = User.query.all()
    print(users_after)
    # output:
    # [(1, user1, user1 @ flask.com, 3, True),
    #  (2, user2, user2 @ flask.com, 2, True),
    #  (3, user3, user3 @ flask.com, 3, True),
    #  (4, user4, user4 @ flask.com, 4, True)]
    return str(users_before) + '<br><br>' + str(users_after)


if __name__ == '__main__':
    app.run(debug=True)
