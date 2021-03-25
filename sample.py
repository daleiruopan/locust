from custom_locust import CustomLocust
from locust import TaskSet, task, constant, between

import json
import os
import random

class UserBehavior(TaskSet):
    @task
    def get_google(self):
        self.client.get(
            "",
            name="get_local"
        )

class MyLocust(CustomLocust):
    host = "http://127.0.0.1"
    tasks = [UserBehavior]
    wait_time = between(1, 1)

    CustomLocust.test_name="SAMPLE.LOAD_TEST"
