import boto3

sqs = boto3.client('sqs')
queue_name = 'test_sqs'

# Create the SQS Queue
queue_response = sqs.create_queue(QueueName=queue_name)
queue_url = queue_response['QueueUrl']

print("SQS Queue created successfully!")
print("Queue URL:", queue_url)
