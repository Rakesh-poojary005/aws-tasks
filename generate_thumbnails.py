import boto3
from PIL import Image
from io import BytesIO

bucket_name='test-bucket-00120'

s3 = boto3.client('s3')
thumbnail_size = (100, 100)  # Setting desired thumbnail size

def generate_thumbnail(event, context):
    # Get the file name from the SQS event
    file_name = event['Records'][0]['body']

    # Download the image from S3
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    image_data = response['Body'].read()

    # Generate the thumbnail
    image = Image.open(BytesIO(image_data))
    image.thumbnail(thumbnail_size)
    thumbnail_data = BytesIO()
    image.save(thumbnail_data, format='JPEG')

    # Upload the thumbnail to the S3 bucket
    thumbnail_key = 'thumbnails/' + file_name  # Store thumbnails in a separate folder
    s3.put_object(Bucket=bucket_name, Key=thumbnail_key, Body=thumbnail_data.getvalue())

    return {
        'statusCode': 200,
        'body': 'Thumbnail generated successfully.'
    }
