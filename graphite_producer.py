import graphyte
import os
class MetricProducer(object):
    def __init__(self):
        self.graphite_host = os.getenv('GRAPHITE_HOST')

    def sanitize_string(self, origin_string):
        new_string = origin_string.replace(" ", "").replace("?", "_").replace("=", "-").replace(".", "-")
        return new_string

    def produce(self, **kwargs):
        # print(kwargs)
        # {'payload': {'result': 'success', 'request_type': 'GET', 'name': 'get_banners', 'response_time': 129.57279199999937, 'response_length': 15}, 'test_name': 'BANNERS.LOAD_TEST'}
        payload = kwargs.get("payload")
        test_name = kwargs.get("test_name")
        
        metric_response_time = "%s.%s.%s.%s.response_time" % (
            self.sanitize_string(test_name), 
            payload["request_type"], 
            self.sanitize_string(payload["name"]), 
            payload["result"]
        )
        # print(metric_response_time+ "=====>" +str(payload["response_time"]))
        metric_response_length = "%s.%s.%s.%s.response_length" % (
            self.sanitize_string(test_name), 
            payload["request_type"], 
            self.sanitize_string(payload["name"]), 
            payload["result"]
        )
        metric_resquests_count = "%s.%s.%s.%s" % (
            self.sanitize_string(test_name), 
            payload["request_type"], 
            self.sanitize_string(payload["name"]), 
            payload["result"]
        )
        # send metrics
        #graphyte.init(self.graphite_host, prefix='locust.loadtest', protocol='tcp')
        graphyte.init(self.graphite_host, prefix='locust.loadtest', protocol='udp')
        print(payload["response_time"])
        graphyte.send(metric_response_time, payload["response_time"])
        #graphyte.send(metric_response_length, payload["response_length"])
        graphyte.send(metric_resquests_count, 1)
