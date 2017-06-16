#!/usr/bin/env python
#coding: utf-8
import sys,os
import urllib.request, urllib.parse, urllib.error,urllib.request,urllib.error,urllib.parse
import base64
import hmac
import hashlib
from hashlib import sha1
import time
import uuid
import json
access_key_id = 'LTAIQUNefOkV72rR';
access_key_secret = 'Mcse8AAI0UBqgjuvUj9z3k8u4yAAUT';
server_address = 'https://sms.aliyuncs.com'
#定义参数
user_params = {'Action': 'SingleSendSms', 'ParamString': '{"code":"1111","product":"PRODUCTNAME"}', 'RecNum': 'PHONENUMBER','SignName': 'SIGNNAME','TemplateCode': 'SMS_48465100' }

def percent_encode(encodeStr):
    encodeStr = str(encodeStr)
    res = urllib.parse.quote(encodeStr.encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res

def compute_signature(parameters, access_key_secret):
    sortedParameters = sorted(list(parameters.items()), key=lambda parameters: parameters[0])
    canonicalizedQueryString = ''
    for (k,v) in sortedParameters:
        canonicalizedQueryString += '&' + percent_encode(k) + '=' + percent_encode(v)
    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])
    print("stringToSign:  "+stringToSign)
    h = hmac.new(b"Mcse8AAI0UBqgjuvUj9z3k8u4yAAUT&", stringToSign.encode('utf-8'), sha1)
    signature = base64.encodestring(h.digest()).strip()
    return signature


def compose_url(user_params):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
    parameters = { \
            'Format'        : 'JSON', \
            'Version'       : '2016-09-27', \
            'AccessKeyId'   : access_key_id, \
            'SignatureVersion'  : '1.0', \
            'SignatureMethod'   : 'HMAC-SHA1', \
            'SignatureNonce'    : str(uuid.uuid1()), \
            'RegionId': 'cn-hangzhou',
            'Timestamp'     : timestamp\
    }
    for key in list(user_params.keys()):
        parameters[key] = user_params[key]
    signature = compute_signature(parameters, access_key_secret)
    parameters['Signature'] = signature
    url = server_address + "/?" + urllib.parse.urlencode(parameters)
    return url


def make_request(user_params, quiet=False):
        url = compose_url(user_params)
        request = urllib.request.Request(url)
        try:
            context = ssl._create_unverified_context()
            conn = urllib.request.urlopen(request, context=context)
            response = conn.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            print((e.read().strip()))
            raise SystemExit(e)
        try:
            obj = json.loads(response)
            if quiet:
                return obj
        except ValueError as e:
            raise SystemExit(e)
        json.dump(obj, sys.stdout, sort_keys=True, indent=2)
        sys.stdout.write('\n')


print(sys.stdin.encoding)
make_request(user_params)
