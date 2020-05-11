# from flask.ext.wtf import Form
# from wtforms import TextField
#
#
# class LoginForm(Form):
#     admin = TextField('Admin', [validators.Required()])
#
#     def __init__(self, *args, **kwargs):
#         kwargs['csrf_enabled'] = False
#         Form.__init__(self, *args, **kwargs)
#
#     def validate(self):
#         lf = Form.validate(self)
#         if not lf:
#             return False
#
#         admin = Admin.query.filter_by(userd=self.admin.data).first()
#         if admin is None:
#             self.admin.errors.append('Unknown admin')
#             return False
#
#         self.admin = admin
#         return True
