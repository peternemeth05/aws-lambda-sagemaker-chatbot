import json
import boto3

# Init the SageMaker and S3 clients
sagemaker_client = boto3.client('sagemaker-runtime')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Get user input from the incoming Lambda event
        # Lambda event is the JSON object that contains data describing the trigger that started the function
        # This automatically passes to the handler function
    user_input = event.get('user_input', '')

    try:
        # Fetch data from S3 (optional, adjust key if you're using this for game data)
        s3_response = s3_client.get_object(
            Bucket='aicloudprojects3bucket',
            Key='console_pricing.json'
        )
        pricing_data = json.loads(s3_response['Body'].read().decode('utf-8'))

        # Check if the user is asking about console/game pricing
        if any(keyword in user_input.lower() for keyword in ['price', 'cost', 'console', 'game']):
            prompt = f"""
            User: {user_input}

            You are a video game expert with up-to-date knowledge of console and game pricing. Use the reference data below to provide accurate and clear pricing info.

            Reference data:
            {pricing_data}

            Please provide relevant pricing details and short recommendations if applicable.
            """
        else:
            prompt = f"""
            User: {user_input}

            You are a professional video game expert. Answer the user's question clearly and helpfully, using examples from gaming history, game mechanics, or recent industry trends where helpful.

            Keep it beginner-friendly and enthusiastic.
            """

        # Call the SageMaker endpoint to invoke the LLM with the prompt
        print("Prompt: {}".format(prompt))
        response = sagemaker_client.invoke_endpoint(
            EndpointName='jumpstart-dft-meta-textgeneration-llama-2-7b-f',
            ContentType='application/json',
            Body=json.dumps({
                "inputs": prompt,
                "parameters": {
                    "temperature": 0.2
                }
            }),
            #InferenceComponentName='jumpstart-dft-meta-textgeneration-llama-2-7b-f'
        )

        # Decode model response
        raw_response = response['Body'].read().decode('utf-8')
        print("Raw SageMaker response:", raw_response)
        response_body = json.loads(raw_response)

        if isinstance(response_body, list) and len(response_body) > 0: # checks to see if the the model wraps the response in a list
            response_body = response_body[0]

        generated_text = response_body.get('generated_text', 'No response generated.')

        return {
            "statusCode": 200,
            "body": json.dumps({"response": generated_text})
        }

    except Exception as e:
        print("Lambda error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }