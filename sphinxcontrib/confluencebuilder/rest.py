# -*- coding: utf-8 -*-
"""
    sphinxcontrib.confluencebuilder.rest
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2017 by the contributors (see AUTHORS file).
    :license: BSD, see LICENSE.txt for details.
"""

from .exceptions import ConfluenceAuthenticationFailedUrlError
from .exceptions import ConfluenceBadApiError
from .exceptions import ConfluenceBadServerUrlError
from .exceptions import ConfluenceTimeoutError
import json
import requests

class Rest:
    BIND_PATH = "/rest/api/"

    def __init__(self, server_url, server_user, server_pass):
        self.url = server_url
        self.auth = None
        if server_user:
            self.auth = (server_user, server_pass)

    def get(self, key, params):
        restUrl = self.url + self.BIND_PATH + key
        if params:
            restUrl += "?" + params[0];
            for param in params[1:]:
                restUrl += "&" + param;

        try:
            rsp = requests.get(restUrl, auth=self.auth)
        except requests.exceptions.Timeout:
            raise ConfluenceTimeoutError(self.url)
        if rsp.status_code == 401:
            raise ConfluenceAuthenticationFailedUrlError
        if not rsp.ok:
            err = ""
            err += "REQ: GET\n"
            err += "RSP: " + str(rsp.status_code) + "\n"
            err += "URL: " + self.url + self.BIND_PATH + "\n"
            err += "API: " + key
            raise ConfluenceBadApiError(err)

        try:
            json_data = json.loads(rsp.content)
        except ValueError:
            raise ConfluenceBadServerUrlError(self.url,
                "REST reply did not provide valid JSON data.")

        return json_data

    def post(self, key, data):
        restUrl = self.url + self.BIND_PATH + key
        try:
            rsp = requests.post(restUrl, auth=self.auth, json=data)
        except requests.exceptions.Timeout:
            raise ConfluenceTimeoutError(self.url)
        if rsp.status_code == 401:
            raise ConfluenceAuthenticationFailedUrlError
        if not rsp.ok:
            err = ""
            err += "REQ: POST\n"
            err += "RSP: " + str(rsp.status_code) + "\n"
            err += "URL: " + self.url + self.BIND_PATH + "\n"
            err += "API: " + key
            raise ConfluenceBadApiError(err)

        try:
            json_data = json.loads(rsp.content)
        except ValueError:
            raise ConfluenceBadServerUrlError(self.url,
                "REST reply did not provide valid JSON data.")

        return json_data

    def put(self, key, value, data):
        restUrl = self.url + self.BIND_PATH + key + "/" + value
        try:
            rsp = requests.put(restUrl, auth=self.auth, json=data)
        except requests.exceptions.Timeout:
            raise ConfluenceTimeoutError(self.url)
        if rsp.status_code == 401:
            raise ConfluenceAuthenticationFailedUrlError
        if not rsp.ok:
            err = ""
            err += "REQ: PUT\n"
            err += "RSP: " + str(rsp.status_code) + "\n"
            err += "URL: " + self.url + self.BIND_PATH + "\n"
            err += "API: " + key
            raise ConfluenceBadApiError(err)

        try:
            json_data = json.loads(rsp.content)
        except ValueError:
            raise ConfluenceBadServerUrlError(self.url,
                "REST reply did not provide valid JSON data.")

        return json_data

    def delete(self, key, value):
        restUrl = self.url + self.BIND_PATH + key + "/" + value
        try:
            rsp = requests.delete(restUrl, auth=self.auth)
        except requests.exceptions.Timeout:
            raise ConfluenceTimeoutError(self.url)
        if rsp.status_code == 401:
            raise ConfluenceAuthenticationFailedUrlError
        if not rsp.ok:
            err = ""
            err += "REQ: DELETE\n"
            err += "RSP: " + str(rsp.status_code) + "\n"
            err += "URL: " + self.url + self.BIND_PATH + "\n"
            err += "API: " + key
            raise ConfluenceBadApiError(err)
