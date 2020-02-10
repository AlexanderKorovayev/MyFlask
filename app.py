from implementations.my_flask import flask
from interfaces.i_response import Response
import json
from implementations.my_flask.session import Session
from implementations.my_flask.request import Request


# инициализация фласка
app = flask.Flask(2000)

# реализация БЛ
@app.route('/users', 'POST')
def handle_post_users():
    """
    обработка запроса на создание пользователя
    :return: объект ответа
    """
    
    data = {'name': Request.query()['name'][0],
            'age': Request.query()['age'][0]}

    Session.save_data(data)
    return Response(204, 'Created')


@app.route('/users', 'GET')
def handle_get_users():
    """
    обработка запроса на получение всех пользователей
    :return: объект ответа
    """
    accept = Request.headers.get('Accept')
    if 'text/html' in accept:
        print("IN text/html")
        content_type = 'text/html; charset=utf-8'
        body = '<html><head></head><body>'
        body += f'<div>Пользователи ({len(Session.load_data())})</div>'
        print(len(Session.load_data()))
        body += '<ul>'
        print(Session.load_data().items())
        for k, v in Session.load_data().items():
            print("TEST555")
            body += f'<li>#{k} {v["name"]}, {v["age"]}</li>'
        body += '</ul>'
        body += '</body></html>'

    elif 'application/json' in accept:
        print("IN application/json")
        content_type = 'application/json; charset=utf-8'
        body = json.dumps(Session.load_data())

    else:
        print("NO ACCEPTIBLE")
        return Response(406, 'Not Acceptable')

    body = body.encode('utf-8')
    headers = [('Content-Type', content_type),
               ('Content-Length', len(body))]
    print('FINISH HANDLE GET USERS')
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
