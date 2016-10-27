#!/usr/bin/env python
# coding=utf-8

import os
import re
import sys
import json
import urllib
import urllib.request
import socket
import struct

from alfred.feedback import *


# Taobao restful query api
API = 'http://ip.taobao.com/service'

# Regular expression for a valid ip address
REGEXP_IP = r'(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)'

def query_ip(ip = None):
    '''Query the ip information with the taobao api.'''
    if ip is None: # Query the local ip instead
        url = API + '/getIpInfo2.php?ip=myip'
    else:
        url = '%s/getIpInfo.php?ip=%s' % (API, ip)
    
    try:
        res = urllib.request.urlopen(url).read()
        res = res.decode('utf-8')
        return json.loads(res)
    except Exception as e:
        err(e, '调用接口失败,请重试!')


def generate_feedback_results(ip_query):
	'''Generate the feedback results.'''
	fb = Feedback()

	if ip_query:
		ip_list = re.findall(REGEXP_IP, ip_query)
	else:
		ip_list = [None]

	for ip in ip_list:
		info = query_ip(ip)
		#print ip, info
	
	if info['code'] == 1: # query failed
		kwargs = {
			'title': u'查询 IP 地址失败',
			'subtitle': u'错误原因: %s' % info['data'],
			'valid': False
		}
	else: # query success
		data = info['data']

	title = u'%s 位于 %s %s %s' % (data['ip'], data['country'],
	data['region'], data['city'])

	if data['isp']:
		subtitle = u'运营商: %s %s' % (data['area'], data['isp'])
	else:
		subtitle = ''#None

	kwargs = {
		'title': title,
		'subtitle': subtitle,
		'arg': '%s\n%s' % (title, subtitle)
	}

	fb.addItem(**kwargs)
	fb.output()

def ip2long(ip):
    return struct.unpack("!I", socket.inet_aton(ipstr))[0]

def long2ip(ip):
    return socket.inet_ntoa(struct.pack("!I", ip))

def err(e, str):
    fb = Feedback()
    kwargs = {
        'title': '!!!发生错误!!!',
        'subtitle': str,
        'arg': '发生异常'
    }
    
    fb.addItem(**kwargs)
    fb.output()

def main():
	'''The main entry.'''
	# Note: do not use single quote here, because Alfred doesn't give choice to
	# escape a single quote.

	ip_query = "{query}"
	generate_feedback_results(ip_query)

if __name__ == '__main__':
	main()

