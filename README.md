# ChatGPT Lambda Bedrock Service

## Overview
A serverless HTTP API that uses **AWS Lambda**, **API Gateway**, and **Amazon Bedrock** (Anthropic Claude 3.7 Sonnet) to generate AI-powered responses to user prompts. Clients send JSON with a `"prompt"` field; the Lambda function invokes your Bedrock inference profile, and returns the generated text.

---

## Architecture
- **Amazon API Gateway**  
  - Exposes a REST endpoint `POST /ask`  
  - Lambda proxy integration  
  - CORS enabled  
  - Deployed to the `dev` stage

- **AWS Lambda**  
  - Runtime: Python 3.13 (arm64)  
  - Handler: `src/lambda_function.py`  
  - Memory: 500 MB, Timeout: 2 min  
  - Execution role: `chatGPTLambdaRole` (Bedrock‑Invoke + CloudWatch Logs)

- **Amazon Bedrock**  
  - Anthropic Claude 3.7 Sonnet via **inference profile ARN**  
  - Region: `us-east-2`  

- **IAM Role**  
  - `chatGPTLambdaRole`  
  - Permissions:  
    - `bedrock:InvokeModel` on your inference profile  
    - `logs:CreateLogGroup` / `logs:CreateLogStream` / `logs:PutLogEvents`

![Architecture Diagram](docs/architecture.png)  
> _Paste your draw.io or hand‑drawn diagram into `docs/architecture.md` and render it as `architecture.png`._

---

## Technologies Used
- **AWS Lambda** (Python 3.13, arm64)  
- **Amazon API Gateway** (REST API, Lambda proxy, CORS)  
- **Amazon Bedrock** (Anthropic Claude 3.7 Sonnet)  
- **Boto3** (AWS SDK for Python)  
- **CloudWatch Logs**  
- **IAM** (least‑privilege execution role)

---

## Project Structure
```plaintext
chatgpt-lambda-bedrock/
├── .gitignore
├── README.md                 # This file
├── src/
│   ├── lambda_function.py    # Main Lambda handler—you will paste your working code here
│   ├── requirements.txt      # boto3
│   └── config/
│       └── settings.py       # Loads MODEL_ID & AWS_REGION from env vars
└── docs/
    └── architecture.md       # Text + embedded diagram image
