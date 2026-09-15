# Serverless Audio Processing Pipeline (AWS SAM)

S3 upload triggers a Lambda that extracts metadata into DynamoDB and starts
a Step Functions execution, which transcodes the file, generates a waveform
image, and publishes an SNS notification. A separate HTTP API exposes a
search endpoint over the metadata table.

## Project structure

```
template.yaml              SAM template defining every resource
functions/
  metadata/app.py          S3 trigger, extracts metadata, starts the state machine
  transcode/app.py         Transcodes audio with ffmpeg
  waveform/app.py          Generates a waveform PNG with ffmpeg
  notify/app.py            Publishes the completion event to SNS
  search/app.py            Queries DynamoDB behind the HTTP API
statemachine/
  pipeline.asl.json        Step Functions definition (transcode -> waveform -> notify)
layers/ffmpeg/
  build.sh                 Fetches the ffmpeg static binary (run before first build)
```

## Prerequisites

- AWS CLI, configured (`aws configure`)
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Docker, if you want `sam build --use-container` (recommended, keeps the build environment consistent with Lambda)

## Deploy

```bash
# 1. Populate the ffmpeg layer (only needs to run once, or whenever ffmpeg needs updating)
./layers/ffmpeg/build.sh

# 2. Build
sam build

# 3. Deploy, guided mode walks you through parameters the first time
sam deploy --guided
```

When prompted, supply your email for `NotificationEmail`. Confirm the SNS
subscription email AWS sends you afterward, or you won't receive pipeline
notifications.

After deploy, `sam deploy` prints the stack outputs: the bucket name, the
search API endpoint, the state machine ARN, and the SNS topic ARN.

## Test it

```bash
aws s3 cp your-test-song.mp3 s3://<BucketName-from-outputs>/uploads/your-test-song.mp3
```

Then check:
- DynamoDB: `aws dynamodb scan --table-name AudioMetadata`
- Step Functions console: confirm an execution started and succeeded
- Your inbox: SNS notification email
- Search API: `curl "<ApiEndpoint-from-outputs>?title=your-test-song"`

## Free tier notes

- DynamoDB is provisioned at 5 RCU / 5 WCU, comfortably under the always-free 25/25 allotment.
- The HTTP API (not REST API) is used for the search endpoint, since HTTP APIs get 1 million free calls a month for your first 12 months.
- Use short test clips so the transcode and waveform Lambdas finish in a couple of seconds each.
- Run `sam delete` when you're done to tear down every resource and avoid leftover storage charges.

## Cleanup

```bash
sam delete
```
