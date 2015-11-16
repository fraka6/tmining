#!/usr/bin/python
''' simple interface to simulate or use RetailBucket '''
import sys
import argparse
import time
from datetime import datetime, timedelta
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pprint import pprint

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-g','--generate', action="store_true", help='generate fake data')
parser.add_argument('-r', '--range', default=5, type=int,  help='bucket range')
parser.add_argument('-u', '--url', default="http://localhost", help="url on which to to post data")
parser.add_argument('-p', '--port', default=8080, type=int, help="port #")
parser.add_argument('--post', action="store_true", help="post data on the server")
parser.add_argument('--server', action="store_true", help="activate server")

class BucketData(dict):
    ''' general BucketData class '''
    format_date='%Y%m%d %H:%M'
    format_date_range='-{h}:{m}'

    @classmethod
    def get_time_range(cls, range_minutes=5):
        start = datetime.now()
        stop = start+timedelta(minutes=range_minutes)
        end = cls.format_date_range.format(h=stop.hour, m=stop.minute)
        return start.strftime(cls.format_date) + end

    def __init__(self, fieldnames, org, branch, zone, device_id, 
                 range_minutes=5):
        ''' bucket data object; rdata['20150907-1200:1205'] '''
        self.fieldnames = fieldnames
        self.org = org
        self.branch = branch
        self.zone = zone
        self.device_id = device_id
        self.range_minutes = range_minutes
    
    def add(self, values, date_range=None):
        ''' add values for a given time range '''
        # generate date_range
        date_range = date_range or BucketData.get_time_range(self.range_minutes)
        self[date_range]=dict([(key,val) for key, val in zip(self.fieldnames, values)])
    
    def json(self):
        data = {'data':self}
        print json.dumps(data)

class RetailBucket(BucketData):
    def __init__(self, org, branch, zone, device_id, range_minutes=5):
        fieldnames = ['time_range','height','in_out']
        BucketData.__init__(self, fieldnames, org, branch, zone, device_id, range_minutes)
    
    @classmethod
    def create(cls, org, branch, zone, device_id, values, date_range=None, 
               range_minutes=5):
        rb = RetailBucket(org, branch, zone, device_id, range_minutes)
        rb.add(values, date_range)
        return rb

class PostHandler(BaseHTTPRequestHandler):
    def do_POST(s):
        """Respond to a POST request."""
        s.send_response(200)
        pprint (type(s.request))

def main(args=None):
    args = args.split(' ') if args else sys.argv[1:]
    args = parser.parse_args(args)

    # generate fake data
    time_range = BucketData.get_time_range()
    values = (time_range, 1.76, 'in')
    rb = RetailBucket.create('Doyle','VRM', 'front_door', '1', values)

    if args.generate:
        print rb.json()

    if args.post:
        from urlparse import urlparse
        from httplib import HTTPConnection
        urlparts = urlparse(args.url)
        conn = HTTPConnection(urlparts.netloc, urlparts.port or args.port)
        conn.request("POST", urlparts.path, rb.json())
        resp = conn.getresponse()
        body = resp.read()

    if args.server:
        print('http server is starting...')
        #ip and port of server
        server_address = ('127.0.0.1', args.port)
        httpd = HTTPServer(server_address, PostHandler)#BaseHTTPRequestHandler)
        print('http server is running...listening on port %s' %args.port)
        httpd.serve_forever()
    
if __name__ == "__main__":
    main()
    
