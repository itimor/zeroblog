# -*- coding: utf-8 -*-
# author: itimor
# description: 递归解析json

import json


def recursive_json_loads(data):
    if isinstance(data, list):
        return [recursive_json_loads(i) for i in data]
    elif isinstance(data, tuple):
        return tuple([recursive_json_loads(i) for i in data])
    elif isinstance(data, dict):
        return {recursive_json_loads(k): recursive_json_loads(data[k]) for k in data.keys()}
    else:
        try:
            obj = json.loads(data)
            if obj == data:
                return data
        except:
            return data
        return recursive_json_loads(obj)


if __name__ == '__main__':
    a = {'aa': 123}
    p = recursive_json_loads(a)
    print(a)
