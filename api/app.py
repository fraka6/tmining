#!/usr/bin/python
''' simple interface to simulate or use RetailBucket API 
    how to run it: 
      1) gunicorn app:api
      2) http GET localhost:8000/bucket
      3) http GET localhost:8000/count
    
    ** leveraging falcon http://falcon.readthedocs.org/en/latest/user/install.html#install '''
import sys
import argparse
import time
from datetime import datetime, timedelta
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pprint import pprint
import falcon
from random import random, randint, randrange, choice
from collections import defaultdict

class BucketData(defaultdict):
    ''' general BucketData class '''
    format_date='%Y%m%d %H:%M'
    format_date_range='-%H:%M'

    @classmethod
    def get_time_range(cls, start=None, range_minutes=5):
        ''' get time range '''
        start = start or datetime.now()
        stop = start+timedelta(minutes=range_minutes)
        return start.strftime(cls.format_date) + stop.strftime(cls.format_date_range)

    def __init__(self, fieldnames, org, branch, zone, device_id, 
                 range_minutes=5):
        ''' bucket data object; rdata['20150907-1200:1205'] '''
        super(BucketData, self).__init__(lambda:[])
        self.fieldnames = fieldnames
        self.org = org
        self.branch = branch
        self.zone = zone
        self.device_id = device_id
        self.range_minutes = range_minutes
    
    def add(self, values, date_range=None):
        ''' add values for a given time range '''
        # generate date_range
        date_range = date_range or BucketData.get_time_range(range_minutes=self.range_minutes)
        self[date_range].append(dict([(key,val) for key, val in zip(self.fieldnames, values)]))            
        
    def add_random(self, height=None, max_min=60, bucket=5, verbose=True):
        ''' add random user entering and exiting '''
    
        now = datetime.now()

        def get_random_time_range():
            delta = randint(0, max_min)
            delta =  delta - (delta % bucket)
            now_delta = datetime(now.year, now.month, now.day, now.hour) + timedelta(minutes=delta)
            return now_delta, self.get_time_range(now_delta)
        
        now1, time_range1 = get_random_time_range()
        now2, time_range2 = get_random_time_range()

        height = height or (random() + 1.0)
        
        if now1 < now2:
            in_dt, out_dt = now1, now2
            in_tr, out_tr = time_range1, time_range2
        else:
            in_dt, out_dt = now2, now1
            in_tr, out_tr = time_range2, time_range1
         
        # add in and out user
        self.add((in_tr, height, 'in'), in_tr)
        self.add((out_tr, height, 'out'), out_tr)

        if verbose:
            print "new user", height, "in:", in_tr, "out", out_tr       
            
    def filter_bucket(bucket, key, val):
        return dict([(key, el) for key, el in bucket.items() if el[key]==val])
    
    def count(self, constraint=None):
        ''' count nb of people entering each time bucket period;
            constraint = (key, val) '''
        key,val = contraint if constraint else None, None
                
        if constraint:
            return dict([(time_range, len(self.filter_bucket(self[time_range], key, val))) for time_range, el in self.items()])
        else:
            return dict([(time_range, len(self[time_range])) for time_range in self])
    
    def on_get(self, req, resp):
        resp.body = json.dumps(self)
        resp.status = falcon.HTTP_200

class Count:
    def __init__(self, bucket):
        self.bucket = bucket
        
    def on_get(self, req, resp):
        resp.body = json.dumps(self.bucket.count())
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
now =  datetime.now() 
time_range = BucketData.get_time_range(now)
values = (time_range, 1.76, 'in')
rb = RetailBucket.create('Doyle','VRM', 'front_door', '1', values)
count = Count(rb)
now+=timedelta(minutes=3)
time_range = BucketData.get_time_range(now)
values = (time_range, 1.76, 'out')
rb.add(values, time_range)
# add 10 random users
for i in range(10):
    rb.add_random()

api = falcon.API()
api.add_route('/bucket', rb)  
api.add_route('/count', count)  
print "running server"   
