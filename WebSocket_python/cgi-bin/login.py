#!/usr/bin/env python3
import cgitb
import cgi
import os

cgitb.enable()

form = cgi.FieldStorage()
print(form)

first_name = form.getvalue('name')
last_name = form.getvalue('lastname')
MAC = form.getvalue('MAC')
if (MAC == "2C:54:6C:66:90:FF"):
    print("Content-Type:text/html;charset=utf-8")
    print("Content-type:text/html\r\n")
    print("<h1> Login OK </h1>")
else:
    print("Content-Type:text/html;charset=utf-8")
    print("Content-type:text/html\r\n")
    print("<h1> Login Fail </h1>")





