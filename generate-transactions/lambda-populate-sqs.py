import json
import logging
import boto3
import datetime

from botocore.exceptions import ClientError

def send_sqs_message(QueueName, msg_body):
    """
    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_body: String message body
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """

    # Send the SQS message
    sqs_client = boto3.client('sqs', 'us-west-2')
    sqs_queue_url = sqs_client.get_queue_url(QueueName=QueueName)['QueueUrl']
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=json.dumps(msg_body))
    except ClientError as e:
        logging.error(e)
        return None
    return msg


def lambda_handler(event, context):
    """Exercise send_sqs_message()"""

    QueueName = 'awseb-e-bixkzhwxs8-stack-AWSEBWorkerQueue-1CI8FR4I4ZH1R'
    Duration = 1
    
    # Set up logging
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(message)s')

    # Send some SQS messages
    msgCount = 0
    endTime = datetime.datetime.now() + datetime.timedelta(minutes=Duration)
    while datetime.datetime.now() < endTime:
        msg = send_sqs_message(QueueName,'message ' + str(msgCount))
        msgCount = msgCount + 1
        if msg is not None:
            logging.info(f'Sent SQS message ID: {msg["MessageId"]}')
    
    return {
        'statusCode': 200,
        'body': 'Sent ' + str(msgCount) + ' messages'
    }