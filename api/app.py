#!/usr/bin/python
''' simple interface to simulate or use RetailBucket 
    how to run it: 
      1) gunicorn app:api
      2) http GET localhost:8000/bucket
    
    ** leveraging falcon http://falcon.readthedocs.org/en/latest/user/install.html#install '''
import sys
import argparse
import time
from datetime import datetime, timedelta
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pprint import pprint
import falcon

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
    
    def on_get(self, req, resp):
        resp.body = self.json()
        resp.status = falcon.HTTP_200

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
    
# generate fake data
time_range = BucketData.get_time_range()
values = (time_range, 1.76, 'in')
rb = RetailBucket.create('Doyle','VRM', 'front_door', '1', values)

api = falcon.API()
api.add_route('/bucket', rb)  
print "running server"   
