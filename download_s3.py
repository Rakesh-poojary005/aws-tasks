import boto3

s3 = boto3.client('s3')
bucket_name='test-bucket-00120'

def download_image(event, context):
    # Get the file name from the request
    file_name = event['queryStringParameters']['fileName']

    # Download the image from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    image_data = response['Body'].read()

    return {
        'statusCode': 200,
        'body': image_data,
        'headers': {
            'Content-Type': 'image/jpeg'
        }
    }

def download_thumbnail(event, context):
    # Get the file name from the request
    file_name = 'thumbnails/' + event['queryStringParameters']['fileName']  
    # Download the thumbnail from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    thumbnail_data = response['Body'].read()

    return {
        'statusCode': 200,
        'body': thumbnail_data,
        'headers': {
            'Content-Type': 'image/jpeg'
        }
    }
