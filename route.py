from flask import Flask

import view


def add_route(app: Flask):
    # index
    app.add_url_rule('/', 'index', view.index, methods=['GET', 'POST'])

    # login
    app.add_url_rule('/login', 'login', view.login, methods=['GET','POST'])

    # register
    app.add_url_rule('/register', 'register', view.register, methods=['GET','POST'])

    # logout
    app.add_url_rule('/logout', 'logout', view.logout)

    # history
    app.add_url_rule('/history', 'history', view.history)


    # set menu
    app.add_url_rule('/set-menu', 'set_menu', view.set_menu)

    # delete menu
    app.add_url_rule('/delete-menu', 'delete_menu', view.delete_menu)

    # delete user
    app.add_url_rule('/delete-user', 'delete_user', view.delete_user)
