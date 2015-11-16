#!/usr/bin/python
''' simple interface to tretail '''
import sys
import argparse
from datetime import datetime, timedelta



parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-g','--generate', action="store_true", help='generate fake data')
parser.add_argument('--range', default=5, type=int,  help='bucket range')

class BucketData(dict):

    format_date='%Y%m%d %H:%M'
    format_date_range='-{h}:{m}'

    @classmethod
    def get_date_range(cls, range_minutes=5):
        start = datetime.now()
        stop = start+timedelta(minutes=range_minutes)
        end = cls.format_date_range.format(h=stop.hour, m=stop.min)
        return start.strftime(now, cls.format_date) + end

    def __init__(self, fieldnames, org, branch, zone, device_id, 
                 range_minutes=5):
        ''' bucket data object; rdata['20150907-1200:1205']'''
        self.fielnames = fieldnames
        self.org = org
        self.branch = branch
        self.zone = zone
        self.device_id = device_id
        self.range_minutes = range_minutes
    
    def add(self, values, date_range=None):
        ''' add values for a given time range '''
        # generate date_range
        date_range = date_range or get_date_range(self.range_minutes)
        self[date_range]=dict([(key,val) for key, val in zip(self.fieldsnames, values)])
        
      

def main(args=None):
    args = args.split(' ') if args else sys.argv[1:]
    args = parser.parse_args(args)
    if args.generate:
        pass

if __name__ == "__main__":
    main()
    
