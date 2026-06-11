import boto3
import json
import urllib.parse

sns_client = boto3.client("sns")

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:ImageUploadNotification"


def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        size = record["s3"]["object"]["size"]

        message = (
            f"New image uploaded!\n"
            f"  Bucket : {bucket}\n"
            f"  File   : {key}\n"
            f"  Size   : {size} bytes"
        )

        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Image Upload Notification",
            Message=message,
        )

        print(f"Published SNS message: {response['MessageId']} | {key}")

    return {"statusCode": 200, "body": json.dumps("Notification sent successfully")}
