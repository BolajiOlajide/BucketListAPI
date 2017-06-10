"""
Define decorators for the application.

All decorators to be used in the application are defined here.
"""
from datetime import timedelta
import functools

from flask import (
    jsonify,
    wrappers,
    request,
    url_for,
    current_app,
    make_response
)


def json(f):
    """
    Modify result of passed in function to return pretty printed JSON.

    Courtesy - Miguel Grinberg
    """
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        response = f(*args, **kwargs)
        status = None

        # extract status code
        if isinstance(response, tuple):
            response, status = response

        # return result if an error occurred
        if isinstance(response, wrappers.Response) and \
                response.status_code > 300:
            return response

        # convert result to json and return
        if not isinstance(response, dict):
            response = response.to_json()
        response = jsonify(response)
        if status is not None:
            response.status_code = status
        return response
    return wrapped


def paginate():
    """
    Generate a paginated response for a resource collection.

    Routes that use this decorator must return a SQLAlchemy query as a
    response.

    The output of this decorator is a Python dictionary with the paginated
    results. The application must ensure that this result is converted to a
    response object, either by chaining another decorator or by using a
    custom response object that accepts dictionaries.

    Courtesy - Miguel Grinberg
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            # get the number of the page to be displayed from URL
            page = request.args.get('page', 1, type=int)

            # get the number of items to be displayed per page
            limit = min(request.args.get(
                'limit', current_app.config['DEFAULT_PER_PAGE'], type=int),
                current_app.config['MAX_PER_PAGE'])

            # get query, paginate the query and get content of query
            query = f(*args, **kwargs)
            pagination = query.paginate(page, limit)
            content = pagination.items

            # prepare the meta portion of the json response
            pages = {'page': page, 'limit': limit,
                     'total': pagination.total, 'pages': pagination.pages}
            if pagination.has_prev:
                pages['prev'] = url_for(request.endpoint,
                                        page=pagination.prev_num, limit=limit,
                                        _external=True, **kwargs)
            else:
                pages['prev'] = None

            if pagination.has_next:
                pages['next'] = url_for(request.endpoint,
                                        page=pagination.next_num, limit=limit,
                                        _external=True, **kwargs)
            else:
                pages['next'] = None

            pages['first'] = url_for(request.endpoint, page=1,
                                     limit=limit, _external=True,
                                     **kwargs)
            pages['last'] = url_for(request.endpoint, pages=pagination.pages,
                                    limit=limit, _external=True,
                                    **kwargs)
            return jsonify({
                'meta': pages,
                'bucketlists': [each.to_json() for each in content]
            })
        return wrapped
    return decorator


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return functools.update_wrapper(wrapped_function, f)
    return decorator
