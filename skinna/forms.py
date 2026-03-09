from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class CadastroForm(FlaskForm):

    usuario = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=2, max=30)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    senha1 = PasswordField(
        "Senha",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    senha2 = PasswordField(
        "Confirmar senha",
        validators=[
            DataRequired(),
            EqualTo("senha1")
        ]
    )

    submit = SubmitField("Criar Conta")


class LoginForm(FlaskForm):

    usuario = StringField(
        "Username",
        validators=[DataRequired()]
    )

    senha = PasswordField(
        "Senha",
        validators=[DataRequired()]
    )

    submit = SubmitField("Entrar")