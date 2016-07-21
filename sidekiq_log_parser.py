#coding: utf-8

import sys
import os
import re
import pprint
import argparse
import string

DELIMETER = ';'

def process_file(input_file, output_file):
  
  """
    Read input file line by line and write result to output file.

    Input file contains Sidekiq logs from Heroku (LogEntries):

    PREFIX TIMESTAMP ROLE DYNO - - PID TID JOB JID MESSAGE
  
    PREFIX ~ "143 <190>1"
    ROLE - "app"
    DYNO ~ /sidekiq\.\d+/
    TIMESTAMP ~ "2016-01-20T11:51:34.485Z"
    PID - int
    TID ~ TID-ox81qj6a8
    JOB ~ /[\w\:]+/
    JID ~ "JID-070b7183a0435ff1506783ef"
    MESSAGE -> "INFO: <STATUS>"
    STATUS -> "start" | "done: <DURATION>"
    DURATION -> "<float> sec"
  
    Output file contains JID, TID, JOB, TIMESTAMP, DURATION only for done jobs.
    
    Args:
      input_file: input file object
      output_file: output file object
  """
  
  for line in input_file:
    data = parse_line(line) 
    if data:
      output_file.write(string.join(data, DELIMETER))
      output_file.write('\n')
            
def parse_line(line):
  """
    Parse string and extract job id, thread id, timestamp, duration, status and job name.
    Return NONE if line doesn't contain information about finished job.
    Args:
      line: line to parse
  """
  matches = re.search(
    '^\d+\s+\<\d+\>\d+\s+(\d{4}\-\d{2}\-\d{2}T\d{2}\:\d{2}\:\d{2}\.\d+\+\d{2}\:\d{2})\s+\w+\s+\w+\.\d+\s+\-\s\-\s+\d+\s+(TID\-\w+)\s+([\w\:]+)\s+(JID\-\w+)\s+INFO\:\s+(fail|done)\:\s(\d+(?:\.\d+)?)\s+',
    line)
  if matches:
    return matches.group(4), matches.group(2), matches.group(1), matches.group(3), matches.group(5), matches.group(6)
  else:
    return False
  
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Proccess Sidekiq log')
  parser.add_argument('-i', dest='inputfile', type=argparse.FileType('r'), help='input file containing log', required=True)
  parser.add_argument('-o', dest='outputfile', type=argparse.FileType('w'), help='output file to write result', required=True)

  args = parser.parse_args()
  
  process_file(args.inputfile, args.outputfile)
  print('Done') 