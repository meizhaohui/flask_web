#!/usr/bin/python3
"""
@Author  : 梅朝辉 Meizhaohui
@Email   : meizhaohui@jcdz.cc

@Time    : 2018/11/1 23:54
@File    : usesqlalchemy_relationship.py
@Version : 1.0
@Interpreter: Python3.6.2
@Software: PyCharm

@Description:  使用sqlalchemy中的relationship建立双向关系
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
    # 创建双向指向, 在Article类中创建属性user, 在User类中创建属性articles
    # 如果不指定backref，则只有Article类有user属性，User类无articles属性
    user = relationship('User', backref='articles')
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
article1 = Article(title='标题1', content='正文1', tag='Python', user_id=1)
article2 = Article(title='标题2', content='正文2', tag='Java', user_id=1)
article3 = Article(title='标题3', content='正文3', tag='Python', user_id=2)
article4 = Article(title='标题4', content='正文4', tag='Java', user_id=2)
session.add(article1)
session.add_all([article2, article3, article4])
# 提交即保存到数据库中
session.commit()

# 联合查询
# 查询用户名是user1的所有文章
user1 = session.query(User).filter(User.username == 'user1').first()
print(user1)  # output: (1,user1,user1@flask.com,True)
print(hasattr(user1, 'articles')) # output: True
print(user1.articles)
# output: [(1,标题1,正文1,Python,1,True), (2,标题2,正文2,Java,1,True)]

# 查询所有tag是Python的文章的用户名
articles = session.query(Article).filter_by(tag='Python').all()
print(articles)
# output: [(1,标题1,正文1,Python,1,True), (3,标题3,正文3,Python,2,True)]
for article in articles:
    print(hasattr(article, 'user'))
    print(article.user.username)
# output:
# True
# user1
# True
# user2

# 新增数据
user6 = User(username='user6', email='user6@flask.com')
article5 = Article(title='标题5', content='正文5', tag='Python')
print(user6)  # output: (None,user6,user6@flask.com,None)
print(article5)  # output: (None,标题5,正文5,Python,None,None)
article5.user = user6
session.add(article5)
session.flush()
print(user6)  # output: (6,user6,user6@flask.com,True)
print(article5)  # output: (5,标题5,正文5,Python,6,True)
session.commit()
