"""__author__ = 何志成"""
from flask import Blueprint, render_template, request, url_for, session
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash

from back.models import User, ArticleType, db, Article
from utils.functions import is_login

back_blue = Blueprint('back', __name__)


@back_blue.route('/index/')
@is_login
def index():
    return render_template('back/index.html')


@back_blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if username and password and password2:
            # 先判断该账号是否被注册过
            user = User.query.filter(User.username == username).first()
            if user:
                # 判断账号已经被注册过
                error = '该账号已注册，请更换账号'
                return render_template('back/register.html', error=error)

            if not password == password2:
                # 两次密码不一致
                error = '两次密码不一致'
                return render_template('back/register.html', error=error)

            user = User()
            user.username = username
            user.password = generate_password_hash(password)
            user.save()
            return redirect(url_for('back.login'))

        else:
            error = '请填写完整的信息'
            return render_template('back/register.html', error=error)


@back_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')
    if request.method == 'POST':
        # 获取数据
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '该账号不存在，请去注册'
                return render_template('back/login.html', error=error)

            if not check_password_hash(user.password, password):
                error = '密码错误请重新输入'
                return render_template('back/login.html', error=error)

            # 账号密码正确，跳转首页
            session['user_id'] = user.id
            return redirect(url_for('back.index'))

        else:
            error = '请填写完整的登录信息'
            return render_template('back/login.html', error=error)


@back_blue.route('/logout/', methods=['GET'])
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))


# 分类页面
@back_blue.route('/a_type/', methods=['GET', 'POST'])
def a_type():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/category_list.html', types=types)


# 添加分类
@back_blue.route('/add_type/', methods=['GET', 'POST'])
def add_type():
    if request.method == 'GET':
        return render_template('back/category_add.html')
    if request.method == 'POST':
        atype = request.form.get('atype')
        if atype:
            # 保存分类信息
            art_type = ArticleType()
            art_type.t_name = atype
            db.session.add(art_type)
            db.session.commit()
            return redirect(url_for('back.a_type'))

        else:
            error = '请填写分类信息'
            return render_template('back/category_add.html', error=error)


# 删除功能
@back_blue.route('/del_type/<int:id>/', methods=['GET', 'POST'])
def del_type(id):
    # 删除分类
    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.a_type'))


# 文章列表
@back_blue.route('/article_list/', methods=['GET', 'POST'])
def article_list():
    articles = Article.query.all()
    return render_template('back/article_list.html', articles=articles)


# 添加文章
@back_blue.route('/article_add/', methods=['GET', 'POST'])
def article_add():
    if request.method == 'GET':
        types = ArticleType.query.all()
        return render_template('back/article_detail.html', types=types)
    if request.method == 'POST':
        title = request.form.get('name')
        desc = request.form.get('desc')
        category = request.form.get('category')
        content = request.form.get('content')
        if title and desc and category and content:
            # 保存输入信息
            art = Article()
            art.title = title
            art.desc = desc
            art.content = content
            # id
            art.type = category
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('back.article_list'))

        else:
            error = '请填写完整的文章信息'
            return render_template('back/article_detail.html', error=error)


@back_blue.route('/the_front_page/')
def the_front_page():
    return render_template('web2/index.html')


def main():
    pass


if __name__ == '__main__':
    main()
