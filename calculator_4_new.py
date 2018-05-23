#!/usr/bin/env python3
import sys
import csv
import os
from multiprocessing import Process, Queue

import getopt
import configparser
from datetime import datetime


class Config(object):

    def read_config(self, cityname, configfile, q0):
        config_local = {}
        config = configparser.ConfigParser()
        config.read(configfile)
        cityname_upper = cityname.upper()
        kvs = config.items(cityname_upper)
        for key, value in kvs:
            try:
                number = float(value.strip())
                config_local[key.strip()] = number
            except ValueError:
                print("config parameter error - float")
                sys.exit(1)
        q0.put(config_local)


class UserData(object):

    def read_users_data(self, userfile, q1):
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


class IncomeTaxCalculator(object):

    def calc_for_all_userdata(self, q0, q1, q2):

        list_str = []
        config_queue_dict = q0.get()
        userdata_queue_list = q1.get()
        for user in userdata_queue_list:
            userid = user[0]
            salary = int(user[1])

            insurance = 0
            start = 3500
            money_tax = 0

            low = float(config_queue_dict['JiShuL'.lower()])
            high = float(config_queue_dict['JiShuH'.lower()])
            for x in config_queue_dict:

                if x == 'JiShuL'.lower() or x == 'JiShuH'.lower():
                    continue
                if salary < low:
                    insurance += low * float(config_queue_dict[x])
                elif salary > high:
                    insurance += high * float(config_queue_dict[x])
                else:
                    insurance += salary * float(config_queue_dict[x])

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
            now = datetime.now()
            str_now = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
            str_gongzi = "{},{},{:.2f},{:.2f},{:.2f},{}".format(userid, salary, insurance, tax, salary_after_tax,
                                                                str_now)
            list_str.append(str_gongzi.split(','))
        q2.put(list_str)

    def export(self, name_gongzi, q2):
        if os.path.exists(name_gongzi):
            os.remove(name_gongzi)
        gongzi_queue_list = q2.get()
        for line in gongzi_queue_list:
            with open(name_gongzi, 'a', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(line)


def usage():
    print("Usage:%s -C cityname -c configfile -d userdata -o resultdata" % (sys.argv[0]))


if __name__ == '__main__':
    name_dict = {}
    try:
        shortargs = 'hC:c:d:o:'
        longargs = ['help']
        opts, args = getopt.getopt(sys.argv[1:], shortargs, longargs)

        city_exist = False
        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit(1)
            elif opt in ('-C'):
                name_dict['name_city'] = arg
                city_exist = True
            elif opt in ('-C'):
                name_dict['name_city'] = arg
            elif opt in ('-c'):
                name_dict['name_config'] = arg
            elif opt in ('-d'):
                name_dict['name_user'] = arg
            elif opt in ('-o'):
                name_dict['name_gongzi'] = arg
            else:
                print('wrong parameters %s %s' % (opt, arg))
                usage()
                exit(1)
    except getopt.GetoptError:
        print('getopt error!')
        usage()
        sys.exit(1)

    if city_exist == False:
        name_dict['name_city'] = 'DEFAULT'


    config = Config()
    userdata = UserData()
    gongzi = IncomeTaxCalculator()

    q0 = Queue()
    q1 = Queue()
    q2 = Queue()

    p_config = Process(target=config.read_config, args=(name_dict['name_city'], name_dict['name_config'], q0,))
    p_userdata = Process(target=userdata.read_users_data, args=(name_dict['name_user'], q1,))
    p_cal = Process(target=gongzi.calc_for_all_userdata, args=(q0, q1, q2))
    p_export = Process(target=gongzi.export, args=(name_dict['name_gongzi'], q2,))

    p_config.start()
    p_config.join()

    p_userdata.start()
    p_userdata.join()

    p_cal.start()
    p_cal.join()

    p_export.start()
    p_export.join()
