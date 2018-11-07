#!/usr/bin/python3
"""
@Author  : 梅朝辉 Meizhaohui
@Email   : mzh.whut@gmail.com

@Time    : 2018/11/1 23:54
@File    : usesqlalchemy_relationship.py
@Version : 1.0
@Interpreter: Python3.6.2
@Software: PyCharm

@Description:  使用sqlalchemy中的relationship back_populates建立显式双向指向-一多对多关系
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
from sqlalchemy import Table

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
# 以文章与标签为例演示多对多关系，多对多关系需要构建关联表
# 一篇文章可以有多个标签，一个标签可以对应多篇文章
article_tag_relation = Table(
    'article__tag',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('article_id', ForeignKey('article.id')),
    Column('tag_id', ForeignKey('tag.id'))
)


class Article(Base):
    # 表名article,文章表
    __tablename__ = 'article'
    # 字段id,主键，默认自增长
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 字段title，标题，最大50位变长字符串，非空
    title = Column(String(50), nullable=False)
    # 字段content，文章内容，长文本
    content = Column(Text)
    # 字段is_active,是否激活
    is_active = Column(Boolean, server_default='1')
    tags = relationship('Tag', secondary=article_tag_relation,
                        back_populates='articles')

    def __repr__(self):
        return f"({self.id}, {self.title}, {self.content}, {self.is_active})"


class Tag(Base):
    # 表名tag，标签表
    __tablename__ = 'tag'
    # 字段id,主键，默认自增长
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 字段username，用户名，最大50位变长字符串，非空
    name = Column(String(50), nullable=False)
    # 字段is_active,是否激活
    is_active = Column(Boolean, default=True)
    articles = relationship('Article', secondary=article_tag_relation,
                            back_populates='tags')

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.is_active})"


# 删除所有数据表
Base.metadata.drop_all(engine)
# 创建数据表
# Base.metadata.create_all(engine)会找到Base的所有子类，并在数据库中建立这些表
Base.metadata.create_all(engine)

# # 向数据表中添加数据
tag1 = Tag(name='Python')
tag2 = Tag(name='Java')
tag3 = Tag(name='C++')
tag4 = Tag(name='Go')
tag5 = Tag(name='Ruby')

# 增加一个标签到session中
session.add(tag1)
# 增加一组用户到session中
session.add_all([tag2, tag3, tag4, tag5])

article1 = Article(title='标题1', content='正文1')
article2 = Article(title='标题2', content='正文2')
article3 = Article(title='标题3', content='正文3')
article4 = Article(title='标题4', content='正文4')
article1.tags = [tag1, tag2]
session.add(article1)
session.commit()
article2.tags = [tag3, tag4]
article3.tags = [tag4, tag1]
article4.tags = [tag5]
# tag1.articles = [article3, article4]
# tag2.articles = [article3, article2]
session.add(article1)
session.add(article2)
session.add(article3)
session.add(article4)
# 提交即保存到数据库中
session.commit()

# 查询文章1的所有标签
article1 = session.query(Article).filter_by(title='标题1').first()
print(hasattr(article1, 'tags'))  # output: True
print(article1.tags)
# output: [(2, Java, True), (1, Python, True)]

# 查询标签Python的所有文章
tag1 = session.query(Tag).filter_by(name='Python').first()
print(hasattr(tag1, 'articles'))  # output: True
print(tag1.articles)
# outout: [(1, 标题1, 正文1, True), (3, 标题3, 正文3, True)]