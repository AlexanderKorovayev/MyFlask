from implementations.my_flask import flask
from interfaces.i_response import Response
import json


# инициализация фласка
app = flask.Flask(2000)

@app.route('/users', 'POST')
def handle_post_users(req):
    """
    обработка запроса на создание пользователя
    :param req: объект запроса
    :return: объект ответа
    """
    user_id = len(_users) + 1
    _users[user_id] = {'id': user_id,
                            'name': req.query['name'][0],
                            'age': req.query['age'][0]}
    return Response(204, 'Created')

@app.route('/users', 'GET')
def handle_get_users(self, req):
    """
    обработка запроса на получение всех пользователей
    :param req: объект запроса
    :return: объект ответа
    """
    accept = req.headers.get('Accept')
    if 'text/html' in accept:
        content_type = 'text/html; charset=utf-8'
        body = '<html><head></head><body>'
        body += f'<div>Пользователи ({len(self._users)})</div>'
        body += '<ul>'
        for u in self._users.values():
            body += f'<li>#{u["id"]} {u["name"]}, {u["age"]}</li>'
        body += '</ul>'
        body += '</body></html>'

    elif 'application/json' in accept:
        content_type = 'application/json; charset=utf-8'
        body = json.dumps(self._users)

    else:
        return Response(406, 'Not Acceptable')

    body = body.encode('utf-8')
    headers = [('Content-Type', content_type),
                ('Content-Length', len(body))]
    return Response(200, 'OK', headers, body)

# как реализовать это пока хз
'''
if req.path.startswith('/users/'):
            user_id = req.path[len('/users/'):]
            if user_id.isdigit():
                return self.handle_get_user(req, user_id)
def handle_get_user(self, req, user_id):
    """
    бработка запроса на получение пользоватедя по id
    :param req: объект запроса
    :param user_id: id пользователя
    :return: объект запроса
    """
    user = self._users.get(int(user_id))
    if not user:
        raise HTTPError(404, 'Not found')

    accept = req.headers.get('Accept')
    if 'text/html' in accept:
        contentType = 'text/html; charset=utf-8'
        body = '<html><head></head><body>'
        body += f'#{user["id"]} {user["name"]}, {user["age"]}'
        body += '</body></html>'

    elif 'application/json' in accept:
        contentType = 'application/json; charset=utf-8'
        body = json.dumps(user)

    else:
        return Response(406, 'Not Acceptable')

    body = body.encode('utf-8')
    headers = [('Content-Type', contentType),
                ('Content-Length', len(body))]
    return Response(200, 'OK', headers, body)
'''

if __name__ == '__main__':
    app.run()
