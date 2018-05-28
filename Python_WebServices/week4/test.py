import requests

# defining the api-endpoint
API_ENDPOINT = "http://127.0.0.1:8000/routing/sum_post_method"


# your source code here
source_code = '''
print("Hello, world!")
a = 1
b = 2
print(a + b)
'''

# data to be sent to api
data = {'a': 30,
        'b': -10}

# sending post request and saving response as response object
r = requests.post(url=API_ENDPOINT, data=data)

# extracting response text
pastebin_url = r.text
print("Result: {} code {}".format(pastebin_url, r.status_code))

