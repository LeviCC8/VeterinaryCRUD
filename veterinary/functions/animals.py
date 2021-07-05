from flask import request, flash
from flask_login import current_user
from veterinary import db
from veterinary.models import Animal
from veterinary.functions.utils import flash_form_errors_messages


def update_animal(update_animal_form):
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

        flash_form_errors_messages(update_animal_form, 'Falha na atualização do animal')

    return animal_to_update


def delete_animal():
    deleted_animal = request.form.get('deleted_animal')
    animal_to_delete = Animal.query.filter_by(id=deleted_animal).first()
    if animal_to_delete:
        flash(f"Seu animal {animal_to_delete.name} foi deletado do sistema!", category='success')
        Animal.query.filter_by(id=deleted_animal).delete()
        db.session.commit()
    return animal_to_delete


def add_animal(register_animal_form):
    if register_animal_form.validate_on_submit():
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


def update_health(update_health_form):
    updated_health = request.form.get('updated_health')
    animal_to_update = Animal.query.filter_by(id=updated_health).first()
    if animal_to_update:
        if update_health_form.validate_on_submit():
            animal_to_update.update_health(update_health_form.health.data)
            flash(f"A saúde do animal {animal_to_update.name} foi atualizada para {animal_to_update.health}!",
                  category='success')
