class Node:
    def __init__(self, k, son = []):
        self.k = k
        self.son = son


def build():
    cat_list = ['phone']
    tree = {}
    for cat in cat_list:
        for line in open("sentiment_analysor/aspect_data/%s/hierarchy" % cat, "r"):
            line = line.strip().decode("utf-8")
            line = line.split(" : ")
            high = tuple(line[0].split(' '))
            low = []
            for item in line[1].split(','):
                low.append(tuple(item.split(' ')))
                tree[high] = low

        high = set(tree.keys())
        low = set([])
        for k, v in tree.items():
            low |= set(v)

        high_top = high - low
        high_bottom = list(high - high_top)
        high_top = list(high_top)
        while len(high_bottom) > 0:
            for aspect_high in high_top:
                for aspect_low in high_bottom:
                    if aspect_low in tree[aspect_high]:
                        tree[aspect_high].extend(tree[aspect_low])
                        high_bottom.remove(aspect_low)
                        tree.pop(aspect_low)

        return tree

# tree = build()
# print 1
