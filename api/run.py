#!/usr/bin/python
''' simple interface to tretail '''
import sys
import argparse
import time
from datetime import datetime, timedelta
import json

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-g','--generate', action="store_true", help='generate fake data')
parser.add_argument('--range', default=5, type=int,  help='bucket range')

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
        print json.dumps(self)

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


def main(args=None):
    args = args.split(' ') if args else sys.argv[1:]
    args = parser.parse_args(args)
    if args.generate:
        time_range = BucketData.get_time_range()
        values = (time_range, 1.76, 'in')
        rb = RetailBucket.create('Doyle','VRM', 'front_door', '1', values)
        print rb.json()

if __name__ == "__main__":
    main()
    
