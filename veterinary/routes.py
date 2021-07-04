from veterinary import app
from flask import render_template, redirect, url_for, flash, request
from veterinary.models import *
from veterinary.forms import *
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime


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
    if user_form.errors != {}:  # If there are errors from the validations
        for err_msg in user_form.errors.values():
            flash(f'Falha no registro do usuário: {err_msg}', category='danger')

    return render_template('register.html', form=user_form)


@app.route('/register-client', methods=['GET', 'POST'])
def register_client_page():
    if 'user_form' in data:
        user_form = data['user_form']
        client_form = RegisterClientForm()
        if client_form.validate_on_submit():
            client_to_create = Client(login=user_form.login.data,
                                  name=user_form.name.data,
                                  cpf=user_form.cpf.data,
                                  password=user_form.password1.data,
                                  user_type=user_form.user_type.data)
            db.session.add(client_to_create)
            db.session.commit()

            credit_card_to_create = CreditCard(number=client_form.number.raw_data[0],
                                               name_titular=client_form.name_titular.data,
                                               cvv=client_form.cvv.raw_data[0],
                                               date_validate=client_form.date_validate.data,
                                               client_login=client_to_create.login)
            db.session.add(credit_card_to_create)
            db.session.commit()

            login_user(client_to_create)
            flash(f"Conta criada com sucesso! Bem-vindo(a) ao sistema VeterinaryCRUD, {client_to_create.name}!",
                  category='success')
            del data['user_form']
            return redirect(url_for('home_page'))
        if client_form.errors != {}:  # If there are errors from the validations
            for err_msg in client_form.errors.values():
                flash(f'Falha no registro do usuário: {err_msg}', category='danger')

        return render_template('register.html', form=client_form)
    else:
        return redirect(url_for('register_user_page'))


@app.route('/register-veterinarian', methods=['GET', 'POST'])
def register_veterinarian_page():
    if 'user_form' in data:
        user_form = data['user_form']
        veterinarian_form = RegisterVeterinarianForm()
        if veterinarian_form.validate_on_submit():
            veterinarian_to_create = Veterinarian(login=user_form.login.data,
                                  name=user_form.name.data,
                                  cpf=user_form.cpf.data,
                                  password=user_form.password1.data,
                                  user_type=user_form.user_type.data,
                                  expertise=veterinarian_form.expertise.data,
                                  college=veterinarian_form.college.data,
                                  salary=veterinarian_form.salary.raw_data[0])
            db.session.add(veterinarian_to_create)
            db.session.commit()

            veterinarian_registration_to_create = VeterinarianRegistration(number=veterinarian_form.number.raw_data[0],
                                               issuing_agency=veterinarian_form.issuing_agency.data,
                                               date_validate=veterinarian_form.date_validate.data,
                                               veterinarian_login=veterinarian_to_create.login)
            db.session.add(veterinarian_registration_to_create)
            db.session.commit()

            login_user(veterinarian_to_create)
            flash(f"Conta criada com sucesso! Bem-vindo(a) ao sistema VeterinaryCRUD, {veterinarian_to_create.name}!",
                  category='success')
            del data['user_form']
            return redirect(url_for('home_page'))
        if veterinarian_form.errors != {}:  # If there are errors from the validations
            for err_msg in veterinarian_form.errors.values():
                flash(f'Falha no registro do usuário: {err_msg}', category='danger')

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
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Seja bem-vindo(a) ao sistema VeterinaryCRUD, {attempted_user.name}!', category='success')
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
            # Update Animal logic
            updated_animal = request.form.get('updated_animal')
            animal_to_update = Animal.query.filter_by(id=updated_animal).first()
            if animal_to_update:
                if update_animal_form.validate_on_submit():
                    animal_to_update.update_infos(name=update_animal_form.name.data,
                                          age=update_animal_form.age.raw_data[0],
                                          type=update_animal_form.type.data,
                                          race=update_animal_form.race.data)
                    flash(f"Seu animal {animal_to_update.name} foi atualizado com sucesso!",
                          category='success')

                if update_animal_form.errors != {}:  # If there are errors from the validations
                    for err_msg in update_animal_form.errors.values():
                        flash(f'Falha na atualização do animal: {err_msg}', category='danger')

            # Delete Animal logic
            deleted_animal = request.form.get('deleted_animal')
            animal_to_delete = Animal.query.filter_by(id=deleted_animal).first()
            if animal_to_delete:
                flash(f"Seu animal {animal_to_delete.name} foi deletado do sistema!", category='success')
                Animal.query.filter_by(id=deleted_animal).delete()
                db.session.commit()

            # Add Animal Logic
            if register_animal_form.validate_on_submit() and animal_to_update is None:
                animal_to_create = Animal(name=register_animal_form.name.data,
                                      age=register_animal_form.age.raw_data[0],
                                      type=register_animal_form.type.data,
                                      race=register_animal_form.race.data,
                                      health='Saudável',
                                      client_login=current_user.login)
                db.session.add(animal_to_create)
                db.session.commit()
                flash(f"Seu animal {animal_to_create.name} está cadastrado no sistema e pronto para marcar consultas!",
                      category='success')

            if animal_to_update is None and animal_to_delete is None and register_animal_form.errors != {}:  # If there are errors from the validations
                for err_msg in register_animal_form.errors.values():
                    flash(f'Falha no registro do novo animal: {err_msg}', category='danger')
        elif current_user.is_veterinarian():
            # Update Health logic
            updated_health = request.form.get('updated_health')
            animal_to_update = Animal.query.filter_by(id=updated_health).first()
            if animal_to_update:
                if update_health_form.validate_on_submit():
                    animal_to_update.update_health(update_health_form.health.data)
                    flash(f"A saúde do animal {animal_to_update.name} foi atualizada para {animal_to_update.health}!",
                          category='success')

                if update_health_form.errors != {}:  # If there are errors from the validations
                    for err_msg in update_health_form.errors.values():
                        flash(f'Falha na atualização da saúde do animal: {err_msg}', category='danger')

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
            # Schedule Consultation logic
            scheduled_consultation = request.form.get('scheduled_consultation')
            consultation_to_schedule = Consultation.query.filter_by(id=scheduled_consultation).first()
            if consultation_to_schedule:
                consultation_to_schedule.schedule_consult(schedule_consultation_form.animals.data)
                flash(f"Consulta marcada com sucesso!", category='success')

            # Unschedule Consultation logic
            unscheduled_consultation = request.form.get('unscheduled_consultation')
            consultation_to_unschedule = Consultation.query.filter_by(id=unscheduled_consultation).first()
            if consultation_to_unschedule:
                flash(f"Sua consulta foi desmarcada com sucesso!", category='success')
                consultation_to_unschedule.unschedule_consult()

        elif current_user.is_veterinarian():
            # Delete Consultation logic
            deleted_consultation = request.form.get('deleted_consultation')
            consultation_to_delete = Consultation.query.filter_by(id=deleted_consultation).first()
            if consultation_to_delete:
                flash(f"Sua consulta foi deletada do sistema!", category='success')
                Consultation.query.filter_by(id=deleted_consultation).delete()
                db.session.commit()

            # Add Consultation Logic
            if register_consultation_form.validate_on_submit() and consultation_to_delete is None:
                date = datetime(year=register_consultation_form.date.data.year,
                                month=register_consultation_form.date.data.month,
                                day=register_consultation_form.date.data.day,
                                hour=register_consultation_form.time.data.hour,
                                minute=register_consultation_form.time.data.minute)
                consultation_to_create = Consultation(date=date,
                                          is_scheduled=False,
                                          veterinarian_login=current_user.login)
                db.session.add(consultation_to_create)
                db.session.commit()
                flash(f"Sua consulta foi marcada com sucesso!", category='success')

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
