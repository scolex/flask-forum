from flask.ext.wtf import (Form, TextField, BooleanField, SubmitField, Required)

class CreateCategoryForm(Form):
    title = TextField('Title', [Required()])

class CreateTopicForm(Form):
    title = TextField('Title', [Required()])
    important = BooleanField('Important')
    locked = BooleanField('Locked')

class SendPostForm(Form):
    content = TextField('Content', [Required()])