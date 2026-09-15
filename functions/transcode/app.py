import subprocess
import os
import boto3

s3 = boto3.client("s3")


def handler(event, context):
    bucket, key = event["bucket"], event["fileId"]
    local_in = "/tmp/in_audio"
    local_out = "/tmp/out_128k.mp3"
    s3.download_file(bucket, key, local_in)

    subprocess.run(
        ["/opt/bin/ffmpeg", "-y", "-i", local_in, "-b:a", "128k", local_out],
        check=True
    )

    out_key = f"processed/{os.path.basename(key)}_128k.mp3"
    s3.upload_file(local_out, bucket, out_key)
    return {**event, "transcodedKey": out_key}
