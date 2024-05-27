from src.utils import conclusion, filtered_operation_by_state, filtered_operation_by_date


def main(filename='operations.json'):
    operation = conclusion(filename)
    operation = filtered_operation_by_state(*operation, state='EXECUTED')
    operation = filtered_operation_by_date(*operation)

    for op in operation[:5]:
        print(op.save())


if __name__ == '__main__':
    main()
