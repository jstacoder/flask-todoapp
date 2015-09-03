from flask import render_template, request, redirect, flash,url_for
from models import Category, Todo, Priority, db
from todoapp import app
from wtforms import Form,fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField

cqf = lambda: Category.query.all()
pqf = lambda: Priority.query.all()
get_label = lambda x: x.name

class AddTodoForm(Form):
    description = fields.StringField('description')
    category = QuerySelectField('category',query_factory=cqf,get_label=get_label)
    priority = QuerySelectField('priority',query_factory=pqf,get_label=get_label)
    submit = fields.SubmitField('Create Todo')



@app.route('/')
def list_all():
    return render_template(
        'list.html',
        categories=Category.query.all(),
        todos=Todo.query.join(Priority).order_by(Priority.value.desc()).all()
    )


@app.route('/<name>')
def list_todos(name):
    category = Category.query.filter_by(name=name).first()
    return render_template(
        'list.html',
        todos=Todo.query.filter_by(category=category).join(Priority).order_by(Priority.value.desc()).all(),
        categories=Category.query.all(),
    )


@app.route('/new-task', methods=['GET', 'POST'])
def new():
    form_args = {}
    if 'cat_name' in request.args:
        form_args = {'category':Category.query.filter(Category.name==request.args['cat_name']).first()}
    form = AddTodoForm(**form_args)
    if request.method == 'POST':
        category = Category.query.filter_by(id=request.form['category']).first()
        priority = Priority.query.filter_by(id=request.form['priority']).first()
        todo = Todo(category=category, priority=priority, description=request.form['description'])
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('list_all'))
    else:
        return render_template(            
            'new-task.html',
            cat_page=len(request.args)>0,
            cat_name=(('cat_name' in request.args) and request.args['cat_name']),
            page='new-task',
            categories=Category.query.all(),
            priorities=Priority.query.all(),
            form=form
        )


@app.route('/<int:todo_id>', methods=['GET', 'POST'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if request.method == 'GET':
        return render_template(
            'new-task.html',
            todo=todo,
            categories=Category.query.all(),
            priorities=Priority.query.all()
        )
    else:
        category = Category.query.filter_by(id=request.form['category']).first()
        priority = Priority.query.filter_by(id=request.form['priority']).first()
        description = request.form['description']
        todo.category = category
        todo.priority = priority
        todo.description = description
        db.session.commit()
        return redirect('/')


@app.route('/new-category', methods=['GET', 'POST'])
def new_category():
    if request.method == 'POST':
        category = Category(name=request.form['category'])
        db.session.add(category)
        db.session.commit()
        return redirect('/')
    else:
        return render_template(
            'new-category.html',
            page='new-category.html')


@app.route('/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get(category_id)
    if request.method == 'GET':
        return render_template(
            'new-category.html',
            category=category
        )
    else:
        category_name = request.form['category']
        category.name = category_name
        db.session.commit()
        return redirect('/')


@app.route('/delete-category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    if request.method == 'POST':
        category = Category.query.get(category_id)
        if not category.todos:
            db.session.delete(category)
            db.session.commit()
        else:
            flash('You have TODOs in that category. Remove them first.')
        return redirect('/')


@app.route('/delete-todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')


@app.route('/mark-done/<int:todo_id>', methods=['POST'])
def mark_done(todo_id):
    if request.method == 'POST':
        todo = Todo.query.get(todo_id)
        todo.is_done = True
        db.session.commit()
        return redirect('/')

