
from locust import HttpUser, events
from graphite_producer import MetricProducer
from helpers import DBForwarder

import gevent
import graphyte
import json
import os
import socket
# import threading


class CustomLocust(HttpUser):
    test_name = "LocustTest"
    metrics = True
    abstract = True
    forwarder = DBForwarder()
    graphite = MetricProducer()
    forwarder.add_backend(graphite)
    gevent.spawn(forwarder.run)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # return if metrics is not True
        if not self.metrics:
            return

        self.test_name = self.test_name.replace(" ", ".")

        events.request_success.add_listener(self.__success_hook)
        events.request_failure.add_listener(self.__failure_hook)
        events.quitting.add_listener(self.__quitting)

    def __success_hook(self, request_type, name, response_time, response_length):
        OK_TEMPLATE = '{"result": "success", "request_type":"%s", "name":"%s", ' \
                  '"response_time":%s, "response_length":%s}'

        json_string = OK_TEMPLATE % (request_type, name, response_time, response_length)
        message = {"payload": json.loads(json_string), "test_name": self.test_name}
        self.forwarder.add(message)

    def __failure_hook(self, request_type, name, response_time, exception, response_length):
        ERR_TEMPLATE = '{"result": "failure","request_type":"%s", "name":"%s", ' \
                       '"response_time":%s, "exception":"%s"}'
        json_string = ERR_TEMPLATE % (request_type, name, response_time, exception)
        message = {"payload": json.loads(json_string), "test_name": self.test_name}
        self.forwarder.add(message)

    def __quitting(self, environment):
        pass
