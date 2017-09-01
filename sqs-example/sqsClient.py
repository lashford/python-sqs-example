import boto3
from botocore.exceptions import ClientError

class SQSClient:
    """ An abstraction over the AWS SQS api, allowing for simple consumption of SQS """

    def __init__(self, endpoint_url, region='us-east-1'):

        # Initialise Boto3 Session
        session = boto3.session.Session()

        # FIXME:
        #      AWS Creds should either be provided by config file
        #      i.e ~/.aws/credentails or as environment variables.
        #      As we are currently testing with localStack any keys will do.

        # Initialise SQS client
        self.sqs = session.client(
            'sqs',
            region_name=region,
            endpoint_url=endpoint_url,
            aws_access_key_id='ACCESS_KEY',
            aws_secret_access_key='SECRET_KEY',
            aws_session_token='SESSION_TOKEN',
        )
        print("SQSClient Initialised")

    def create_queue(self, name):
        """ Create Queue in SQS, returning the QueueURL """
        response = self.sqs.create_queue(
            QueueName=name,
            Attributes={
                'DelaySeconds': '60',
                'MessageRetentionPeriod': '86400'
            }
        )
        print("QueueCreated -> %s" % response)
        queue_url = response['QueueUrl']
        return queue_url

    def delete_queue(self, queue_url):
        """ Delete the queue, given the following URL """
        response = self.sqs.delete_queue(QueueUrl=queue_url)
        print("Deleted Queue -> %s" % queue_url)
        return ("Queue at URL {0} deleted").format(queue_url)

    def send_message(self, queue_url, body):
        """ Send message to the specified SQS queue """
        response = self.sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=body,
        )
        msg_id = response['MessageId']
        print("Message ID -> %s" % msg_id)
        return "msg_id"

    def consume_next_message(self, queue_url):
        """ Receive Message from Queue """
        response = self.sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[""],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=10, # FIXME This timeout needs some more thought!!!
        )
        message = response['Messages'][0] # we only wnat the first message.
        print("Message -> %s" % message)
        return message

    def delete_message(self, queue_url, receipt_handle):
        """ delete Message from Queue given receipt_handle """
        try:
            self.sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                print("Queue does not exist, nothing to do")
            else:
                print("Unexpected error: %s" % e)
                raise

        return "deleted :  {0}".format(receipt_handle)
