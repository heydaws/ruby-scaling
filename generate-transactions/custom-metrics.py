import json
import logging
import boto3
import datetime
from botocore.exceptions import ClientError

cloudwatch = boto3.client('cloudwatch')
sqs_client = boto3.client('sqs')


def publish_metric(value):
    
    # Send the SQS message
    try:
        response = cloudwatch.put_metric_data(
            MetricData = [
                {
                    'MetricName': 'NumMessagesCreated',
                    'Dimensions': [
                        {
                            'Name': 'MessageSource',
                            'Value': 'Lambda'
                        }
                    ],
                    'Unit': 'None',
                    'Value': value
                },
            ],
            Namespace='BeanstalkScaling'
        )
    except ClientError as e:
        logging.error(e)
        return None
    return response
    
    
def send_sqs_message(QueueUrl, msg_body):
    """
    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_body: String message body
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """

    # Send the SQS message
    try:
        msg = sqs_client.send_message(QueueUrl=QueueUrl,
                                      MessageBody=json.dumps(msg_body))
    except ClientError as e:
        logging.error(e)
        return None
    return msg
    
def lambda_handler(event, context):
    """Exercise send_sqs_message()"""

    QueueUrl = 'https://sqs.us-west-2.amazonaws.com/997023692343/awseb-e-m2t8tupwsp-stack-AWSEBWorkerQueue-ARGFQCHK1RN3'
    Duration = 10
    
    # Set up logging
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(message)s')

    # Send some SQS messages
    msgCount = 0
    endTime = datetime.datetime.now() + datetime.timedelta(minutes=Duration)
    while datetime.datetime.now() < endTime:
        msg = send_sqs_message(QueueUrl,'message ' + str(msgCount))
        msgCount = msgCount + 1
        publish_metric(msgCount)
        
        if msg is not None:
            logging.info(f'Sent SQS message ID: {msg["MessageId"]}')
    
    return {
        'statusCode': 200,
        'body': 'Sent ' + str(msgCount) + ' messages'
    }