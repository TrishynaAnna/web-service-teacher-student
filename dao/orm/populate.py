from dao.orm.model import *
from app import user_datastore

db.create_all()

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
                                  teacher_position = ' ',
                                  teacher_subject = '',
                                  teacher_hobby = '',
                                  teacher_proglanguage ='',
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















