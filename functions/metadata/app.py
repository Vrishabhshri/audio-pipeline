import os
import json
import urllib.parse
import boto3
from mutagen import File as MutagenFile

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
sfn = boto3.client("stepfunctions")

TABLE_NAME = os.environ["TABLE_NAME"]
STATE_MACHINE_ARN = os.environ["STATE_MACHINE_ARN"]

table = dynamodb.Table(TABLE_NAME)


def handler(event, context):
    record = event["Records"][0]["s3"]
    bucket = record["bucket"]["name"]
    key = urllib.parse.unquote_plus(record["object"]["key"])

    local_path = "/tmp/audio_file"
    s3.download_file(bucket, key, local_path)

    audio = MutagenFile(local_path)
    duration = audio.info.length if audio else 0
    bitrate = getattr(audio.info, "bitrate", 0) if audio else 0

    table.put_item(Item={
        "fileId": key,
        "duration": str(round(duration, 2)),
        "bitrate": str(bitrate),
        "status": "METADATA_EXTRACTED"
    })

    sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps({"bucket": bucket, "fileId": key})
    )

    return {"fileId": key, "bucket": bucket, "duration": str(round(duration, 2))}
