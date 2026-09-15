import subprocess
import os
import boto3

s3 = boto3.client("s3")


def handler(event, context):
    bucket, key = event["bucket"], event["transcodedKey"]
    local_in = "/tmp/in_audio.mp3"
    local_out = "/tmp/waveform.png"
    s3.download_file(bucket, key, local_in)

    subprocess.run(
        ["/opt/bin/ffmpeg", "-y", "-i", local_in,
         "-filter_complex", "showwavespic=s=800x200",
         "-frames:v", "1", local_out],
        check=True
    )

    out_key = f"waveforms/{os.path.basename(key)}.png"
    s3.upload_file(local_out, bucket, out_key)
    return {**event, "waveformKey": out_key}
