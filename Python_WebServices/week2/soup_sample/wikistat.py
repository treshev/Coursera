import os
import re

from bs4 import BeautifulSoup


class Tree:
    parent = None
    kids = set()
    data = None

    def __init__(self, data, parent):
        self.data = data
        self.parent = parent

    def add_child(self, child):
        self.kids = child


def find_child(tree, global_list, regexp, path, files):
    with open(path + tree.data, encoding='utf8') as f:

        text = f.read()
        kids = set(regexp.findall(text))
    tree_children = set()
    for x in kids:
        if x in files.keys() and x not in global_list:
            tree_children.add(Tree(x, tree))
            global_list.add(x)
    return tree_children


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_tree(start, end, path):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    files = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}

    global_list = {start}
    tree = Tree(start, None)
    border = find_child(tree, global_list, link_re, path, files)
    result = None
    while border:
        next_level = []
        for item in border:
            if item.data != end:
                kids = find_child(item, global_list, link_re, path, files)
                next_level.extend(kids)
            else:
                result = item
                break
        border = next_level

    path_list = []
    if result:
        while result.parent:
            path_list.append(result.data)
            result = result.parent
        path_list.append(result.data)
    else:
        print("нет пути")
    return path_list


def count_links(links):
    max_len = 0
    for link in links:
        current_length = 1
        current = link
        while current.find_next_sibling() and current.find_next_sibling().name == "a":
            current_length += 1
            current = current.find_next_sibling()

        if max_len < current_length:
            max_len = current_length

    return max_len


def parse(start, end, path):
    """
    Если не получается найти список страниц bridge, через ссылки на которых можно добраться от start до end, то,
    по крайней мере, известны сами start и end, и можно распарсить хотя бы их: bridge = [end, start]. Оценка за тест,
    в этом случае, будет сильно снижена, но на минимальный проходной балл наберется, и тест будет пройден.
    Чтобы получить максимальный балл, придется искать все страницы. Удачи!
    """

    bridge = build_tree(start, end, path)  # Искать список страниц можно как угодно, даже так: bridge = [end, start]

    # Когда есть список страниц, из них нужно вытащить данные и вернуть их
    out = {}
    for file in bridge:
        imgs = 0
        headers = 0
        lists = 0

        with open("{}{}".format(path, file), encoding='utf8') as data:
            soup = BeautifulSoup(data, "lxml")

        body = soup.find(id="bodyContent")

        for img in body.find_all('img'):
            if int(img.attrs.get('width', 0)) >= 200:
                imgs += 1

        for head in body.find_all(re.compile('^h[1-6]$')):
            if head.text[:1] in 'ETC':
                headers += 1

        links = body.find_all('a')
        linkslen = count_links(links)

        all_links = body.find_all('ul')
        all_links.extend(body.find_all('ol'))
        for link in all_links:
            res = True
            for p in link.parents:
                if p.name in ['ul', 'UL', 'ol', 'OL']:
                    res = False
            if res:
                lists += 1
        out[file] = [imgs, headers, linkslen, lists]

    return out
