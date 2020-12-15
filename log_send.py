import glob
import json
import os
import requests

log_files = glob.glob('./log_post/*')
brackets = {'{': '}', '[': ']'}

stack = []
for log_file in log_files:
    with open(log_file, 'r') as f:
        read_strings = ''.join([s.strip() for s in f.readlines()])
    json_string = ''
    for string in read_strings:
        if string in brackets.keys():
            stack.append(brackets[string])
        if string in brackets.values():
            stack.pop(-1)
            if not stack:
                json_string += ','
        json_string += string



