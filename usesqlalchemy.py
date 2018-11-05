#!/usr/bin/python3
"""
@Author  : 梅朝辉 Meizhaohui
@Email   : meizhaohui@jcdz.cc

@Time    : 2018/11/1 23:54
@File    : usesqlalchemy.py
@Version : 1.0
@Interpreter: Python3.6.2
@Software: PyCharm

@Description:  使用sqlalchemy操作数据库
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy import and_
from sqlalchemy import or_

# create_engine() 会返回一个数据库引擎
engine = create_engine(
    "mysql+pymysql://root:root@localhost:3306/flask?charset=utf8mb4",
    echo=False)
# sessionmaker()会生成一个数据库会话类。这个类的实例可以当成一个数据库连接
# 它同时还记录了一些查询的数据，并决定什么时候执行SQL语句
DBSession = sessionmaker(bind=engine)
# 实例化数据库会话类，建立与数据库的连接
session = DBSession()
# 创建对象的基类,declarative_base()创建一个Base类，这个类的子类可以自动与一个表关联
Base = declarative_base()


# 定义表
class User(Base):
    # 表名user，用户表
    __tablename__ = 'user'
    # 字段id,主键，默认自增长
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 字段username，用户名，最大50位变长字符串，非空
    username = Column(String(50), nullable=False)
    # 字段email，邮箱
    email = Column(String(50))
    # 字段is_active,是否激活，
    is_active = Column(Boolean, default=True)


class Article(Base):
    # 表名article,文章表
    __tablename__ = 'article'
    # 字段id,主键，默认自增长
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 字段title，标题，最大50位变长字符串，非空
    title = Column(String(50), nullable=False)
    # 字段content，文章内容，长文本
    content = Column(Text)
    # 字段tag,文章标签
    tag = Column(String(50))
    # 字段is_active,是否激活
    is_active = Column(Boolean, server_default='1')


# 创建数据表
# Base.metadata.create_all(engine)会找到Base的所有子类，并在数据库中建立这些表
Base.metadata.create_all(engine)

# # 向数据表中添加数据
user1 = User(username='user1', email='user1@flask.com')
user2 = User(username='user2', email='user2@flask.com')
user3 = User(username='user3', email='user3@flask.com')
user4 = User(username='user4', email='user4@flask.com')
user5 = User(username='user5', email='user5@flask.com')
# 增加一个用户到session中
session.add(user1)
# 增加一组用户到session中
session.add_all([user2, user3, user4])
session.add(user5)
article1 = Article(title='标题1', content='正文1', tag='Python')
article2 = Article(title='标题2', content='正文2', tag='Java')
article3 = Article(title='标题3', content='正文3', tag='Python')
article4 = Article(title='标题4', content='正文4', tag='Java')
session.add(article1)
session.add_all([article2, article3, article4])
# 提交即保存到数据库中
session.commit()

# 查询数据库数据
print('EQUAL:')
print(session.query(User).filter(User.username == 'user1').one().username) # equal
print('NOT EQUAL:')
print(session.query(User).filter(User.username != 'user1').all()[0].username) # not equal
print('LIKE:')
print(session.query(User).filter(User.username.like('%2')).one().username) # LIKE
print('IN:')
for user in session.query(User).filter(User.username.in_(['user1', 'user2', 'user3'])).all(): # in
    print(user.id, user.username)
print('NOT IN:')
for user in session.query(User).filter(~User.username.in_(['user1', 'user2', 'user3'])).all(): # not in
    print(user.id, user.username)
print('AND:')
print(session.query(User).filter(User.username.like('user%'), User.id == '2').one().username) # AND
print(session.query(User).filter(and_(User.username.like('user%'), User.id == '2')).one().username) # AND
print(session.query(User).filter(User.username.like('user%')).filter(User.id == '2').one().username) # AND
print('OR:')
for user in session.query(User).filter(or_(User.username.like('user%'), User.id == '3')).all():
    print(user.id, user.username)
print('COUNT QUERY')
print(session.query(User).filter(User.username.like('user%')).count())
print([i.username for i in session.query(User).order_by(User.username.desc()).all()])
print([i.username for i in session.query(User).order_by(User.username.asc()).all()])


# 更新数据表
# 更新一条数据
user1 = session.query(User).filter(User.username == 'user1').first()
print(user1.username, user1.email)
user1.email = user1.username + '@python.org'
session.flush()
print(user1.username, user1.email)
session.commit()
print(user1.username, user1.email)
# 更新多条数据
user4 = session.query(User).filter(User.username == 'user4').first()
user5 = session.query(User).filter(User.username == 'user5').first()
print(user4.username, user4.email)
print(user5.username, user5.email)
# synchronize_session='fetch'在更新操作之前，先发一条sql到数据库中进行查询符合条件的记录
session.query(User).filter(User.id > 3).update(
    {User.email: User.username + '@python.org'}, synchronize_session='fetch')
# flush就是把客户端尚未发送到数据库服务器的SQL语句发送过去，此时数据库未生效，flush之后你才能在这个Session中看到效果
session.flush()
print(user4.username, user4.email)
print(user5.username, user5.email)
# commit就是告诉数据库服务器提交事务，commit之后你才能从其它Session中看到效果，数据库才真正生效
session.commit()
# 查询所有数据
print([(user.id, user.username, user.email, user.is_active) for user in
       session.query(User).all()])
# 删除数据
user5 = session.query(User).filter(User.username == 'user5').first()
# 删除一条数据
session.delete(user5)
session.flush()
session.commit()

# 删除多条数据
session.query(User).filter(User.id > 2).delete(synchronize_session='fetch')
session.flush()
session.commit()
print([(user.id, user.username, user.email, user.is_active) for user in
       session.query(User).all()])

