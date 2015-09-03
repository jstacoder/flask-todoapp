from wtforms import Form,fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class AddTodoForm(Form):
    description = fields.StringField('description')
    category = QuerySelectField('category')
    priority = QuerySelectField('priority')
    submit = fields.SubmitField('Create Todo')
    

