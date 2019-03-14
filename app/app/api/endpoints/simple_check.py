# coding=utf-8

import copy

from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify

RESULT = {
    'code': 0,
    'message': 'Success',
    'data': {}
}

# from .tasks import calling_api
from ...task import calling_api


def send_data():
    result = copy.deepcopy(RESULT)

    ret = request.get_json()
    print("request.get_json():", ret)
    url = ret.get("url")
    if url is not None:
        print("url:", url)
        # outcome = calling_api.apply_async(args=[url], countdown=60)
        outcome = calling_api.apply_async(args=[url])
        # outcome = calling_api.delay(url)
        print("outcome:", outcome)
        print("outcome type:", type(outcome))
        print("outcome dict:", type(outcome.__dict__()))

        outcome_dict = {}
        outcome['task_id'] = str(outcome)
        result['data'] = outcome_dict

    else:
        result['code'] = 1
        result['message'] = "failed"

    return jsonify(result)


def get_data(task_id):
    result = copy.deepcopy(RESULT)
    task = calling_api.AsyncResult(task_id)
    # task = calling_api.AsyncResult(task_id)

    task_id = "{0}".format(task.id)
    print(type(task_id), task_id)

    if task.status == 'SUCCESS':
        print("OK")
        result_dict = {}
        result_dict["status"] = task.status
        result_dict["ready"] = task.ready()
        result_dict["result"] = task.result
        result_dict["state"] = task.state
        result_dict["id"] = task.id
        result['data'] = result_dict
    else:
        result['code'] = 1

    return jsonify(result)
