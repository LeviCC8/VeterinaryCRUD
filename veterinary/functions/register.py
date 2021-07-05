from veterinary.models import Client, CreditCard, Veterinarian, VeterinarianRegistration
from veterinary import db
from veterinary.functions.utils import login_user_in_system


def register_client(user_form, client_form):
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

    login_user_in_system(client_to_create,
                         f"Conta criada com sucesso! Bem-vindo(a) ao sistema VeterinaryCRUD, {client_to_create.name}!")


def register_veterinarian(user_form, veterinarian_form):
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

    login_user_in_system(veterinarian_to_create,
                         f"Conta criada com sucesso! Bem-vindo(a) ao sistema VeterinaryCRUD, {veterinarian_to_create.name}!")