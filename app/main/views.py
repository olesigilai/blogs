from flask_login import login_required, current_user
from flask import render_template,request,redirect,url_for, abort
from ..models import Blogs,Role,User,Comments
from .. import db,photos
from . import main
from ..email import mail_message
from .forms import BlogForm,CommentForm,UpdateProfile

@main.route('/blog/', methods = ['GET','POST'])
@login_required
def new_blog():

    form = BlogForm()

    if form.validate_on_submit():
        category = form.category.data
        blog= form.blog.data
        title=form.title.data

        
        new_pitch = Pitches(title=title,category= category,pitch= pitch,user_id=current_user.id)

        title='New Blog'

        new_blog.save_blog()

        return redirect(url_for('main.index'))

    return render_template('blog.html',form= form)

@main.route('/')
def index():
    '''
    Index page
    return
    '''
    message= "Welcome to Blog Website!!"
    title= 'Blog-web!'
    return render_template('index.html', message=message,title=title)


@main.route('/categories/<cate>')
@login_required
def category(cate):
    '''
    function to return the blogs by category
    '''
    category = Blogs.get_blogs(cate)
    

    title = f'{cate}'
    return render_template('categories.html',title = title, category = category)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(author = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(author = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.author))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(author = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/comments/<id>')
@login_required
def comment(id):
    '''
    function to return the comments
    '''
    comm =Comments.get_comment(id)
    print(comm)
    title = 'comments'
    return render_template('comments.html',comment = comm,title = title)

@main.route('/new_comment/<int:pitches_id>', methods = ['GET', 'POST'])
@login_required
def new_comment(blogs_id):
    blogs = Blogs.query.filter_by(id = blogs_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comments(comment=comment,user_id=current_user.id, pitches_id=pitches_id)

        new_comment.save_comment()

        return redirect(url_for('main.index'))
    title='New Blog'
    return render_template('new_comment.html',title=title,comment_form = form,blogs_id=blogs_id)
