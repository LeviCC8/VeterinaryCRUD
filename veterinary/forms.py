from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from veterinary.models import *


class RegisterUserForm(FlaskForm):
    def validate_login(self, login_to_check):
        user = User.query.filter_by(login=login_to_check.data).first()
        if user:
            raise ValidationError('Login já cadastrado!')

    def validate_name(self, name_to_check):
        user = User.query.filter_by(name=name_to_check.data).first()
        if user:
            raise ValidationError('Nome já cadastrado!')

    def validate_cpf(self, cpf_to_check):
        user = User.query.filter_by(cpf=cpf_to_check.data).first()
        if user:
            raise ValidationError('CPF já cadastrado!')

    login = StringField(label='Login:', validators=[
        Length(min=2, max=10, message='Login precisa ter entre 2 à 10 caracteres'),
        DataRequired(message='Login não fornecido')])
    name = StringField(label='Nome Completo:', validators=[
        Length(min=5, max=50, message='Nome precisa ter entre 5 à 50 caracteres'),
        DataRequired(message='Nome não fornecido')])
    cpf = StringField(label='CPF:', validators=[
        Length(min=11, max=11, message='CPF precisa ter 11 caracteres'),
        DataRequired(message='CPF não fornecido')])
    password1 = PasswordField(label='Senha:', validators=[
        Length(min=6, max=60, message='Senha precisa ter entre 6 à 60 caracteres'),
        DataRequired(message='Senha não fornecida')])
    password2 = PasswordField(label='Repita a Senha:', validators=[
        EqualTo('password1', message='Confirmação de senha inválida'),
        DataRequired(message='Confirmação de senha não fornecida')])
    user_type = SelectField('Tipo de usuário', choices=[('client', 'Cliente'), ('veterinarian', 'Veterinário')])
    submit = SubmitField(label='Próximo passo')


class RegisterClientForm(FlaskForm):
    def validate_number(self, number_to_check):
        credit_card = CreditCard.query.filter_by(number=number_to_check.data).first()
        if credit_card:
            raise ValidationError('Número de cartão já cadastrado!')

    number = IntegerField(label='Número do cartão de crétido:', validators=[
        DataRequired(message='Número do cartão de crédito não fornecido')])
    name_titular = StringField(label='Nome do Titular:', validators=[
        Length(min=5, max=50, message='Nome do titular do cartão precisa ter entre 5 à 50 caracteres'),
        DataRequired(message='Nome do titular do cartão não fornecido')])
    cvv = IntegerField(label='CVV:', validators=[
        DataRequired('CVV não fornecido')])
    date_validate = DateField(label='Data de Vencimento:', format='%Y-%m-%d')
    submit = SubmitField(label='Criar Conta')


class RegisterVeterinarianForm(FlaskForm):
    def validate_number(self, number_to_check):
        veterinarian_registration = VeterinarianRegistration.query.filter_by(number=number_to_check.data).first()
        if veterinarian_registration:
            raise ValidationError('Número de registro veterinário já cadastrado!')

    expertise = StringField(label='Especialidade:', validators=[
        Length(min=3, max=20, message='Especialidade precisa ter entre 3 à 20 caracteres'),
        DataRequired(message='Especialidade não fornecida')])
    college = StringField(label='Faculdade:', validators=[
        Length(min=3, max=30, message='Faculdade precisa ter entre 3 à 30 caracteres'),
        DataRequired(message='Faculdade não fornecida')])
    salary = IntegerField(label='Salário:', validators=[
        DataRequired(message='Salário não fornecido')])
    number = IntegerField(label='Número de registro veterinário:', validators=[
        DataRequired(message='Número de registro veterinário não fornecido')])
    issuing_agency = StringField(label='Nome da Agência Emissora:', validators=[
        Length(min=5, max=30, message='Nome da agência emissora precisa ter entre 5 à 30 caracteres'),
        DataRequired(message='Nome da agência emissora não fornecida')])
    date_validate = DateField(label='Data de Vencimento:', format='%Y-%m-%d')
    submit = SubmitField(label='Criar Conta')


class LoginForm(FlaskForm):
    login = StringField(label='Login:', validators=[DataRequired()])
    password = PasswordField(label='Senha:', validators=[DataRequired()])
    submit = SubmitField(label='Entrar')


class RegisterAnimalForm(FlaskForm):
    def insert_default(self, animal):
        self.name.default = animal.name
        self.age.default = animal.age
        self.type.default = animal.type
        self.race.default = animal.race

    name = StringField(label='Nome:', validators=[
        Length(min=2, max=20, message='Nome precisa ter entre 2 à 20 caracteres'),
        DataRequired(message='Nome não fornecido')])
    age = IntegerField(label='Idade:', validators=[
        DataRequired(message='Idade não fornecida')])
    type = StringField(label='Tipo:', validators=[
        Length(min=2, max=15, message='Tipo precisa ter entre 2 à 15 caracteres'),
        DataRequired(message='Tipo não fornecido')])
    race = StringField(label='Raça:', validators=[
        Length(min=2, max=20, message='Raça precisa ter entre 2 à 20 caracteres'),
        DataRequired(message='Raça não fornecida')])
    submit = SubmitField(label='Cadastrar Animal')


class DeleteAnimalForm(FlaskForm):
    submit = SubmitField(label='Deletar Animal')