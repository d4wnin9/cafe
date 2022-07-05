import json

json_open = open('AB_6_27_30.json', 'r')
json_load = json.load(json_open)

a_b_menu = []
for i in json_load:
    #[date, Am, Ap, Ac, Bm, Bp, Bc]
    date = list(i.keys())[0]

    amenu = i[date]['Aセット']['name']
    aprice = i[date]['Aセット']['price']
    acalorie = i[date]['Aセット']['calorie']

    bmenu = i[date]['Bセット']['name']
    bprice = i[date]['Bセット']['price']
    bcalorie = i[date]['Bセット']['calorie']

    menu = [date, amenu, aprice, acalorie, bmenu, bprice, bcalorie]
    a_b_menu.append(menu)

json_open2 = open('permanent.json', 'r')
json_load2 = json.load(json_open2)

parmanent_menu = []
for i in json_load2:
    menu = i['name']
    price = i['price']
    calorie = i['calorie']

    menu = f"PermMenu(menu='{menu}', price='{price}', calorie='{calorie}')"
    parmanent_menu.append(menu)

for line in parmanent_menu:
    print(line)