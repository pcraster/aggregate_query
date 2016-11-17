# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask import current_app
# from flask_login import UserMixin, AnonymousUserMixin
# from . import db
# 
# 
# class Permission:
#     USE_API = 0x01
#     # 0x02
#     # 0x04
#     # 0x08
#     ADMINISTRATOR = 0x80
# 
# 
# class Role(db.Model):
# 
#     __tablename__ = "roles"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship("User", backref="role", lazy="dynamic")
# 
# 
#     @staticmethod
#     def insert_roles():
# 
#         roles = {
#             "User": (
#                 Permission.USE_API, True),
#             "Administrator": (
#                 0xff, False)
#         }
# 
#         for role_name in roles:
# 
#             role = Role.query.filter_by(name=role_name).first()
# 
#             if role is None:
#                 role = Role(name=role_name)
# 
#             role.permissions = roles[role_name][0]
#             role.default = roles[role_name][1]
# 
#             db.session.add(role)
# 
#         db.session.commit()
# 
# 
#     def __repr__(self):
#         return "<Role {}>".format(self.name)
# 
# 
# class User(UserMixin, db.Model):
# 
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(64), unique=True, index=True)
#     # username = db.Column(db.String(64), unique=True, index=True)
#     password_hash = db.Column(db.String(128))
#     role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
#     last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
# 
# 
#     def __init__(self,
#             email,
#             password,
#             role):
#         self.email = email
#         self.password = password  # Will be hashed on the fly, see below
#         self.role = role
# 
# 
#     @property
#     def password(self):
#         raise AttributeError("password is not a readable attribute")
# 
# 
#     @password.setter
#     def password(self,
#             password):
#         """
#         Set the password
# 
#         The password is hashed and cannot be recovered
#         """
#         self.password_hash = generate_password_hash(password)
# 
# 
#     def verify_password(self,
#             password):
#         """
#         Return whether the password passed in matches the one passed
#         in earlier
#         """
#         return check_password_hash(self.password_hash, password)
# 
# 
#     def generate_configuration_token(self,
#             expiration=3600):
#         serializer = Serializer(current_app.config["SECRET_KEY"], expiration)
#         return serializer.dumps({"confirm": self.id})
# 
# 
#     def confirm(self,
#             token):
# 
#         serializer = Serializer(current_app.config["SECRET_KEY"])
# 
#         try:
#             data = serializer.loads(token)
#         except:
#             return False
# 
#         if data.get("confirm") != self.id:
#             return False
# 
#         self.confirmed = True
# 
#         db.session.add(self)
# 
#         return True
# 
# 
#     def generate_reset_token(self,
#             expiration=3600):
# 
#         serializer = Serializer(current_app.config["SECRET_KEY"], expiration)
# 
#         return serializer.dumps({"reset": self.id})
# 
# 
#     def reset_password(self, token, new_password):
# 
#         serializer = Serializer(current_app.config["SECRET_KEY"])
# 
#         try:
#             data = serializer.loads(token)
#         except:
#             return False
# 
#         if data.get("reset") != self.id:
#             return False
# 
#         self.password = new_password
# 
#         db.session.add(self)
# 
#         return True
# 
# 
#     def can(self,
#             permissions):
#         return self.role is not None and \
#             (self.role.permissions & permissions) == permissions
# 
# 
#     def is_administrator(self):
#         return self.can(Permission.ADMINISTRATOR)
# 
# 
#     def ping(self):
#         self.last_seen = datetime.utcnow()
#         db.session.add(self)
# 
# 
#     def to_json(self):
#         json_user = {
#             "email": self.email,
#             "last_seen": self.last_seen,
#         }
# 
#         return json_user
# 
# 
#     def generate_auth_token(self,
#             expiration):
# 
#         serializer = Serializer(current_app.config["SECRET_KEY"],
#             expires_in=expiration)
# 
#         return serializer.dumps({"id": self.id}).decode("ascii")
# 
# 
#     @staticmethod
#     def verify_auth_token(
#             token):
# 
#         serializer = Serializer(current_app.config["SECRET_KEY"])
# 
#         try:
#             data = serializer.loads(token)
#         except:
#             return None
# 
#         return User.query.get(data["id"])
# 
# 
#     def __repr__(self):
#         return "<User {}>".format(self.email)
# 
# 
# class AnonymousUser(AnonymousUserMixin):
# 
#     def can(self,
#             permissions):
#         return False
# 
#     def is_administrator(self):
#         return False
