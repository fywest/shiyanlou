import sys
import csv
import os
from multiprocessing import Process, Queue


class Args(object):
    def __init__(self):
        try:
            self.args = sys.argv[1:]
            if len(sys.argv[1:]) != 6:
                raise ValueError
        except ValueError:
            print("Parameter Error")
            print(sys.argv[0], "-c test.cfg -d user.csv -o gongzi.csv")
            sys.exit(1)

    def get_name_config(self):
        index_c = self.args.index('-c')
        return self.args[index_c + 1]

    def get_name_user(self):
        index_d = self.args.index('-d')
        return self.args[index_d + 1]

    def get_name_gongzi(self):
        index_o = self.args.index('-o')
        return self.args[index_o + 1]

    def show(self):
        print(self.args)


def read_config(configfile=sys.argv[2]):
    config_local = {}
    with open(configfile, 'r') as file:
        for line in file:
            list = line.split('=')
            try:
                number = float(list[1].strip())
                config_local[list[0].strip()] = number
            except ValueError:
                print("config parameter error - float")
                sys.exit(1)
    return config_local


def read_users_data(q1, userfile=sys.argv[4]):
    userdata = []
    with open(userfile, 'r') as file:
        for line in file:
            list_user = line.split(',')
            try:
                id = int(list_user[0].strip())
                amount = int(list_user[1].strip())
                user_tup = (id, amount)
                userdata.append(user_tup)
            except ValueError:
                print("config parameter error - int")
                sys.exit(1)
    q1.put(userdata)
    return userdata


def calc_for_all_userdata(q1, q2):
    userdata = q1.get()
    list_str = []
    for user in userdata:
        userid = user[0]
        salary = int(user[1])

        insurance = 0
        start = 3500
        money_tax = 0

        config = read_config()
        low = float(config['JiShuL'])
        high = float(config['JiShuH'])
        for x in config:

            if x == 'JiShuL' or x == 'JiShuH':
                continue
            if salary < low:
                insurance += low * float(config[x])
            elif salary > high:
                insurance += high * float(config[x])
            else:
                insurance += salary * float(config[x])

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
        str = "{},{},{:.2f},{:.2f},{:.2f}".format(userid, salary, insurance, tax, salary_after_tax)
        list_str.append(str.split(','))
    q2.put(list_str)
    return list_str


def export(q2,name_gongzi=sys.argv[6]):
    result = q2.get()
    if os.path.exists(name_gongzi):
        os.remove(name_gongzi)
    for line in result:
        with open(name_gongzi, 'a', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(line)


if __name__ == '__main__':
    args = Args()

    q1 = Queue()
    q2 = Queue()

    p_userdata = Process(target=read_users_data, args=(q1,))
    p_cal = Process(target=calc_for_all_userdata, args=(q1, q2))
    p_export = Process(target=export, args=(q2,))

    p_userdata.start()
    p_userdata.join()

    p_cal.start()
    p_cal.join()

    p_export.start()
    p_export.join()
