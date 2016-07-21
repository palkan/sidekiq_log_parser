import unittest
import tempfile
import os
import sidekiq_log_parser as slp

class TestSidekiqLogParser(unittest.TestCase):
  def test_parse_line(self):
    self.assertFalse(slp.parse_line('179 <190>1 2016-07-20T13:00:00.014845+00:00 app sidekiq.1 - - 3 TID-qowcrc7tfw DocusignStatusUpdatesJob JID-f4a644b41965843c7cf72908 INFO: start'))
    self.assertEqual(
      (
        'JID-f4a644b41965843c7cf72908',
        'TID-qowcrc7tfw',
        '2016-07-20T13:00:00.014845+00:00',
        'DocusignStatusUpdatesJob',
        'done',
        '0.3'
      ),
      slp.parse_line('179 <190>1 2016-07-20T13:00:00.014845+00:00 app sidekiq.1 - - 3 TID-qowcrc7tfw DocusignStatusUpdatesJob JID-f4a644b41965843c7cf72908 INFO: done: 0.3 sec '))
    self.assertEqual(
      (
        'JID-f4a644b41965843c7cf72908',
        'TID-qowcrc7tfw',
        '2016-07-20T13:00:00.014845+00:00',
        'DocusignStatus::UpdatesJob',
        'fail',
        '32'
      ),
      slp.parse_line('179 <190>1 2016-07-20T13:00:00.014845+00:00 app sidekiq.1 - - 3 TID-qowcrc7tfw DocusignStatus::UpdatesJob JID-f4a644b41965843c7cf72908 INFO: fail: 32 sec'))

  def test_process_file(self):
    input = open('test_log.txt','r')
    tmp = tempfile.mkstemp()[1]
    output = open(tmp, 'w')
    slp.process_file(input, output)
    input.close()
    output.close()
    gold_file = open('test_log_gold.txt','r')
    expected = gold_file.read().rstrip('\n\t')
    gold_file.close()
    res_file = open(tmp)
    result = res_file.read().rstrip('\n\t')
    res_file.close()
    self.assertEqual(expected,result)
  
if __name__ == '__main__':
    unittest.main()