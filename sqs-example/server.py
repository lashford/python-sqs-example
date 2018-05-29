from sqsClient import SQSClient
from random import *

def main():
    """ A Simple example of using the SQS Client library. """
    try:
        sqs = SQSClient('http://localhost:4576')

        print('Create Queue')
        queue_name = "TEST_QUEUE"
        queue_url = sqs.create_queue('TEST_QUEUE')

        print('Send Message')
        body = 'Some Awesome message {0}'.format(randint(1, 1000))
        sqs.send_message(queue_url, body)

        print('Consume Message')
        msg = sqs.consume_next_message(queue_url)

        print('Compare Messages')
        if msg['Body'] != body:
            print('ERROR: These two values should be equal {0} {1}'.format(msg['Body'], body))
        else:
            msg_id = msg['MessageId']
            print("Message ID -> %s" % msg_id)

            receipt_handle = msg['ReceiptHandle']
            print("Receipt Handle -> %s" % receipt_handle)
            
            print('Delete Message')
            sqs.delete_message(queue_url, receipt_handle)

            print('Delete Queue')
            sqs.delete_queue(queue_url)
    except Exception as e:
        print("Something went wrong %s" % e)
        raise
