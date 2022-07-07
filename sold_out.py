from flask import Flask, request
from database import db
from model import ABMenu, PermMenu
from generate_menu import json_load2
import json
import datetime

pmenu_name[]
for i in json_load2:
    menu = i['name']
    pmenu_name.append(menu)

def sold_out():
    if request.method == 'POST':
        stock_a = request.form.get("a_out")
        stock_b = request.form.get("b_out")

        if stock_a != None:
            a_soldout = db.session.query(ABMenu).filter(ABMenu.date = datetime.date.today).one_or_none
            a_soldout.a_out_of_stock = True
            db.session.commit()
        elif stock_b != None:
            b_soldout = db.session.query(ABMenu).filter(ABMenu.date = datetime.date.today).one_or_none
            b_soldout.b_out_of_stock = True
            db.session.commit()

        for i in pmenu_name:
            stock_p = request.form.get(i)
            if stock_p != None: break
        if stock_p != None:
            for i in pmenu_name:
                p_soldout = db.session.query(PermMenu).filter(PermMenu.menu = pmenu_name[i]).one_or_none
                if p_soldout != None:
                    p_soldout.out_of_stock = True
                    break
            db.session.commit()