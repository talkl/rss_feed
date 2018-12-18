from bottle import route, run, static_file, template, request, response, HTTPResponse
import json
import feedparser
import datetime


# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers[
            'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


@route('/path/to/your/endpoint', method=['OPTIONS', 'GET'])
@enable_cors
def get_users():
    response_body = json.dumps({'key': 'value'})
    return HTTPResponse(body=response_body, status=200,
                        headers={'Content-type': 'application/json', 'Access-Control-Allow-Origin': '*',
                                 'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS',
                                 'Access-Control-Allow-Headers': 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'})


@route('/css/<filename:re:.*\.css>')
def css(filename):
    return static_file(filename, root='./css')


@route('/js/<filename:re:.*\.js>')
def js(filename):
    return static_file(filename, root='./js')


@route('/media/<filename:re:.*\.(jpg|png|gif|ico)>')
def media(filename):
    return static_file(filename, root='./media')


rss_options = {
    'jpost': 'https://www.jpost.com/Rss/RssFeedsHeadlines.aspx',
    'wallstreetj': 'http://online.wsj.com/xml/rss/3_7011.xml',
    'dmail': 'http://www.dailymail.co.uk/articles.rss',
    'fifa': 'http://www.fifa.com/rss/index.xml'
}


@route('/get_rss_feed', method=['OPTIONS', "GET"])
@enable_cors
def get_rss():
    selected_rss_by_user = request.query['rss']
    response.headers['Content-type'] = 'application/json'
    feed = feedparser.parse(rss_options[selected_rss_by_user])
    feed_result = []
    for entry in feed['entries']:
        feed_result.append({
            'title': entry['title'],
            'link': entry['link'],
        })
    return json.dumps(feed_result)


@route('/refresh_rss_feed', method=['OPTIONS', "GET"])
@enable_cors
def refresh_rss():
    selected_rss_by_user = request.query['rss']
    if request.get_cookie("refresh_time", secret='refresh-password'):
        refresh_time = str(datetime.datetime.now())
        print(refresh_time)
        response.set_cookie("refresh_time", refresh_time, secret='refresh-password')
    else:
        refresh_time = str(datetime.datetime.now())
        print(refresh_time)
        response.set_cookie("refresh_time", refresh_time, secret='refresh-password')
        print('got here')
    response.headers['Content-type'] = 'application/json'
    feed = feedparser.parse(rss_options[selected_rss_by_user])
    feed_result = []
    for entry in feed['entries']:
        feed_result.append({
            'title': entry['title'],
            'link': entry['link'],
        })
    return json.dumps({'headlines': feed_result, 'refresh': refresh_time})


@route('/', method=['OPTIONS', "GET"])
@enable_cors
def index():
    return template("index.html")


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
