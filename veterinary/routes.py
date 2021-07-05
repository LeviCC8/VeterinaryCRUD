from veterinary import app
from flask import render_template, redirect, url_for, flash, request
from veterinary.forms import *
from flask_login import logout_user, login_required, current_user
from veterinary.functions.register import register_client, register_veterinarian
from veterinary.functions.utils import flash_form_errors_messages, login_user_in_system
from veterinary.functions.animals import update_animal, delete_animal, add_animal, update_health
from veterinary.functions.consultations import schedule_consultation, unschedule_consultation, delete_consultation, add_consultation


data = {}


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/register-user', methods=['GET', 'POST'])
def register_user_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    user_form = RegisterUserForm()
    if user_form.validate_on_submit():
        data['user_form'] = user_form

        if user_form.user_type.data == 'client':
            return redirect(url_for('register_client_page'))

        elif user_form.user_type.data == 'veterinarian':
            return redirect(url_for('register_veterinarian_page'))

    flash_form_errors_messages(user_form, 'Falha no registro do usuário')

    return render_template('register.html', form=user_form)


@app.route('/register-client', methods=['GET', 'POST'])
def register_client_page():
    if 'user_form' in data:
        user_form = data['user_form']
        client_form = RegisterClientForm()

        if client_form.validate_on_submit():
            register_client(user_form, client_form)
            del data['user_form']
            return redirect(url_for('home_page'))

        flash_form_errors_messages(client_form, 'Falha no registro do usuário')

        return render_template('register.html', form=client_form)
    else:
        return redirect(url_for('register_user_page'))


@app.route('/register-veterinarian', methods=['GET', 'POST'])
def register_veterinarian_page():
    if 'user_form' in data:
        user_form = data['user_form']
        veterinarian_form = RegisterVeterinarianForm()

        if veterinarian_form.validate_on_submit():
            register_veterinarian(user_form, veterinarian_form)
            del data['user_form']
            return redirect(url_for('home_page'))

        flash_form_errors_messages(veterinarian_form, 'Falha no registro do usuário')

        return render_template('register.html', form=veterinarian_form)
    else:
        return redirect(url_for('register_user_page'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(login=form.login.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):

            login_user_in_system(attempted_user,
                                 f'Seja bem-vindo(a) ao sistema VeterinaryCRUD, {attempted_user.name}!')

            return redirect(url_for('home_page'))
        else:
            flash('Seus dados estão incorretos, tente novamente!', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("Você saiu da sua conta, volte sempre!", category='info')
    return redirect(url_for("home_page"))


@app.route('/animals', methods=['GET', 'POST'])
@login_required
def animals_page():
    update_animal_form = RegisterAnimalForm()
    register_animal_form = RegisterAnimalForm()
    delete_animal_form = ConfirmForm()
    update_health_form = UpdateHealthForm()

    if request.method == 'POST':
        if current_user.is_client():

            animal_to_update = update_animal(update_animal_form)

            animal_to_delete = delete_animal()

            if animal_to_update is None:
                add_animal(register_animal_form)

            if animal_to_update is None and animal_to_delete is None:
                flash_form_errors_messages(register_animal_form, 'Falha no registro do novo animal')

        elif current_user.is_veterinarian():
            update_health()
            flash_form_errors_messages(update_health_form, 'Falha na atualização da saúde do animal')

        return redirect(url_for('animals_page'))

    if request.method == "GET":
        if current_user.is_client():
            animals = Animal.query.filter_by(client_login=current_user.login)

        elif current_user.is_veterinarian():
            animals = Animal.query.all()

        return render_template('animals.html',
                               animals=animals,
                               update_animal_form=update_animal_form,
                               register_animal_form=register_animal_form,
                               delete_animal_form=delete_animal_form,
                               update_health_form=update_health_form,
                               User=User)


@app.route('/consultations', methods=['GET', 'POST'])
@login_required
def consultations_page():
    register_consultation_form = RegisterConsultationForm()
    delete_consultation_form = ConfirmForm()
    schedule_consultation_form = ScheduleConsultationForm()
    unschedule_consultation_form = ConfirmForm()

    if request.method == 'POST':
        if current_user.is_client():
            schedule_consultation(schedule_consultation_form)

            unschedule_consultation()

        elif current_user.is_veterinarian():
            consultation_to_delete = delete_consultation()

            if consultation_to_delete is None:
                add_consultation(register_consultation_form)

        return redirect(url_for('consultations_page'))

    if request.method == 'GET':

        if current_user.is_client():
            consultations = Consultation.query.filter_by(is_scheduled=False)
            scheduled_consultations = current_user.get_scheduled_consultations()

        elif current_user.is_veterinarian():
            consultations = Consultation.query.filter_by(veterinarian_login=current_user.login)
            scheduled_consultations = []

        return render_template('consultations.html',
                               consultations=consultations,
                               scheduled_consultations=scheduled_consultations,
                               register_consultation_form=register_consultation_form,
                               schedule_consultation_form=schedule_consultation_form,
                               unschedule_consultation_form=unschedule_consultation_form,
                               delete_consultation_form=delete_consultation_form,
                               User=User, Animal=Animal)
