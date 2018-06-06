import requests

MAIN_URL = "http://127.0.0.1:8000"


def main_test_body(test_cases):
    result = ""
    for method, url, status_code, body in test_cases:
        response = -1
        if method == 'get':
            response = requests.get(MAIN_URL + url)
        elif method == 'post':
            response = requests.post(MAIN_URL + url)
        elif method == 'put':
            response = requests.put(MAIN_URL + url)

        # print(response.content)

        if response.status_code != status_code or (body is not None and response.content.decode() != body):
            if body is not None:
                result += " ERROR: Method:{:4s}  URL:{:44s} Status code: {} instead {} Body:'{}'\n".format(method, url,
                                                                                                           response.status_code,
                                                                                                           status_code,
                                                                                                           body)
            else:
                result += " ERROR: Method:{:4s}  URL:{:44s} Status code: {} instead {}\n".format(method, url,
                                                                                                 response.status_code,
                                                                                                 status_code)
        else:
            if body is not None:
                result += "PASSED: Method:{:4s}  URL:{:44s} Status code: {} Body: '{}'\n".format(method, url,
                                                                                                 status_code,
                                                                                                 body)
            else:
                result += "PASSED: Method:{:4s}  URL:{:44s} Status code: {}\n".format(method, url,
                                                                                      status_code)

    return result


def test_simple_route():
    test_cases = (["get", "/routing/simple_route/", 200, ""],
                  ["get", "/routing/simple_route/blabla", 404, None],
                  ["post", "/routing/simple_route/", 405, None],
                  ["put", "/routing/simple_route/", 405, None],
                  )
    return main_test_body(test_cases)


def test_slug_route():
    test_cases = (
        ["get", "/routing/slug_route/a-1s_d2", 200, "a-1s_d2"],
        ["get", "/routing/slug_route/a-1s_d2/", 200, "a-1s_d2"],
        ["get", "/routing/slug_route/a-1Ds_d2/", 404, None],
        ["get", "/routing/slug_route/1411rwasf123412341234/", 404, None],
        ["get", "/routing/slug_route/.4/24][/", 404, None],
    )
    return main_test_body(test_cases)


def test_sum_route():
    test_cases = (
        ["get", "/routing/sum_route/1/2/", 200, "3"],
        ["get", "/routing/sum_route/1/-2/", 200, "-1"],
        ["get", "/routing/sum_route/45/12/", 200, "57"],
        ["get", "/routing/sum_route/1/b/", 404, None],
        ["get", "/routing/sum_route/a/2/", 404, None],
    )
    return main_test_body(test_cases)


def sum_get_method(url='/routing/sum_get_method/'):
    test_cases = (
        ["get", url + "?a=1&b=2", 200, "3"],
        ["get", url + "?a=1&b=-2", 200, "-1"],
        ["post", url + "?a=1&b=-2", 200, "-1"],
        ["put", url + "?a=1&b=-2", 200, "-1"],
        ["get", url + "?a=1&b=b", 400, None],
        ["get", url + "?a=a&b=2", 400, None],
        ["get", url, 400, None],
    )
    return main_test_body(test_cases)


def sum_post_method():
    test_cases = (
        ["post", "/routing/sum_post_method/", 1, 2, 200, "3"],
        ["post", "/routing/sum_post_method/", 1, -2, 200, "-1"],
        ["post", "/routing/sum_post_method/", 1, "b", 400, None],
        ["post", "/routing/sum_post_method/", "a", 2, 400, None],
        ["post", "/routing/sum_post_method/", None, None, 400, None],
        ["get", "/routing/sum_post_method/", None, None, 400, None],
    )
    result = ""
    for method, url, a, b, status_code, body in test_cases:
        data = {"a": a, "b": b}
        response = requests.post(MAIN_URL + url, data=data)
        if response.status_code == status_code and (body is None or response.content.decode() == body):
            result += "PASSED: Method:{:4s}  URL:{:28s} Params a = {} b = {} Status code: {} body {}\n".format(
                method, url,
                a, b,
                status_code,
                body)
        else:
            result += " ERROR: Method:{:4s}  URL:{:28s} Params a = {} b = {} Status code: {} instead {} body {}\n".format(
                method, url,
                a, b, response.status_code,
                status_code, body)

    response = requests.get(MAIN_URL + "/routing/sum_post_method/")
    result += str(response.status_code)
    return result


if __name__ == '__main__':
    # print(test_simple_route())
    # print(test_slug_route())
    # print(test_sum_route())
    # print(sum_get_method())
    print(sum_get_method("/template/echo/"))
    # print(sum_post_method())
