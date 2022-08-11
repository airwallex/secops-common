import json

from secops_common.logsetup import logger
from os import environ


def serialize(obj):
    return json.dumps(obj)


def deserialize_str(s):
    with_double = s.replace("'", '"')
    return json.loads(with_double)


def deserialize(bs):
    return deserialize_str(bs.decode('utf8'))


# Persisting items as a json lines file
def save_json_file(items, dest):
    f = open(dest, 'a')
    try:
        for obj in items:
            f.write(serialize(obj) + "\n")
    finally:
        f.close()


def file_deserialize(bs):
    decoded = bs.decode('utf8').replace("\'", '').replace('\\\\', '').replace(
        '\\"', '').replace("'", '"')
    return json.loads(decoded)


def file_lines_deserialize(filename):
    with open(filename) as file:
        lines = file.readlines()
        return [deserialize(str.encode(line.rstrip())) for line in lines]


# Checking if we are running in the context of a cloud function
def is_function():
    return environ.get('FUNCTION_TARGET') is not None
