import json

from src.operations import Operations


def conclusion(filename) -> list[Operations]:
    operation: list[Operations] = []
    with open(filename) as f:
        for data in json.load(f):
            if data:
                op = Operations.init_from_dict(data)
                operation.append(op)

        return json.load(f)


def filtered_operation_by_state(*operation: Operations, state: str):
    filter_operations: list[Operations] = []
    for op in operation:
        if op.state == state:
            filter_operations.append(op)
    return filter_operations


def filtered_operation_by_date(*operation: Operations) -> list[Operations]:
    return sorted(operation, key=get_date)


def get_date(op: Operations):
    return op.date
