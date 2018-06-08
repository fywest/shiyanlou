# -*- coding: UTF-8 -*-

from flask import request
from flask import Flask
from flask import render_template
# from ele import ele_red_packet
from lou_challenege_ele.ele import ele_red_packet


app = Flask(__name__)


@app.route('/',methods=['POST','GET'])
def phone_number_form():
    phone=''
    if request.method=='POST':

        phone = request.form["phone"]
        print(request.method,phone)
    else:
        print(request.method)

    get_red_packet = ele_red_packet(phone)
    return render_template('index.html', phone_number=get_red_packet)



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)