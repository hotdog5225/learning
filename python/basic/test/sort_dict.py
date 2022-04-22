y = [
    {
        "name": "item1",
        "score": {
            "title": 1,
            "content": 4,
        }
    },
    {
        "name": "item1",
        "score": {
            "title": 2,
            "content": 3,
        }
    }]

sort_key = "content"


def key(item):
    global sort_key
    return item["score"][sort_key]


def sort_dict_list(l):
    return sorted(l, key=key, reverse=True)


def get_value(key, l):
    return l["score"][key]


if __name__ == '__main__':
    y = sort_dict_list(y)
    print(y)

    for d in y:
        key1 = "title"
        value1 = d["score"][key1]
        key2 = "content"
        value2 = d["score"][key2]
        exp = "value1 * 0.1 + value2 * 0.2"
        key = "new_key"
        value = eval(exp)
        d["score"][key] = value

    print(y)
