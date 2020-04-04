from implementations.my_flask_synchro import flask
from implementations.my_flask_synchro.response import response
import json
from implementations.my_flask_synchro.session import session
from implementations.my_flask_synchro.request import request


# инициализация фласка
app = flask.Flask(2001)

# реализация БЛ
@app.route('/users', 'POST')
def handle_post_users():
    """
    обработка запроса на создание пользователя
    :return: объект ответа
    """

    data = {'name': request.query()['name'][0],
            'age': request.query()['age'][0]}

    session.save_data(data)
    response.set_data(204, 'Created')


@app.route('/users', 'GET')
def handle_get_users():
    """
    обработка запроса на получение всех пользователей
    :return: объект ответа
    """

    accept = request.headers.get('Accept')
    if 'text/html' == accept:
        content_type = 'text/html; charset=utf-8'
        body = '<html><head></head><body>'
        body += f'<div>Пользователи ({len(session.load_data())})</div>'
        body += '<ul>'
        for k, v in session.load_data().items():
            body += f'<li>#{k} {v["name"]}, {v["age"]}</li>'
        body += '</ul>'
        body += '</body></html>'

    elif 'application/json' == accept:
        content_type = 'application/json; charset=utf-8'
        body = json.dumps(session.load_data())

    else:
        response.set_data(406, 'Not Acceptable')
        return

    body = body.encode('utf-8')
    headers = [('Content-Type', content_type),
               ('Content-Length', len(body))]
    response.set_data(200, 'OK', headers, body)


if __name__ == '__main__':
    app.run()
