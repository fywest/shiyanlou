#!/usr/bin/env python3

def change():
    global a
    a=90
    print(a)

a=9
print("before a= ",a)
change()
print("after change() a= ",a)
