#!/usr/bin/env python3
import sys


def calculate(salary):
    insurance = 0
    start = 3500

    insurance_dict = {'pension': 0.08, 'medical': 0.02, 'unemployment': 0.005, 'injury': 0, 'maternity': 0,
                      'fund': 0.06}
    for KEY in insurance_dict:
        insurance += salary * insurance_dict[KEY]

    if salary <= start:
        return salary - insurance
    else:
        money_tax = salary - insurance - start

    if money_tax > 80000:
        rate_tax = 0.45
        reduce_tax = 13505
    elif money_tax > 55000:
        rate_tax = 0.35
        reduce_tax = 5505
    elif money_tax > 35000:
        rate_tax = 0.30
        reduce_tax = 2755
    elif money_tax > 9000:
        rate_tax = 0.25
        reduce_tax = 1005
    elif money_tax > 4500:
        rate_tax = 0.20
        reduce_tax = 555
    elif money_tax > 1500:
        rate_tax = 0.10
        reduce_tax = 105
    else:
        rate_tax = 0.03
        reduce_tax = 0

    tax = money_tax * rate_tax - reduce_tax
    salary_after_tax = salary - insurance - tax

    return salary_after_tax


if len(sys.argv) < 2:
    print("Parameter Error")
    sys.exit(1)

employee_dict = {}
for arg in sys.argv[1:]:
    list_parameter = arg.split(':')
    try:
        if len(list_parameter) < 2:
            raise ValueError
        if (list_parameter[0].isdigit()) and (list_parameter[1].isdigit()):

            employee_dict[list_parameter[0]] = list_parameter[1]

        else:
            raise ValueError
    except ValueError:
        print("Parameter Error")
        sys.exit(1)
for key in employee_dict:
    print("{}:{:.2f}".format(key, calculate(int(employee_dict[key]))))
sys.exit(0)
