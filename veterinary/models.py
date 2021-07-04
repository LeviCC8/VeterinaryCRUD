from veterinary import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_login):
    return User.query.get(user_login)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    login = db.Column(db.String(length=10), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False, unique=True)
    cpf = db.Column(db.String(length=11), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    user_type = db.Column(db.String(length=50), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'user',
        'polymorphic_on':user_type
    }

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def get_id(self):
        return self.login

    def is_client(self):
        return self.user_type == 'client'

    def is_veterinarian(self):
        return self.user_type == 'veterinarian'

    def register(self):
        pass

    def login_account(self):
        pass


class Client(User):
    __tablename__ = 'client'
    login = db.Column(db.String(length=10), db.ForeignKey('user.login'), primary_key=True)
    credit_card = db.relationship('CreditCard', backref='client', lazy=True, uselist=False)
    animals = db.relationship('Animal', backref='client', lazy=True)
    __mapper_args__ = {
        'polymorphic_identity':'client'
    }


class CreditCard(db.Model):
    number = db.Column(db.Integer(), primary_key=True)
    name_titular = db.Column(db.String(length=50), nullable=False)
    cvv = db.Column(db.Integer(), nullable=False)
    date_validate = db.Column(db.DateTime(), nullable=False)
    client_login = db.Column(db.String(length=10), db.ForeignKey('user.login'), nullable=False, unique=True)


class Veterinarian(User):
    __tablename__ = 'veterinarian'
    login = db.Column(db.String(length=10), db.ForeignKey('user.login'), primary_key=True)
    registration = db.relationship('VeterinarianRegistration', backref='veterinarian', lazy=True,
                                    uselist=False)
    consultations = db.relationship('Consultation', backref='veterinarian', lazy=True)
    expertise = db.Column(db.String(length=20), nullable=False)
    college = db.Column(db.String(length=30), nullable=False)
    salary = db.Column(db.Integer(), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity':'veterinarian'
    }


class VeterinarianRegistration(db.Model):
    number = db.Column(db.Integer(), primary_key=True)
    issuing_agency = db.Column(db.String(length=30), nullable=False)
    date_validate = db.Column(db.DateTime(), nullable=False)
    veterinarian_login = db.Column(db.String(length=10), db.ForeignKey('user.login'), nullable=False, unique=True)


class Animal(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=20), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.String(length=15), nullable=False)
    race = db.Column(db.String(length=20), nullable=False)
    health = db.Column(db.String(length=30), nullable=False)
    client_login = db.Column(db.String(length=10), db.ForeignKey('user.login'), nullable=False)
    consultations = db.relationship('Consultation', backref='animal', lazy=True)

    def update_infos(self, name, age, type, race):
        self.name = name
        self.age = age
        self.type = type
        self.race = race
        db.session.commit()


class Consultation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)
    veterinarian_login = db.Column(db.String(length=10), db.ForeignKey('user.login'), nullable=False)
    is_scheduled = db.Column(db.Boolean(), nullable=False)
    animal_id = db.Column(db.String(length=10), db.ForeignKey('animal.id'))
