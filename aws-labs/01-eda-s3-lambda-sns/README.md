# Lab 01 — Event-Driven Architecture: S3 + Lambda + SNS

**Difficulty:** Beginner  
**AWS Services:** Amazon S3, AWS Lambda, Amazon SNS  
**Estimated time:** 30–45 min

## Use Case

When a user uploads an image to an S3 bucket, a Lambda function is triggered automatically and sends an email notification via SNS.

---

## Architecture

```
┌─────────────┐        upload         ┌──────────────────────┐
│  User/Client│ ─────────────────────▶│  S3 Bucket           │
└─────────────┘                       │  amc-eda-project-123 │
                                      └──────────┬───────────┘
                                                 │
                                   S3 Event (ObjectCreated)
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │  Lambda Function     │
                                      │  ImageUploadProcessor│
                                      └──────────┬───────────┘
                                                 │
                                    Publish to SNS Topic
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │  SNS Topic           │
                                      │  ImageUploadNotif... │
                                      └──────────┬───────────┘
                                                 │
                                      Notify Subscribers
                                                 │
                                                 ▼
                                      ┌──────────────────────┐
                                      │  Subscriber (Email)  │
                                      └──────────────────────┘
```

---

## Step 1 — Create the S3 Bucket

1. Go to **S3 → Create bucket**
2. Bucket name: `amc-eda-project-123`
3. Region: `us-east-1` (keep consistent with Lambda and SNS)
4. Block all public access: **enabled** (default)
5. Click **Create bucket**

---

## Step 2 — Create the SNS Topic

1. Go to **SNS → Topics → Create topic**
2. Type: **Standard**
3. Name: `ImageUploadNotification`
4. Click **Create topic**
5. Copy the **Topic ARN** — you will need it in the Lambda code

---

## Step 3 — Create an Email Subscription

1. Inside the topic, click **Create subscription**
2. Protocol: **Email**
3. Endpoint: your email address
4. Click **Create subscription**
5. Check your inbox and confirm the subscription link

---

## Step 4 — Create the Lambda Function

1. Go to **Lambda → Create function**
2. Name: `ImageUploadProcessor`
3. Runtime: **Python 3.12**
4. Architecture: `x86_64`
5. Execution role: Create a new role with basic Lambda permissions

### IAM permissions required

After creation, attach this inline policy to the Lambda execution role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sns:Publish",
      "Resource": "arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:ImageUploadNotification"
    }
  ]
}
```

---

## Step 5 — Upload the Lambda Code

Replace `YOUR_ACCOUNT_ID` in `lambda_function.py` with your real AWS account ID, then paste the code into the Lambda inline editor (or zip and upload).

The function code is in [`lambda_function.py`](./lambda_function.py).

**What the code does:**
- Reads the S3 event to get the bucket name, file key, and file size
- Builds a human-readable message
- Publishes it to the SNS topic
- Returns HTTP 200

---

## Step 6 — Add the S3 Trigger

1. Inside the Lambda function, click **Add trigger**
2. Source: **S3**
3. Bucket: `amc-eda-project-123`
4. Event types: **PUT** (ObjectCreated)
5. Suffix: `.jpg,.png,.jpeg` (optional — filter only images)
6. Click **Add**

> Lambda will automatically get `s3:GetObject` permission added to its resource-based policy.

---

## Step 7 — Test the System

1. Go to your S3 bucket
2. Upload any `.jpg` or `.png` image
3. Wait ~10 seconds and check your email

**Verify in Lambda logs:**

1. Go to **Lambda → Monitor → View CloudWatch logs**
2. Look for the latest log stream
3. You should see a line like:
   ```
   Published SNS message: <MessageId> | your-image.jpg
   ```

---

## Expected Outcome

```
Subject: Image Upload Notification
Body:
  New image uploaded!
    Bucket : amc-eda-project-123
    File   : your-image.jpg
    Size   : 204800 bytes
```

---

## Cleanup (avoid charges)

- Delete the S3 bucket contents and then the bucket
- Delete the Lambda function `ImageUploadProcessor`
- Delete the SNS topic `ImageUploadNotification`
- Delete the IAM role created for the Lambda

---

## What's Next

| Lab | Topic |
|-----|-------|
| [Lab 02](../02-sqs-decoupling/README.md) | Decoupling with SQS |
| [Lab 03](../03-eventbridge-rules/README.md) | Event routing with EventBridge |
