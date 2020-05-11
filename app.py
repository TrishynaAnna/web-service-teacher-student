from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, current_user, login_required, roles_accepted, RoleMixin, UserMixin, Security
from datetime import datetime

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1998@localhost/diplom'
# db = SQLAlchemy(app)
from forms.student_form import StudentForm
from forms.teacher_form import TeacherForm

app = Flask(__name__)
app.secret_key = 'key'

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1998@localhost/diplom'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lajdaazigpumhb:2c22c122aace9c7e284a54a8b9c5fce77d7b3e25e63b7f6be7d0f2ef93ce1fb0@ec2-174-129-253-27.compute-1.amazonaws.com:5432/df88p4jfspv874'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


student_have_role = db.Table('student_have_role',
                            db.Column("student_id", db.Integer(), db.ForeignKey('orm_student.id')),
                            db.Column("role_id", db.Integer(), db.ForeignKey('orm_role.id'))
                            )
teacher_have_role = db.Table('teacher_have_role',
                            db.Column("teacher_id", db.Integer(), db.ForeignKey('orm_teacher.id')),
                            db.Column("role_id", db.Integer(), db.ForeignKey('orm_role.id'))
                            )

teacher_own_diplomWork = db.Table('teacher_own_diplomWork',
                            db.Column("teacher_id", db.Integer(), db.ForeignKey('orm_teacher.id')),
                            db.Column("diplomWork_id", db.Integer(), db.ForeignKey('orm_diplomWork.diplomWork_id'))
                            )

techer_own_diplomTopic = db.Table('techer_own_diplomTopic',
                            db.Column("teacher_id", db.Integer(), db.ForeignKey('orm_teacher.id')),
                            db.Column("diplomTopic_id", db.Integer(), db.ForeignKey('orm_diplomTopic.diplomTopic_id'))
                            )



class ormStudent(db.Model, UserMixin):
    __tablename__ = 'orm_student'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=True)
    birthday =  db.Column(db.String(20), nullable=False)
    group = db.Column(db.String(20), nullable=False)
    hobby = db.Column(db.String(40), nullable=False)
  # photo = db.Column(db.text, nullable=False)
    grades = db.Column(db.Integer, nullable=False)
    proglanguage = db.Column(db.String(40), nullable=False)
    specialization = db.Column(db.String(40), nullable=False)
    subject = db.Column(db.String(20), nullable=False)

    roles = db.relationship("ormRole", secondary=student_have_role, backref=db.backref('student', lazy='dynamic'))




class ormTeacher(db.Model, UserMixin):
    __tablename__ = 'orm_teacher'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=True)
    birthday =  db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    hobby = db.Column(db.String(40), nullable=False)
  # photo = db.Column(db.text, nullable=False)
    position = db.Column(db.String(20), nullable=False)
    proglanguage = db.Column(db.String(40), nullable=False)
    specialization = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    works = db.Column(db.String(20), nullable=False)


    roles = db.relationship("ormRole", secondary=teacher_have_role, backref=db.backref('teacher', lazy='dynamic'))
    diplomWork = db.relationship("ormdiplomWork", secondary=teacher_own_diplomWork, backref=db.backref('owner', lazy='dynamic'))
    diplomTopic = db.relationship("ormdiplomTopic", secondary=techer_own_diplomTopic, backref=db.backref('teacher', lazy='dynamic'))

class ormRole(db.Model, RoleMixin):
        __tablename__ = 'orm_role'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique=True)


class ormDiplomTopic(db.Model):
    __tablename__ = 'diplomTopic'
    diplomTopic_id = db.Column(db.Integer, primary_key=True)
    diplomTopic_name = db.Column(db.String(300), nullable=False)
    diplomTopic_subject = db.Column(db.String(150), nullable=False)
    diplomTopic_proglanguage = db.Column(db.String(50), nullable=False)
    diplomTopic_teacher = db.Column(db.String(50), nullable=False)

    diplomTopic = db.relationship("ormdiplomTopic", secondary=teacher_owndiplomTopic, backref=db.backref('teacher', lazy='dynamic'))



class ormDiplomWork(db.Model):
    __tablename__ = 'diplomWork'

    diplomWork_id = db.Column(db.Integer, primary_key=True)
    diplomWork_name = db.Column(db.String(300), primary_key=True)
    diplomWork_proglanguage = db.Column(db.String(50), nullable=False)
    diplomWork_subject= db.Column(db.String(100), nullable=False)
    diplomWork_specialization= db.Column(db.Integer, nullable=False)
    diplomWork_teacher= db.Column(db.String(100), nullable=False)
    diplomWork_title = db.Column(db.String(150), nullable=False)


    diplomWork = db.relationship("ormDiplomWork", secondary=teacher_own_diplomWork, backref=db.backref('owner', lazy='dynamic'))






  user_datastore = SQLAlchemyUserDatastore(db,ormTeacher, ormStudent, ormRole)
  security = Security(app, user_datastore)


@app.route('/new', methods=['GET', 'POST'])
def new():
    db.create_all()

    # db.session.delete(student_have_role)
    # db.session.delete(teacher_have_role)
    # db.session.delete(teacher_own_diplomWork)
    # db.session.delete(techer_own_diplomTopic)
    # db.session.flush()
    # db.session.query(ormRole).delete()
    # db.session.query(ormDiplomwork).delete()
    # db.session.query(ormDiplomTopic).delete()
    # db.session.query(ormTeacher).delete()
    # db.session.query(ormStudent).delete()


Dima = user_datastore.create_user(username="Dima",
                                  password="0000",
                                  name="Dima",
                                  surname="Koltsov",
                                  email="dima_2010@ukr.net",
                                  birthday="01.01.1999",
                                  group="KM-63",
                                  hobby="travel",
                                  grades="A",
                                  proglanguage="Python",
                                  specialization="113",
                                  subject="Математика"
                                  )

Vlad = user_datastore.create_user(username="Vlad",
                                  password="0000",
                                  name="Vlad",
                                  surname="Kanevckyi",
                                  email="vladkaneve@gmail.com",
                                  birthday="04.02.1999",
                                  group="KM-63",
                                  hobby="travel",
                                  grades="B",
                                  proglanguage="Python",
                                  specialization="113",
                                  subject="Інформатика"
                                  )

Anna = user_datastore.create_user(username="Anna",
                                  password="0000",
                                  name="Anna",
                                  surname="Trishyna",
                                  email="trish@gmail.com",
                                  birthday="17.12.1998",
                                  group="KM-63",
                                  hobby="travel",
                                  grades="C",
                                  proglanguage="Python, Javascript",
                                  specialization="113",
                                  subject="Математика")


Admin = user_datastore.create_role(name="Admin")

User = user_datastore.create_role(name="User")

Dima.roles.append(User)
Vlad.roles.append(User)
Anna.roles.append(Admin)


Oleg = user_datastore.create_user(teacher_id = '0000000300871028',
                                  teacher_username = 'OlegChertov',
                                  teacher_name = 'Олег',
                                  teacher_lastname = 'Чертов',
                                  teacher_birthday =  '00.00.0000',
                                  teacher_position = 'Завідувач кафедри',
                                  teacher_subject = 'Математика',
                                  teacher_hobby = 'Відпочинок з рідними',
                                  teacher_proglanguage ='Python',
                                  teacher_item ="Підсистема калібрування фінансових моделей із застосуванням автоматичного диференціювання",
                                  teacher_works ="Підсистема калібрування фінансових моделей із застосуванням автоматичного диференціювання",
                                  teacher_specialization ="113")


Julia = user_datastore.create_user(teacher_id= '000000033681552X',                               #id!!!!!!!
                                  teacher_username = 'BaiJulia',
                                  teacher_name = 'Julia',
                                  teacher_lastname = 'Bai',
                                  teacher_birthday =  '00.00.0000',
                                  teacher_position = ' Доцент',
                                  teacher_subject = 'Математика',
                                  teacher_hobby = 'Читати',
                                  teacher_proglanguage ='C++',
                                  teacher_item ='',
                                  teacher_works ='',
                                  teacher_specialization ='')

# Лілія = Teacher(teacher_id= '0000000157504101',
#                  teacher_username = 'LilyVovk',
#                  teacher_name = 'Lily',
#                  teacher_lastname = 'Vovk',
#                  teacher_birthday =  '21.04.1967',
#                  teacher_position = '',
#                  teacher_subject = '',
#                  teacher_hobby = '',
#                  teacher_proglanguage ='',
#                  teacher_item ='',
#                  teacher_works ='',
#                  teacher_specialization ='')



Admin = user_datastore.create_role(name="Admin")

User = user_datastore.create_role(name="User")


Julia.roles.append(User)
Oleg.roles.append(Admin)






db.session.add_all([Dima, Vlad, Anna, Oleg, Julia])

db.session.commit()

@app.route('/')
def index():
    return render_template("index.html")



@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/student', methods=['GET'])
@login_required
@roles_accepted('Admin', 'User')
def person():
    if current_user.has_role('Admin'):
        result = db.session.query(ormStudent).all()
    else:
        result = db.session.query(ormStudent).filter(ormStudent.id == current_user.id).all()

    # result = db.session.query(ormStudent).all()
    return render_template('student.html', persons=result)





@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    form = StudentForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('studentn_form.html', form=form, form_name="New student", action="new_student")
        else:
            new_student = user_datastore.create_user(
                username=form.username.data,
                password=form.password.data,
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data,
                birthday=form.bithday.data,
                group =form.group.data,
                hobby = form.hobby.data,
              # photo = form.photo.data,
                grades = form.grades.data,
                proglanguage = form.proglanguage.data,
                specialization = form.specialization.data,
                subject = form.subject.data)

            role = db.session.query(ormRole).filter(ormRole.name == "User").one()

            new_student.roles.append(role)

            db.session.add(new_student)
            db.session.commit()

            return redirect(url_for('student'))

    return render_template('student_form.html', form=form, form_name="New student", action="new_student")


@app.route('/edit_student', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', "User")
def edit_person():
    form = StudentForm()

    if request.method == 'GET':

        student_login = request.args.get('student_login')
        student = db.session.query(ormStudent).filter(ormStudent.username == student_login).one()

        # fill form and send to user
        form.username.data = student.username
        form.password.data = student.password
        form.name.data = student.name
        form.surname.data = student.surname
        form.email.data = student.email
        form.bithday.data = student.bithday
        form.group.data = student.group
        form.hobby.data = student.hobby
        # form.photo.data = student.photo
        form.grades.data = student.grades
        form.proglanguage.data = student.proglanguage
        form.specialization.data = student.specialization
        form.subject.data = student.subject

        return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")


    else:

        if not form.validate():
            return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")
        else:
            # find user
            student = db.session.query(ormStudent).filter(ormStudent.username == form.username.data).one()

            # update fields from form data
            student.username = form.username.data
            student.password = form.password.data
            student.name = form.name.data
            student.surname = form.surname.data
            student.email = form.email.data
            student.birthday = form.bithday.data
            student.group = form.group.data
            student.hobby = form.hobby.data
            # student.photo = form.photo.data
            student.grades = form.grades.data
            student.proglanguage = form.proglanguage.data
            student.specialization = form.specialization.data
            student.subject = form.subject.data

            db.session.commit()

            return redirect(url_for('student'))


@app.route('/delete_student', methods=['POST'])
@login_required
@roles_accepted('Admin')
def delete_person():
    student_login = request.form['student_login']

    result = db.session.query(ormStudent).filter(ormStudent.username == student_login).one()

    db.session.delete(result)
    db.session.commit()

    return student_login


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')


@app.route('/teacher', methods=['GET'])
@login_required
@roles_accepted('Admin', 'User')
def person():
    if current_user.has_role('Admin'):
        result = db.session.query(ormTeacher).all()
    else:
        result = db.session.query(ormTeacher).filter(ormTeacher.id == current_user.id).all()

    # result = db.session.query(ormPersons).all()
    return render_template('teacher.html', persons=result)


@app.route('/new_teacher', methods=['GET', 'POST'])
def new_teacher():
    form = TeacherForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('teacher_form.html', form=form, form_name="New teacher", action="new_teacher")
        else:
            new_teacher = user_datastore.create_user(
                username=form.username.data,
                password=form.password.data,
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data,
                birthday = form.bithday.data,
                subject = form.subject.data,
                hobby = form.hobby.data,
            #   photo = form.photo.data,
                position = form.position.data,
                proglanguage = form.proglanguage.data,
                specialization = form.specialization.data,
                title = form.title.data,
                works = form.works.data)

            role = db.session.query(ormRole).filter(ormRole.name == "User").one()

            new_teacher.roles.append(role)

            db.session.add(new_teacher)
            db.session.commit()

            return redirect(url_for('teacher'))

    return render_template('teacher_form.html', form=form, form_name="New teacher", action="new_teacher")


@app.route('/edit_teacher', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', "User")
def edit_person():
    form = TeacherForm()

    if request.method == 'GET':

        teacher_login = request.args.get('teacher_login')
        teacher = db.session.query(ormTeacher).filter(ormTeacher.username == teacher_login).one()

        # fill form and send to user
        form.username.data = teacher.username
        form.password.data = teacher.password
        form.name.data = teacher.name
        form.surname.data = teacher.surname
        form.email.data = teacher.email
        form.bithday.data = teacher.birthday
        form.subject.data = teacher.subject
        form.hobby.data = teacher.hobby
        # form.photo.data = teacher.photo
        form.position.data = teacher.position
        form.proglanguage.data = teacher.proglanguage
        form.specialization.data = teacher.specialization
        form.title.data = teacher.title
        form.works.data = teacher.works

        return render_template('teacher_form.html', form=form, form_name="Edit teacher", action="edit_teacher")


    else:

        if not form.validate():
            return render_template('teacher_form.html', form=form, form_name="Edit teacher", action="edit_teacher")
        else:
            # find user
            teacher = db.session.query(ormTeacher).filter(ormTeacher.username == form.username.data).one()

            # update fields from form data
            teacher.username = form.username.data
            teacher.password = form.password.data
            teacher.name = form.name.data
            teacher.surname = form.surname.data
            teacher.email = form.email.data
            teacher.birthday = form.bithday.data
            teacher.subject = form.subject.data
            teacher.hobby = form.hobby.data
            # teacher.photo = form.photo.data
            teacher.position = form.position.data
            teacher.proglanguage = form.proglanguage.data
            teacher.specialization = form.specialization.data
            teacher.title = form.title.data
            teacher.works = form.works.data


            db.session.commit()

            return redirect(url_for('teacher'))


@app.route('/delete_teacher', methods=['POST'])
@login_required
@roles_accepted('Admin')
def delete_teacher():
    teacher_login = request.form['teacher_login']

    result = db.session.query(ormTeacher).filter(ormTeacher.username == teacher_login).one()

    db.session.delete(result)
    db.session.commit()

    return teacher_login

@app.route('/diplomWork', methods=['GET'])
def diplomWork():
    result = db.session.query(ormDiplomWork).all()
    edit_result = []
    viev_result = []
    if current_user.has_role('Admin'):
        edit_result = result
    elif current_user.has_role('User'):
        teacher = db.session.query(ormTeacher).filter(ormTeacher.id == current_user.id).one()
        for i in result:
            if teacher.diplomWork[0] == i:
                edit_result.append(i)
            else:
                viev_result.append(i)
    else:
        viev_result = result
    # result = db.session.query(ormDiplomWork).all()
    return render_template('diplomWork_form.html', groups=edit_result, groups_1=viev_result)


@app.route('/new_diplomWork', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'User')
def new_diplomWork():
    form = DiplomWorkForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('diplomWork_form.html', form=form, form_name="New diplomWork", action="new_diplomWork")
        else:
            new_diplomWork = ormDiplomWork(
                diplomWork_name = form.diplomWork_name.data,
                diplomWork_title = form.diplomWork_title.data,
                diplomWork_proglanguage = form.diplomWork_proglanguage.data,
                diplomWork_subject = form.diplomWork_subject.data,
                diplomWork_specialization = form.diplomWork_specialization.data)

        teacher = db.session.query(ormTeacher).filter(ormTeacher.id == current_user.id).one()

       teacher.diplomWork.append(new_diplomWork)

    db.session.add(teacher)
    db.session.commit()

    return redirect(url_for('diplomWork'))

    return render_template('diplomWork_form.html', form=form, form_name="New diplomWork", action="new_diplomWork")




@app.route('/edit_diplomWork', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', "User")
def edit_diplomWork():
    form = DiplomWorkForm()

    if request.method == 'GET':

        diplomWork_id = request.args.get('diplomWork_id')
        diplomWork = db.session.query(ormDiplomWork).filter(ormDiplomWork.diplomWork_id == diplomWork_id).one()

        # fill form and send to user
        form.diplomWork_id.data = diplomWork.diplomWork_id
        form.diplomWork_name.data = diplomWork.diplomWork_name
        form.diplomWork_title.data = diplomWork.diplomWork_title
        form.diplomWork_proglanguage.data = diplomWork.diplomWork_proglanguage
        form.diplomWork_subject.data = diplomWork.diplomWork_subject
        form.diplomWork_specialization.data = diplomWork.diplomWork_specialization
        form.diplomWork_teacher.data = diplomWork.diplomWork_teacher



        return render_template('diplomWork_form.html', form=form, form_name="Edit diplomWork", action="edit_diplomWork")

    else:

        if not form.validate():
            return render_template('diplomWork_form.html', form=form, form_name="Edit diplomWork", action="edit_diplomWork")
        else:
            # find user
            diplomWork = db.session.query(ormDiplomWork).filter(ormDiplomWork.diplomWork_id == form.diplomWork_id.data).one()

            # update fields from form data
            form.diplomWork_id.data = diplomWork.diplomWork_id
            form.diplomWork_name.data = diplomWork.diplomWork_name
            form.diplomWork_title.data = diplomWork.diplomWork_title
            form.diplomWork_proglanguage.data = diplomWork.diplomWork_proglanguage
            form.diplomWork_subject.data = diplomWork.diplomWork_subject
            form.diplomWork_specialization.data = diplomWork.diplomWork_specialization


            db.session.commit()

            return redirect(url_for('diplomWork'))


@app.route('/delete_diplomWork', methods=['POST'])
@login_required
@roles_accepted('Admin', "User")
def delete_group():
    diplomWork_id = request.form['diplomWork_id']

    result = db.session.query(ormDiplomWork).filter(ormDiplomWork.diplomWork_id == diplomWork_id).one()

    db.session.delete(result)
    db.session.commit()

    return diplomWork_id

@app.route('/diplomTopic', methods=['GET'])
# @login_required
# @roles_accepted('Admin', 'User')
def diplomTopic():
    result = db.session.query(ormDiplomTopic).all()
    edit_result = []
    viev_result = []
    if current_user.has_role('Admin'):
        edit_result = result
    elif current_user.has_role('User'):
        teacher = db.session.query(ormDiplomTopic).filter(ormTeacher.id == current_user.id).one()
        for i in result:
            if person.group[0] == i:
                edit_result.append(i)
            else:
                viev_result.append(i)
    else:
        viev_result = result
    # result = db.session.query(ormDiplomTopic).all()
    return render_template('diplomTopic.html', groups=edit_result, groups_1=viev_result)


@app.route('/new_diplomTopic', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', 'User')
def new_diplomTopic():
    form = DiplomTopicForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('diplomTopic_form.html', form=form, form_name="New diplomTopic", action="new_diplomTopic")
        else:
            new_diplomTopic = ormDiplomTopic(
                diplomTopic_name=form.diplomTopic_name.data,
                diplomTopic_subject=form.diplomTopic_subject.data,
                diplomTopic_proglanguage=form.diplomTopic_proglanguage.data)



            teacher = db.session.query(ormTeacher).filter(ormTeacher.id == current_user.id).one()

            person.group.append(new_diplomTopic)


            db.session.add(teacher)
            db.session.commit()

            return redirect(url_for('diplomTopic'))

    return render_template('diplomTopic_form.html', form=form, form_name="New diplomTopic", action="new_diplomTopic")


@app.route('/edit_diplomTopic', methods=['GET', 'POST'])
@login_required
@roles_accepted('Admin', "User")
def edit_group():
    form = DiplomTopicForm()

    if request.method == 'GET':

        diplomTopic_id = request.args.get('diplomTopic_id')
        diplomTopic = db.session.query(ormDiplomTopic).filter(ormDiplomTopic.diplomTopic_id == diplomTopic_id).one()

        # fill form and send to user
        form.diplomTopic_id.data = diplomTopic.diplomTopic_id
        form.diplomTopic_name.data = diplomTopic.diplomTopic_name
        form.diplomTopic_subject.data = form.diplomTopic_subject
        form.diplomTopic_proglanguage.data = form.diplomTopic_proglanguage

        return render_template('diplomTopic_form.html', form=form, form_name="Edit diplomTopic", action="edit_diplomTopic")

    else:

        if not form.validate():
            return render_template('diplomTopic_form.html', form=form, form_name="Edit diplomTopic", action="edit_diplomTopic")
        else:
            # find user
            diplomTopic = db.session.query(ormDiplomTopic).filter(ormDiplomTopic.diplomTopic_id == form.diplomTopic_id.data).one()

            # update fields from form data
            diplomTopic.diplomTopic_name = form.diplomTopic_name.data
            diplomTopic.diplomTopic_subject = form.diplomTopic_subject.data
            diplomTopic.diplomTopic_proglanguage = form.diplomTopic_proglanguage.data

            db.session.commit()

            return redirect(url_for('diplomTopic'))


@app.route('/delete_diplomTopic', methods=['POST'])
@login_required
@roles_accepted('Admin', "User")
def delete_group():
    diplomTopic_id = request.form['diplomTopic_id']

    result = db.session.query(ormDiplomTopic).filter(ormDiplomTopic.diplomTopic_id == diplomTopic_id).one()

    db.session.delete(result)
    db.session.commit()

    return diplomTopic_id


@app.route('/clustering', methods=['GET', 'POST'])
@app.route('/clustering', methods=['GET', 'POST'])
@login_required
@roles_accepted("User", "Admin")
def claster():
    #     if id == None:
    #         id = db.session.query(ormTestCase.testcase_id).filter(
    #         ormTestCase.function_name_fk == function_name).all()[-1][0]
    #
    res1 = db.session.query(ormTeacher).all()

    liste = []
    normal = []
    for i in range(len(res1)):
        normal.append(i)

    for i in range(len(res1)):
        liste.append([])
        liste[i].append(normal[i])
        liste[i].append(res1[i].hashtag_views)
    matrix_data = np.matrix(liste)
    df = pd.DataFrame(matrix_data, columns=('par1', 'result'))
    print(df)
    X = df
    print(X)
    count_clasters = 2
    print(count_clasters)
    kmeans = KMeans(n_clusters=count_clasters, random_state=0).fit(X)
    # print(kmeans)
    count_columns = len(X.columns)
    # test_list = [0] * count_columns
    # test_list[0] = 1
    # test_list[1] = 1
    # test_list[2] = 1
    # print(test_list)
    iter = 0
    count_elements = [0, 0]
    for i in matrix_data:
        if kmeans.predict(i)[0] == 0:
            count_elements[0] += 1
        else:
            count_elements[1] += 1
        iter += 1
    # print(kmeans.labels_)
    # print(kmeans.predict(np.array([test_list])))

    pie = go.Pie(
        values=np.array(count_elements),
        labels=np.array(['unpopular', 'popular'])
    )
    data = {
        "pie": [pie]
    }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('clasteresation.html', count_claster=count_clasters, graphsJSON=graphsJSON)


if __name__ == '__main__':
    app.run()
