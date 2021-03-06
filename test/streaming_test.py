import os
import unittest
import logging
import time
import uuid

from subprocess import Popen, PIPE
from signalrcore.hub_connection_builder import HubConnectionBuilder
from test.base_test_case import BaseTestCase, Urls

class TestSendMethod(BaseTestCase):
    server_url = Urls.server_url_ssl
    received = False
    items = list(range(0,10))

    def on_complete(self, x):
        self.complete = True
    
    def on_error(self, x):
        raise ValueError(x)

    def on_next(self, x):
        item = self.items[0]
        self.items = self.items[1:]
        self.assertEqual(x, item)

    def test_stream(self):
        self.complete = False
        self.items = list(range(0,10))
        self.connection.stream(
            "Counter",
            [len(self.items), 500]).subscribe({
                "next": self.on_next,
                "complete": self.on_complete,
                "error": self.on_error
            })
        while not self.complete:
            time.sleep(0.1)

class TestSendNoSslMethod(TestSendMethod):
    server_url = Urls.server_url_no_ssl