from implementations.my_flask_thread import flask
from implementations.my_flask_thread.response import Response
import json
from implementations.my_flask_thread.session import session
from datetime import datetime


# инициализация фласка
app = flask.Flask(2000)

# реализация БЛ
@app.route('/users', 'POST')
def handle_post_users(request):
    """
    обработка запроса на создание пользователя
    :request: объект запроса, будет автоматически вставляться фласком
    :return: объект ответа
    """

    print(f'in handle function')

    data = {'name': request.query()['name'][0],
            'age': request.query()['age'][0]}
    
    print(f'start save data {datetime.now().time()}')
    session.save_data(data)
    print(f'finish save data {datetime.now().time()}')
    response = Response()
    response.set_data(204, 'Created')
    return response


@app.route('/users', 'GET')
def handle_get_users(request):
    """
    обработка запроса на получение всех пользователей
    :request: объект запроса, будет автоматически вставляться фласком
    :return: объект ответа
    """

    response = Response()

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
        return response

    body = body.encode('utf-8')
    headers = [('Content-Type', content_type),
               ('Content-Length', len(body))]
    response.set_data(200, 'OK', headers, body)
    return response


if __name__ == '__main__':
    app.run()
