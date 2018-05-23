import os
import re


class Tree:
    parent = None
    kids = set()
    data = None

    def __init__(self, data, parent):
        self.data = data
        self.parent = parent

    def add_child(self, child):
        self.kids = child


path = "./wiki/"

files = dict.fromkeys(os.listdir(path))

start = 'Stone_Age'
end = 'Python_(programming_language)'
regexp = re.compile(r"(?<=/wiki/)[\w()]+")


def find_child(tree, global_list):
    with open(path + tree.data, encoding='utf8') as f:

        text = f.read()
        kids = set(regexp.findall(text))
    tree_children = set()
    for x in kids:
        if x in files.keys() and x not in global_list:
            tree_children.add(Tree(x, tree))
            global_list.add(x)
    return tree_children


def build_tree(tree, global_list):
    border = find_child(tree, global_list)

    while border:
        next_level = []
        for item in border:
            if item.data != end:
                kids = find_child(item, global_list)
                next_level.extend(kids)
            else:
                return item
        border = next_level
    return None


if __name__ == '__main__':
    global_list = {start}
    tree = Tree(start, None)
    res = build_tree(tree, global_list)
    if res:
        while res.parent:
            print(res.data)
            res = res.parent
        print(res.data)
    else:
        print("Пути нет")
