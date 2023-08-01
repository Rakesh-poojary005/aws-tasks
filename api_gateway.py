import boto3

api_gateway = boto3.client('apigateway')
lambda_client = boto3.client('lambda')

def create_api():
    # Create the API Gateway
    api_name = 'ImageAPI'
    api_response = api_gateway.create_rest_api(name=api_name, description='API for image upload and retrieval')

    # Extract the API ID from the response
    api_id = api_response['id']

    # Define the resource and method names for each endpoint
    resource_name_upload = 'upload'
    resource_name_download_image = 'download/image'
    resource_name_download_thumbnail = 'download/thumbnail'
    method_name_upload = 'POST'
    method_name_download = 'GET'

    # Create the REST API resources
    resource_response_upload = api_gateway.create_resource(restApiId=api_id, parentId=api_id, pathPart=resource_name_upload)
    resource_response_download_image = api_gateway.create_resource(restApiId=api_id, parentId=api_id, pathPart=resource_name_download_image)
    resource_response_download_thumbnail = api_gateway.create_resource(restApiId=api_id, parentId=api_id, pathPart=resource_name_download_thumbnail)

    # Extract the resource IDs from the response
    resource_id_upload = resource_response_upload['id']
    resource_id_download_image = resource_response_download_image['id']
    resource_id_download_thumbnail = resource_response_download_thumbnail['id']

    # Create the methods for each resource
    method_response_upload = api_gateway.put_method(
        restApiId=api_id,
        resourceId=resource_id_upload,
        httpMethod=method_name_upload,
        authorizationType='NONE' 
    )
    method_response_download_image = api_gateway.put_method(
        restApiId=api_id,
        resourceId=resource_id_download_image,
        httpMethod=method_name_download,
        authorizationType='NONE' 
    )
    method_response_download_thumbnail = api_gateway.put_method(
        restApiId=api_id,
        resourceId=resource_id_download_thumbnail,
        httpMethod=method_name_download,
        authorizationType='NONE'
    )

    # Set up the integration between the methods and the Lambda functions
    lambda_function_name = 'GenerateThumbnailLambdaFunction' 
    integration_response_upload = api_gateway.put_integration(
        restApiId=api_id,
        resourceId=resource_id_upload,
        httpMethod=method_name_upload,
        type='AWS_PROXY', 
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:{boto3.session.Session().region_name}:lambda:path/2015-03-31/functions/arn:aws:lambda:{boto3.session.Session().region_name}:{774565248809}:function:{lambda_function_name}/invocations'
    )

    lambda_function_name_download_image = 'DownloadImageLambdaFunction'  
    integration_response_download_image = api_gateway.put_integration(
        restApiId=api_id,
        resourceId=resource_id_download_image,
        httpMethod=method_name_download,
        type='AWS_PROXY',  # This indicates that the integration is with a Lambda function
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:{boto3.session.Session().region_name}:lambda:path/2015-03-31/functions/arn:aws:lambda:{boto3.session.Session().region_name}:{774565248809}:function:{lambda_function_name_download_image}/invocations'
    )

    lambda_function_name_download_thumbnail = 'DownloadThumbnailLambdaFunction'  
    integration_response_download_thumbnail = api_gateway.put_integration(
        restApiId=api_id,
        resourceId=resource_id_download_thumbnail,
        httpMethod=method_name_download,
        type='AWS_PROXY',  
        integrationHttpMethod='POST',
        uri=f'arn:aws:apigateway:{boto3.session.Session().region_name}:lambda:path/2015-03-31/functions/arn:aws:lambda:{boto3.session.Session().region_name}:{774565248809}:function:{lambda_function_name_download_thumbnail}/invocations'
    )

    # Deploy the API
    deployment_response = api_gateway.create_deployment(restApiId=api_id, stageName='prod')

    # Extract the deployment ID from the response
    deployment_id = deployment_response['id']

    # Get the endpoint URLs for the deployed API
    endpoint_url_upload = f'https://{api_id}.execute-api.{boto3.session.Session().region_name}.amazonaws.com/prod/{resource_name_upload}'
    endpoint_url_download_image = f'https://{api_id}.execute-api.{boto3.session.Session().region_name}.amazonaws.com/prod/{resource_name_download_image}'
    endpoint_url_download_thumbnail = f'https://{api_id}.execute-api.{boto3.session.Session().region_name}.amazonaws.com/prod/{resource_name_download_thumbnail}'

    # Return the API details
    return {
        'api_id': api_id,
        'endpoint_url_upload': endpoint_url_upload,
        'endpoint_url_download_image': endpoint_url_download_image,
        'endpoint_url_download_thumbnail': endpoint_url_download_thumbnail
    }


YOUR_ACCOUNT_ID = 774565248809
bucket_name='test-bucket-00120'

# Create the API
api_details = create_api()

print("API Gateway configured successfully!")
print("Upload Endpoint URL:", api_details['endpoint_url_upload'])
print("Download Image Endpoint URL:", api_details['endpoint_url_download_image'])
print("Download Thumbnail Endpoint URL:", api_details['endpoint_url_download_thumbnail'])
