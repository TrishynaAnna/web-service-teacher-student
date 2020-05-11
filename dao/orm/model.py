from app import db
from app import app
from flask_security import RoleMixin, UserMixin
from flask_security import SQLAlchemyUserDatastore, Security

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

class ormRole(db.Model, RoleMixin):
        __tablename__ = 'orm_role'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique=True)



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
    subject = db.Column(db.String(20), nullable=False)
    hobby = db.Column(db.String(40), nullable=False)
  # photo = db.Column(db.text, nullable=False)
    position = db.Column(db.String(20), nullable=False)
    proglanguage = db.Column(db.String(40), nullable=False)
    specialization = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    works = db.Column(db.String(20), nullable=False)


    roles = db.relationship("ormRole", secondary=teacher_have_role, backref=db.backref('teacher', lazy='dynamic'))
    diplomWork = db.relationship("ormdiplomWork", secondary=teacher_own_diplomWork, backref=db.backref('owner', lazy='dynamic'))
    diplomTopic = db.relationship("ormdiplomTopic", secondary=techer_own_diplomTopic, backref=db.backref('teacher', lazy='dynamic'))


class ormDiplomTopic(db.Model):
     __tablename__ = 'diplomTopic'
    diplomTopic_id = db.Column(db.Integer, primary_key=True)
    diplomTopic_name = db.Column(db.String(300), nullable=False)
    diplomTopic_subject = db.Column(db.String(150), nullable=False)
    diplomTopic_proglanguage = db.Column(db.String(50), nullable=False)


    diplomTopic = db.relationship("ormdiplomTopic", secondary=techer_owndiplomTopic, backref=db.backref('teacher', lazy='dynamic'))



    class ormDiplomWork(db.Model):
     __tablename__ = 'diplomWork'

    diplomWork_id = db.Column(db.Integer, primary_key=True)
    diplomWork_name = db.Column(db.String(300), primary_key=True)
    diplomWork_proglanguage = db.Column(db.String(50), nullable=False)
    diplomWork_subject= db.Column(db.String(100), nullable=False)
    diplomWork_specialization= db.Column(db.Integer, nullable=False)
    diplomWork_title = db.Column(db.String(150), nullable=False)


    diplomWork = db.relationship("ormDiplomWork", secondary=teacher_own_diplomWork, backref=db.backref('owner', lazy='dynamic'))






user_datastore = SQLAlchemyUserDatastore(db,ormTeacher, ormStudent, ormRole)
security = Security(app, user_datastore)