# -*- coding: utf-8 -*-

import re
from datetime import datetime

# 使用正则表达式解析日志文件，返回数据列表
def open_parser(filename):
    with open(filename) as logfile:
        # 使用正则表达式解析日志文件
        pattern = (r''
                   r'(\d+.\d+.\d+.\d+)\s-\s-\s'  # IP 地址
                   r'\[(.+)\]\s'  # 时间
                   r'"GET\s(.+)\s\w+/.+"\s'  # 请求路径
                   r'(\d+)\s'  # 状态码
                   r'(\d+)\s'  # 数据大小
                   r'"(.+)"\s'  # 请求头
                   r'"(.+)"'  # 客户端信息
                   )
        parsers = re.findall(pattern, logfile.read())
    return parsers

def main():

    # 使用正则表达式解析日志文件
    # logs = open_parser('/home/shiyanlou/Code/nginx.log')
    logs = open_parser('nginx.log')

    '''
    1. 解析文件就是分离不同类型数据（IP，时间，状态码等）
    2. 从解析后的文件中统计挑战需要的信息
    '''
    list_all=[]
    for item in logs:
        dict_temp = {}
        dict_temp['ip']=item[0]
        dict_temp['datetime']=item[1]
        dict_temp['requestUrl']=item[2]
        dict_temp['errorCode']=item[3]
        dict_temp['info1']=item[4]
        dict_temp['info2'] = item[5]
        dict_temp['info3'] = item[6]
        list_all.append(dict_temp)

    dict_ip={}
    dict_url_404={}
    for item in list_all:
        # print(item['datetime'][:11])
        if item['datetime'][:11] == '11/Jan/2017':
            # print('****************',item['datetime'][:11])
            if item['ip'] not in dict_ip:
                dict_ip[item['ip']]=1
            else:
                dict_ip[item['ip']]+=1

        # filter url 440
        if item['errorCode']=='404':
            if item['requestUrl'] not in dict_url_404:
                dict_url_404[item['requestUrl']]=1
            else:
                dict_url_404[item['requestUrl']]+=1


    sorted_list_ip=sorted(dict_ip.items(),key=lambda x:x[1])
    tuple_ip_max=sorted_list_ip[-1]
    ip_dict={}
    ip_dict[tuple_ip_max[0]]=tuple_ip_max[1]

    sorted_list_url_440=sorted(dict_url_404.items(),key=lambda x:x[1])
    tuple_url_440_max=sorted_list_url_440[-1]
    url_dict={}
    url_dict[tuple_url_440_max[0]]=tuple_url_440_max[1]



    return ip_dict, url_dict


if __name__ == '__main__':
    ip_dict, url_dict = main()
    print(ip_dict, url_dict)