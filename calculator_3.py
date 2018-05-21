#!/usr/bin/env python3
import sys
import os


class Config:
    def __init__(self, configfile):
        self._config = {}
        with open(configfile, 'r') as file:
            for line in file:
                list = line.split('=')
                self._config[list[0].strip()] = list[1].strip()

    def get_config(self, key):
        return self._config[key]


class User:
    def __init__(self, userfile):
        self._user = {}
        with open(userfile, 'r') as file:
            for line in file:
                list = line.split(',')
                self._user[list[0].strip()] = list[1].strip()

    def get_user(self, key):
        return self._user[key]


def calculate(config, user):
    for userid in user._user:
        salary = int(user._user[userid])

        insurance = 0
        start = 3500
        money_tax = 0

        low = float(config._config['JiShuL'])
        high = float(config._config['JiShuH'])
        for x in config._config:

            if x == 'JiShuL' or x == 'JiShuH':
                continue
            if salary < low:
                insurance += low * float(config._config[x])
            elif salary > high:
                insurance += high * float(config._config[x])
            else:
                insurance += salary * float(config._config[x])

        if salary <= start:
            salary_after_tax = salary - insurance
            rate_tax = 0
            reduce_tax = 0
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
        str = "{},{},{:.2f},{:.2f},{:.2f}\r".format(userid, salary, insurance, tax, salary_after_tax)
        print(str)
        with open(name_gongzi, 'a') as file:
            file.write(str)


if __name__ == '__main__':
    if len(sys.argv[1:]) < 3:
        print("Parameter Error")
        print(sys.argv[0], " test.cfg user.csv gongzi.csv")
        sys.exit(1)

    args = sys.argv[1:]
    index_c = args.index('-c')
    name_config = args[index_c + 1]
    index_d = args.index('-d')
    name_user = args[index_d + 1]
    index_o = args.index('-o')
    name_gongzi = args[index_o + 1]

    config = Config(name_config)
    user = User(name_user)

    if os.path.exists(name_gongzi):
        os.remove(name_gongzi)

    calculate(config, user)
