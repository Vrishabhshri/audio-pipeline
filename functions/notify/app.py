import os
import json
import boto3

sns = boto3.client("sns")
TOPIC_ARN = os.environ["TOPIC_ARN"]


def handler(event, context):
    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="Audio processing complete",
        Message=json.dumps(event)
    )
    return event
