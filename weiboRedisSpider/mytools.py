import json
import time


def convert_responsebody_to_json(response):
    '''
    将response转换为json
    '''
    return json.dumps(json.loads(response.body), ensure_ascii=False)


def write_raw_data_to_file(string, filename):
    with open(filename, "a", encoding='utf-8') as f:
        f.write(str(string))
        f.write("\n")


def write_json_data_to_file(response, filename):
    with open(filename, "a", encoding='utf-8') as f:
        f.write(json.dumps(json.loads(response.body), ensure_ascii=False))
        f.write("\n")


def write_parsed_json_data_to_file(item, filename):
    with open(filename, "a", encoding='utf-8') as f:
        f.write(json.dumps(dict(item), ensure_ascii=False))
        f.write("\n")


def convert_timestamp(str):
    return int(time.mktime(time.strptime(str, "%Y-%m-%d %H:%M:%S")))
