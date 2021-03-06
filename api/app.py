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
from datetime import datetime, date, timedelta
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from pprint import pprint
import falcon
from random import random, randint, randrange, choice
from collections import defaultdict


def date_to_timestamp(d) :
  return int(time.mktime(d.timetuple()))

def randomDate(start, end):
  """Get a random date between two dates"""
  stime = date_to_timestamp(start)
  etime = date_to_timestamp(end)
  ptime = stime + random() * (etime - stime)
  return datetime.fromtimestamp(ptime)

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
        
        # get 2 time range
        now1, time_range1 = get_random_time_range()
        now2, time_range2 = get_random_time_range()

        # generate a random user getting in
        height = height or (random() + 1.0)
        
        # ensure in and out time_range makes sense
        if now1 < now2:
            in_dt, out_dt = now1, now2
            in_tr, out_tr = time_range1, time_range2
            
        else:
            in_dt, out_dt = now2, now1
            in_tr, out_tr = time_range2, time_range1

        # generate random time 
        t1 = randomDate(in_dt, in_dt+timedelta(minutes=bucket))
        t2 = randomDate(out_dt, out_dt+timedelta(minutes=bucket))
        
        # set entry and exit time
        if t1 < t2:
            tin, tout = t1, t2
        else:
            tin, tout = t2, t1

        # add in and out user
        self.add((str(tin), height, 'in'), in_tr)
        self.add((str(tout), height, 'out'), out_tr)

        if verbose:
            print "new user", height, "in:", tin, "out", tout       
            
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
    ''' hardcoded bucket -> the retail one '''
    def __init__(self, org, branch, zone, device_id, range_minutes=5):
        fieldnames = ['time','height','in_out']
        BucketData.__init__(self, fieldnames, org, branch, zone, device_id, range_minutes)

    def count(self):
        ''' count in and out users '''
        def n(val):
            return len([el for el in self[time_range] if el['in_out']==val])
        return dict([(time_range, {'in':n('in'),'out':n('out')}) for time_range in self])
  
# generate fake data
rb = RetailBucket('Doyle','VRM', 'front_door', '1')
count = Count(rb)

# add n random users
for i in range(2):
    rb.add_random(max_min=10, bucket=5)

api = falcon.API()
api.add_route('/bucket', rb)  
api.add_route('/count', count)  
print "running server"   
