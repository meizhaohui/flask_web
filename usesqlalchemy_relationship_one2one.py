#!/usr/bin/python3
"""
@Author  : 梅朝辉 Meizhaohui
@Email   : mzh.whut@gmail.com

@Time    : 2018/11/1 23:54
@File    : usesqlalchemy_relationship.py
@Version : 1.0
@Interpreter: Python3.6.2
@Software: PyCharm

@Description:  使用sqlalchemy中的relationship back_populates uselist建立显式双向指向-一对一关系
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import ForeignKey

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
# 假设用户与文章是一对一关系，即一个用户只有一篇文章，一篇文章只对应一个用户
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
    # 一对一关系是在一对多关系的基础上，在一的类中增加uselist=False参数
    article = relationship('Article', back_populates='user', uselist=False)
    # 使用下面这种形式，表示一对多关系
    # article = relationship('Article', back_populates='user')

    def __repr__(self):
        return f"({self.id},{self.username},{self.email},{self.is_active})"


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
    # 每篇文章都有一个作者，每个作者可以有多篇文章
    user_id = Column(Integer, ForeignKey(User.id))
    # 使用backref快速创建双向指向
    # 创建双向指向, 在Article类中创建属性user, 在User类中创建属性article
    user = relationship('User', back_populates='article')
    # 字段is_active,是否激活
    is_active = Column(Boolean, server_default='1')

    def __repr__(self):
        return f"({self.id},{self.title},{self.content},{self.tag},{self.user_id},{self.is_active})"

# 删除所有数据表
Base.metadata.drop_all(engine)
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
# 如果指定用户的文章为list列表则会报错，因为此时是一对一关系，article不能是列表
# user1.article = [ article1, article4]
# 指定各用户的文章
user1.article = article1
user2.article = article2
user3.article = article3
user4.article = article4
session.add_all([user1, user2, user3, user4, user5])
session.commit()
print(article1.user_id)   # output: 1
# 指定用户1的文章是文章4，而原来用户1的文章是文章1，所以更新后会发现原来文章1的user_id为空
user1.article = article4
session.commit()
print(article1.user_id)  # output: None
