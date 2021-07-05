from flask import request, flash
from flask_login import current_user
from veterinary.models import Consultation
from veterinary import db
from datetime import datetime


def schedule_consultation(schedule_consultation_form):
    scheduled_consultation = request.form.get('scheduled_consultation')
    consultation_to_schedule = Consultation.query.filter_by(id=scheduled_consultation).first()
    if consultation_to_schedule:
        consultation_to_schedule.schedule_consult(schedule_consultation_form.animals.data)
        flash(f"Consulta marcada com sucesso!", category='success')


def unschedule_consultation():
    unscheduled_consultation = request.form.get('unscheduled_consultation')
    consultation_to_unschedule = Consultation.query.filter_by(id=unscheduled_consultation).first()
    if consultation_to_unschedule:
        flash(f"Sua consulta foi desmarcada com sucesso!", category='success')
        consultation_to_unschedule.unschedule_consult()


def delete_consultation():
    deleted_consultation = request.form.get('deleted_consultation')
    consultation_to_delete = Consultation.query.filter_by(id=deleted_consultation).first()
    if consultation_to_delete:
        flash(f"Sua consulta foi deletada do sistema!", category='success')
        Consultation.query.filter_by(id=deleted_consultation).delete()
        db.session.commit()
    return consultation_to_delete


def add_consultation(register_consultation_form):
    if register_consultation_form.validate_on_submit():
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