# 🤖 Serverless AI Chatbot with AWS Lambda and SageMaker

### 👋 Intro
This project is a serverless, AI-powered chatbot built on Amazon Web Services. It uses a Large Language Model (LLM) hosted on Amazon SageMaker and gives it contextual knowledge by retrieving data from an Amazon S3 bucket. This approach, known as lightweight Retrieval-Augmented Generation (RAG), allows the model to answer questions about specific, private data without being retrained.

This repository documents the final code, configuration, and the development journey, including the many steps of debugging and refinement.

### 🛠️ Tech Stack
* **Compute:** AWS Lambda
* **Machine Learning:** Amazon SageMaker (for hosting the Llama 2 model)
* **Storage:** Amazon S3
* **Permissions:** AWS IAM (Identity and Access Management)
* **Language:** Python 3
* **AWS SDK:** Boto3

### ✨ Key Features
* **Serverless Architecture:** No servers to manage. The code runs on-demand with AWS Lambda.
* **Retrieval-Augmented Generation (RAG):** The chatbot can answer questions about custom data by dynamically injecting context from a JSON file stored in S3 into the model's prompt.
* **Dynamic Prompt Engineering:** The system intelligently decides whether to include the custom data based on keywords in the user's question.
* **Scalable AI:** Leverages the power of a pre-trained LLM on a scalable SageMaker endpoint.

### 🚀 The Process
Building this project was a practical lesson in cloud architecture and debugging. The initial goal was to connect a Lambda function to a SageMaker endpoint. However, the journey involved several key steps:
1.  **Initial Setup:** Wrote the core Python script to handle input, fetch data from S3, and call SageMaker.
2.  **IAM Permissions:** The biggest challenge was configuring the correct permissions. This involved creating an IAM Role and debugging `AccessDenied` errors by distinguishing between a **Trust Policy** (who can use the role) and a **Permissions Policy** (what the role can do).
3.  **SageMaker Endpoint Deployment:** The initial endpoint was not deployed. We had to navigate SageMaker JumpStart, subscribe to the Llama 2 model in the AWS Marketplace, and request a service quota increase for the required GPU instance.
4.  **Endpoint Naming:** Once deployed, the endpoint had a different name than expected. This required updating both the IAM policy and the Python code to match the new endpoint ARN and name.
5.  **Refining the Code:** The final step involved refining the Python code to remove an unnecessary `InferenceComponentName` parameter that was causing a `ValidationError`.

### 🎓 Lessons Learned
* **IAM is Foundational:** An incorrect IAM policy is one of the most common sources of errors in AWS. The error messages are key: `AccessDenied` means a permissions issue, while `not found` or `ValidationError` points to a configuration or code issue.
* **Check Every Name and ARN:** A small typo or region mismatch in an ARN (Amazon Resource Name) for S3, Lambda, or SageMaker will cause errors. Always copy and paste directly from the AWS console.
* **SageMaker Deployment is a Process:** Deploying a model from the marketplace isn't a single click. It can involve subscribing, requesting service quota increases, and waiting for the endpoint to become "InService".
* **Read the Error Logs Carefully:** Every error message we encountered contained the exact clue needed to solve the problem. `AccessDenied` pointed to IAM, `Endpoint not found` pointed to SageMaker deployment, and `Inference Component Name header is not allowed` pointed directly to a specific line in the code.

### 💡 Areas for Improvement
* **API Gateway:** Add an Amazon API Gateway in front of the Lambda function to expose it as a public REST API. This would allow web applications or other services to call it easily.
* **More Robust Data Store:** For more complex data, replace the single JSON file in S3 with a scalable database like Amazon DynamoDB.
* **Error Handling:** Improve the Python script's error handling to provide more user-friendly messages for different failure types.
* **Streaming Responses:** For longer answers, modify the function to stream the response back from the model, improving the user experience.

### ⚙️ Running the Project
To set up this project in your own AWS account, follow these steps:

1.  **S3 Bucket:** Create an S3 bucket and upload the `console_pricing.json` file to it.
2.  **SageMaker Endpoint:**
    * Navigate to **SageMaker JumpStart** and find the `meta-llama/Llama-2-7b-chat-hf` model.
    * Subscribe to the model in the AWS Marketplace.
    * Deploy the model to a SageMaker Endpoint. Note the name of the endpoint (e.g., `jumpstart-dft-meta-textgeneration-llama-2-7b-f`).
3.  **IAM Role:**
    * Create a new IAM Role for your Lambda function.
    * Set the **Trust Policy** to allow the Lambda service (`lambda.amazonaws.com`) to assume the role.
    * Attach the `AWSLambdaBasicExecutionRole` managed policy for CloudWatch logs.
    * Create a new **inline policy** using the JSON from `iam_policy.json`. **Remember to replace the placeholder ARNs with your actual S3 bucket and SageMaker endpoint ARNs.**
4.  **Lambda Function:**
    * Create a new Lambda function using a Python runtime.
    * Attach the IAM Role you created in the previous step.
    * Copy the code from `src/lambda_function.py` into the Lambda code editor.
    * **Crucially, update the `EndpointName` variable in the Python script to match your deployed SageMaker endpoint name.**
    * Deploy and test the function using a test event.

### 🎬 Demo
*(Here you can add a screenshot or an animated GIF of your function successfully running in the Lambda console)*

**Test Event:**
```json
{
  "user_input": "what is the price of the new console?"
}
```

**Example Successful Output:**
![image](https://user-images.githubusercontent.com/your-username/your-repo/assets/placeholder.png)
