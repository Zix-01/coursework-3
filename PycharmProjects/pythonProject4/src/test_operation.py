from src.operations import Payment, Operations


def test_init_payment_from_str():
    payment = Payment.init_from_str('Visa Gold 5999414228426353')
    assert payment.name == 'Visa Gold'
    assert payment.number == '5999414228426353'


def test_safe_payment_for_amount():
    payment = Payment(name='Счёт', number='64686473678894779589')
    assert payment.safe() == 'Счёт **9589'


def test_safe_payment_for_card_number():
    payment = Payment(name='Maestro', number='1596837868705199')
    assert payment.safe() == 'Maestro 1596 83** **** 5199'


def split_card_number():
    card_number = '1596837868705199'
    result = Payment.split_card_number(card_number)
    assert result == '1596 8378 6870 5199'


def test_init_from_dict():
    data = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589"
    }

    op = Operations.init_from_dict(data)

    assert op.id == 441945886
    assert op.state == "EXECUTED"
    assert op.amount.price == 31957.58
    assert op.amount.name_currency == "руб."
    assert op.amount.code_currency == "RUB"
    assert op.description == "Перевод организации"
    assert op.from_person == 'Maestro 1596837868705199'
    assert op.to_bank == 'Счет 64686473678894779589'gi
