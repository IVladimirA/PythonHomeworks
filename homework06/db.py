from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from scraputils import get_news

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


"""s = session()
pages = get_news("https://news.ycombinator.com/", 35)
for i in range(len(pages)):
    news = News(
        title=pages[i]["title"],
        author=pages[i]["author"],
        comments=pages[i]["comments"],
        points=pages[i]["points"],
        url=pages[i]["url"],
    )
    s.add(news)
s.commit()"""
Base.metadata.create_all(bind=engine)
