from datetime import datetime


class Payment:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    @classmethod
    def init_from_str(cls, payment):
        *name, number = payment.split(' ')
        return cls(' '.join(name), number)

    def __repr__(self):  # pragma: nocover
        return f'Payment(name={self.name}, number={self.number})'

    def safe(self) -> str:
        if self.name == 'Счёт':
            safe_number = self.get_safe_account()
        else:
            safe_number = self.get_safe_card_number()
            safe_number = self.split_card_number(safe_number)

        return f'{self.name} {safe_number}'

    def get_safe_account(self) -> str:
        return '*' * 2 + self.number[-4:]

    def get_safe_card_number(self) -> str:
        start, middle, end = self.number[:6], self.number[6:-4], self.number[-4:]
        return start + '*' * len(middle) + end

    @staticmethod
    def split_card_number(card_number: str) -> str:
        splits = (4, 4, 4, 4)
        result = []
        for spaces in splits:
            block, tail = card_number[:spaces], card_number[spaces:]
            result.append(block)
            card_number = tail
        return " ".join(result)


class Amount:
    def __init__(self, price, name_currency, code_currency):
        self.price = price
        self.name_currency = name_currency
        self.code_currency = code_currency


class Operations:
    def __init__(self, id, state, date, amount, description, from_person, to_bank):
        self.id = id
        self.state = state
        self.date = date
        self.amount = amount
        self.description = description
        self.from_person = from_person
        self.to_bank = to_bank

    def __repr__(self):  # pragma: nocover
        return (
            f'Operation({self.id}, state={self.state}, date={self.date}, amount={self.amount},'
            f'from={self.from_person}, to={self.to_bank})'
        )

    @classmethod
    def init_from_dict(cls, data):
        return cls(
            id=int(data['id']),
            state=data['state'],
            date=datetime.fromisoformat(data['date']),
            amount=Amount(
                price=float(data['operationAmount']['amount']),
                name_currency=data['operationAmount']['currency']['name'],
                code_currency=data['operationAmount']['currency']['code']
            ),
            description=data['description'],
            from_person=data.get('from'),
            to_bank=data.get('to')
        )

    def safe(self) -> str:  # pragma: nocover
        lines = [
            f'{self.date.strftime("%d.%m.%Y")}: {self.description}'
        ]
        if self.from_person:
            lines.append(f'{self.from_person.safe()} -> {self.to_bank.safe()}')
        else:
            lines.append(f'{self.from_person.safe()}')

        lines.append(f'{self.amount.price} {self.amount.name_currency}')

        return '\n'.join(lines)
