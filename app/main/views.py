from flask_login import login_required, current_user
from flask import render_template,request,redirect,url_for, abort,flash
from ..models import Blogs,Role,User,Comments,Subscriber
from .. import db,photos
from . import main
from ..email import mail_message
from .forms import BlogsForm,CommentForm,UpdateProfile,SubscriberForm
from ..requests import getQuotes

@main.route('/blog/', methods = ['GET','POST'])
@login_required
def new_blog():

    form = BlogsForm()

    if form.validate_on_submit():
        category = form.category.data
        # print("category")
        blog= form.blog.data
        title=form.title.data

        
        new_blog = Blogs(title=title,category= category,blog= blog,user_id=current_user.id)

        title='New Blog'

        new_blog.save_blog()

        return redirect(url_for('main.index'))

    return render_template('blog.html',form= form)

@main.route('/',methods=['GET'])
def index():

    getquotes = getQuotes()
    message= "Welcome to Blog Website!!"
    title= 'Blog-web!'
    return render_template('index.html',getquotes = getquotes,message=message,title=title)


@main.route('/categories')
@login_required
def category():
    '''
    function to return the blogs by category
    '''
    category = Blogs.get_blogs()
  
    

    title = category
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
   
    title = 'comments'
    return render_template('comments.html',comment = comm,title = title)

@main.route('/new_comment/<int:blogs_id>', methods = ['GET', 'POST'])
@login_required
def new_comment( blogs_id):
    
    blogs = Blogs.query.filter_by(id = blogs_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        comment = form.comment.data
        new_comment = Comments(comment=comment,user_id=current_user.id, blogs_id=blogs_id)
        new_comment.save_comment()

        return redirect(url_for('main.category'))
    title='New Blog'
    return render_template('new_comment.html',title=title,comment_form = form,blogs_id=blogs_id)


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteComment(id):
    comment =Comments.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    # flash('comment succesfully deleted')
    return redirect (url_for('main.index'))


@main.route('/deleteblog/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteBlog(id):
    blog = Blogs.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/Subscribe',methods=['GET','POST'])
def subBlog():
    
    form = SubscriberForm()
    if form.validate_on_submit():
        subs = Subscriber(email = form.email.data, username = form.username.data)    
        db.session.add(subs)
        db.session.commit()


        mail_message("You have successfully subscribed to Blog website,Thank for joining us", "email/welcome_subs", subs.email,subs=subs)
    
    return render_template('subscribe.html',subscribe_form=form)
