from urllib.parse import parse_qs


def app(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    query_string = parse_qs(environ['QUERY_STRING'])
    request_body = parse_qs(environ['wsgi.input'].read(request_body_size))

    response_body = 'GET params:\n' + str(query_string) + '\n\nPOST params:\n' + str(request_body)

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [str.encode(response_body)]
