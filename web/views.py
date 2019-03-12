"""__author__ = 何志成"""
from flask import Blueprint, render_template

from back.models import Article

web_blue = Blueprint('web', __name__)


@web_blue.route('/index/')
def index():
    articles = Article.query.limit(14).all()
    return render_template('web2/index.html', articles=articles)


@web_blue.route('/info/<int:id>/')
def info(id):
    article = Article.query.get(id)
    return render_template('web/info.html', article=article)


# 笔记
@web_blue.route('/notes/')
def notes():
    return render_template('web2/new.html')


# 关于自己
@web_blue.route('/about_me/')
def about_me():
    return render_template('web2/about.html')


@web_blue.route('/vim/')
def vim():
    return render_template('https://hancc123.github.io/2019/02/20/vim%E7%BC%96%E8%BE%91%E5%99%A8%E4%B9%8B%E7%A5%9E.md/')


# 后端主页
@web_blue.route('home_page')
def home_page2():
    return render_template('back/index.html')

def main():
    pass


if __name__ == '__main__':
    main()
