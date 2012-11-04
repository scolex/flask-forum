from flask.ext.wtf import (Form, TextField, PasswordField, BooleanField, 
                            RecaptchaField, SubmitField, Required, Email, EqualTo)
from werkzeug import check_password_hash
from users.models import User

class LoginForm(Form):
    email = TextField('email', [Required()])
    password = PasswordField('Password', [Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            email=self.email.data).first()
        if user is None:
            self.email.errors.append('Unknown email')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True


class RegisterForm(Form):
    name = TextField('NickName', [Required()])
    email = TextField('Email address', [Required(), Email()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [
        Required(),
        EqualTo('confirm', message='Passwords must match')
        ])
    accept_tos = BooleanField('I accept the TOS', [Required()])