from flask import Flask, render_template, request, redirect, url_for, Blueprint

from todo_app.app_config import Config
from todo_app.data import trello_items as trello
from todo_app.view_model import ViewModel


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route('/')
    def index():
        items = trello.get_items()
        return render_template('index.html', model=ViewModel(items))

    @app.route('/items/new', methods=['POST'])
    def add_item():
        name = request.form['name']
        trello.add_item(name)
        return redirect(url_for('index'))

    @app.route('/items/<item_id>/start')
    def start_item(item_id):
        trello.start_item(item_id)
        return redirect(url_for('index'))

    @app.route('/items/<item_id>/complete')
    def complete_item(item_id):
        trello.complete_item(item_id)
        return redirect(url_for('index'))

    @app.route('/items/<item_id>/uncomplete')
    def uncomplete_item(item_id):
        trello.uncomplete_item(item_id)
        return redirect(url_for('index'))

    return app

if __name__ == '__main__':
    create_app().run(debug=True)