import os
from bs4 import BeautifulSoup


class Node:
    parent = None
    kids = []

    def __init__(self, parent, kids):
        self.parent = parent
        self.kids = kids


class Tree:
    def __init__(self, root):
        self.top = root


path = "./wiki/"

files = dict.fromkeys(os.listdir(path))

start = 'Stone_Age'
end = 'Python_(programming_language)'


with open(path + start) as f:
    soap = BeautifulSoup(f, 'lxml')

    children = [x["href"] for x in soap.find_all('a', href=True, class_=None) if x["href"].startswith("/wiki/")]
    print(children)
