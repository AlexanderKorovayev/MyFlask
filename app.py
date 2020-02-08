from implementations.my_flask import flask
from interfaces.i_response import Response
import json
from implementations.my_flask.simple_data_worker import SimpleDataWorker
from interfaces.i_data_worker import IDataWorker
from utils import check_type
from implementations.my_flask.request import Request


#TODO функции должны иметь доступ к данным  реквеста а не принимать их в аргументе. 
# во фласке вроде было сделано так что ты импортируешь этот объект и он всегда наполнен данными реквеста, надо погуглить и подумать как сделать так же


# инициализация фласка
app = flask.Flask(2001)

# проверяем подходит ли нам интерфейс работы с данными 
if not check_type(SimpleDataWorker, IDataWorker):
    raise Exception('используется некорректный интерфейс для работы с данными')

# реализация БЛ
@app.route('/users', 'POST')
def handle_post_users():
    """
    обработка запроса на создание пользователя
    :return: объект ответа
    """
    
    data = {'name': Request.query()['name'][0],
            'age': Request.query()['age'][0]}

    SimpleDataWorker.save_data(data)
    return Response(204, 'Created')


@app.route('/users', 'GET')
def handle_get_users():
    """
    обработка запроса на получение всех пользователей
    :return: объект ответа
    """
    accept = Request.headers.get('Accept')
    if 'text/html' in accept:
        content_type = 'text/html; charset=utf-8'
        body = '<html><head></head><body>'
        body += f'<div>Пользователи ({len(SimpleDataWorker.load_data())})</div>'
        print(len(SimpleDataWorker.load_data()))
        body += '<ul>'
        print(SimpleDataWorker.load_data().values())
        for u in SimpleDataWorker.load_data().values():
            body += f'<li>#{u["id"]} {u["name"]}, {u["age"]}</li>'
        body += '</ul>'
        body += '</body></html>'

    elif 'application/json' in accept:
        content_type = 'application/json; charset=utf-8'
        body = json.dumps(SimpleDataWorker.load_data())

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
