from implementations.my_flask_asyncio import flask
from implementations.my_flask_asyncio.response import Response
import json
from implementations.my_flask_asyncio.session import session
import asyncio
from datetime import datetime


# инициализация фласка
app = flask.Flask(2000)

# реализация БЛ
@app.route('/users', 'POST')
async def handle_post_users(request):
    """
    обработка запроса на создание пользователя
    :request: объект запроса, будет автоматически вставляться фласком
    :return: объект ответа
    """

    data = {'name': request.query()['name'][0],
            'age': request.query()['age'][0]}

    await session.save_data(data)
    response = Response()
    response.set_data(204, 'Created')
    return response


@app.route('/users', 'GET')
async def handle_get_users(request):
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
        body += f'<div>Пользователи ({len(await session.load_data())})</div>'
        body += '<ul>'
        items = await session.load_data()
        for k, v in items.items():
            body += f'<li>#{k} {v["name"]}, {v["age"]}</li>'
        body += '</ul>'
        body += '</body></html>'

    elif 'application/json' == accept:
        content_type = 'application/json; charset=utf-8'
        body = json.dumps(await session.load_data())

    else:
        response.set_data(406, 'Not Acceptable')
        return response

    body = body.encode('utf-8')
    headers = [('Content-Type', content_type),
               ('Content-Length', len(body))]
    response.set_data(200, 'OK', headers, body)
    return response


if __name__ == '__main__':
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        print('finish server')
