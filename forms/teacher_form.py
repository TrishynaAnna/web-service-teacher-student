from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField
from wtforms import validators


class TeacherForm(Form):
    id = HiddenField()

    username = StringField("Login: ", [
        validators.DataRequired("Please enter your login."),
        validators.Length(3, 255, "Login should be from 3 to 255 symbols")
    ])

    password = PasswordField("Password: ", [
        validators.DataRequired("Please enter your password."),
        validators.Length(8, 20, "Password should be from 8 to 20 symbols")
    ])

    name = StringField("Name: ", [
        validators.DataRequired("Please enter your name."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])

    surname = StringField("Surname: ", [
        validators.DataRequired("Please enter your surname."),
        validators.Length(3, 100, "Surname should be from 3 to 100 symbols")
    ])

    email = StringField("Email: ", [
        validators.DataRequired("Please enter your email."),
        validators.Email("Wrong email format")
    ])
    # birthday = StringField("Name: ", [
    #     validators.DataRequired("Please enter your name."),
    #     validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    # ])


    subject = StringField("Subject: ", [
        validators.DataRequired("Please enter your favourite subject."),
        validators.Length(3, 50, "Name should be from 3 to 50 symbols")
    ])


    hobby = StringField("Hobby: ", [
        validators.DataRequired("Please enter your hobby."),
        validators.Length(3, 40, "Name should be from 3 to 40 symbols")
    ])


    #   photo =


    position = StringField("Position: ", [
        validators.DataRequired("Please enter your position."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])


    proglanguage = StringField("Proglanguage: ", [
        validators.DataRequired("Please enter your proglanguage."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])


    specialization = StringField("Specialization: ", [
        validators.DataRequired("Please enter your specialization."),
        validators.Length(3, 40, "Name should be from 3 to 40 symbols")
    ])


    title = StringField("Title: ", [
        validators.DataRequired("Please enter your title."),
        validators.Length(3, 150, "Name should be from 3 to 150 symbols")
    ])


    works = StringField("Works: ", [
        validators.DataRequired("Please enter your works."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])

    submit = SubmitField("Save")