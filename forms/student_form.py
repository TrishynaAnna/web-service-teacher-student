from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, DateField, HiddenField
from wtforms import validators


class StudentForm(Form):
    id = HiddenField()

    username = StringField("Login: ", [
        validators.DataRequired("Please enter your login."),
        validators.Length(3, 20, "Login should be from 3 to 20 symbols")
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
        validators.Length(3, 20, "Surname should be from 3 to 20 symbols")
    ])

    email = StringField("Email: ", [
        validators.DataRequired("Please enter your email."),
        validators.Email("Wrong email format")
    ])
    birthday = StringField("Name: ", [
        validators.DataRequired("Please enter your name."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")

    ])


    subject = StringField("Subject: ", [
        validators.DataRequired("Please enter your favourite subject."),
        validators.Length(3, 50, "Name should be from 3 to 50 symbols")
    ])


    hobby = StringField("Hobby: ", [
        validators.DataRequired("Please enter your hobby."),
        validators.Length(3, 30, "Name should be from 3 to 30 symbols")
    ])


    #   photo =

    group = StringField("Group: ", [
        validators.DataRequired("Please enter your group."),
        validators.Length(5, 6, "Name should be from 5 to 6 symbols")
    ])


    grades = StringField("Grades: ", [
        validators.DataRequired("Please enter your grades."),
        validators.Length(2, 2, "Name should be 2 symbols")
        validators.NumberRange(min(60), max(100))
    ])

    proglanguage = StringField("Proglanguage: ", [
        validators.DataRequired("Please enter your proglanguage."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])


    specialization = StringField("Specialization: ", [
        validators.DataRequired("Please enter your name."),
        validators.Length(3, 20, "Name should be from 3 to 20 symbols")
    ])



    submit = SubmitField("Save")