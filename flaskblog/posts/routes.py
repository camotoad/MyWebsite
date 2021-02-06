from flask import Blueprint, url_for, render_template, redirect, request, abort, flash
from flask_login import login_required, current_user
from flaskblog.models import Post
from flaskblog.posts.forms import NewPostForm, UpdatePostForm
from flaskblog import db

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, tags=form.tags.data)
        db.session.add(post)
        db.session.commit()
        flash('Post created', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_post.html', title='Create a new post', form=form, legend='Create a new post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.tags = form.tags.data
        db.session.commit()
        flash('Post has been updated.', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.tags.data = post.tags
    return render_template('new_post.html', title='Update post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route("/categories")
def categories():
    output = []
    for post in Post.query.all():
        split = post.tags.split(',')
        for tag in split:
            if tag and tag not in output:
                output.append(tag)
    return render_template('categories.html', title='Categories', output=output)

@posts.route("/categories/<string:tag>")
def specific_category(tag):
    page = request.args.get('page', 1, type=int)
    post = Post.query.filter(Post.tags.like(f'%{tag}%'))\
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('specific_category.html', title=tag, posts=post)