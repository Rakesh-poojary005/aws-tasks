import os
import boto3
import uuid

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'your-s3-bucket-name'
    
    # Getting the uploaded image data from the event
    image_data = event['body']
    
    # Generating a unique file name for the image, e.g., using UUID
    file_name = str(uuid.uuid4())
    
    try:
        # Upload the image to S3
        s3.put_object(Bucket=bucket_name, Key=file_name, Body=image_data)
        return {
            'statusCode': 200,
            'body': f'Image {file_name} uploaded successfully.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error uploading image: {str(e)}'
        }
