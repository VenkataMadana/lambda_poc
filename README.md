# Simple AWS HTTP Lambda with Python

A simple AWS Lambda function that handles HTTP requests, deployed using GitHub Actions and testable locally with AWS SAM.

## Prerequisites

- Python 3.11+
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [Docker](https://www.docker.com/products/docker-desktop) (for local testing)
- AWS Account with appropriate permissions
- GitHub repository

## Project Structure

```
lambda_poc/
├── lambda_function.py       # Main Lambda handler
├── template.yaml            # AWS SAM template
├── requirements.txt         # Python dependencies
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions workflow
└── README.md
```

## Local Testing

### 1. Install AWS SAM CLI

```bash
# macOS
brew install aws-sam-cli

# Or follow: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Build the Application

```bash
sam build
```

### 4. Start Local API

```bash
sam local start-api
```

This starts a local API Gateway at `http://127.0.0.1:3000`

### 5. Test the Endpoints

**GET Request:**
```bash
curl http://127.0.0.1:3000/
```

**GET with Query Parameters:**
```bash
curl "http://127.0.0.1:3000/test?name=John&age=30"
```

**POST Request:**
```bash
curl -X POST http://127.0.0.1:3000/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Lambda", "data": "test"}'
```

### 6. Invoke Function Directly

```bash
# Create a test event
echo '{"httpMethod": "GET", "path": "/test", "queryStringParameters": {"name": "Test"}}' > event.json

# Invoke the function
sam local invoke HttpLambdaFunction -e event.json
```

## GitHub Actions Deployment

### 1. Set Up AWS Credentials in GitHub

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secrets:
- `AWS_ACCESS_KEY_ID`: Your AWS access key ID
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key

### 2. Configure Region

Edit [.github/workflows/deploy.yml](.github/workflows/deploy.yml) and change the `AWS_REGION` if needed:
```yaml
env:
  AWS_REGION: us-east-1  # Change to your preferred region
```

### 3. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: AWS Lambda HTTP function"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

The GitHub Action will automatically deploy your Lambda function on push to the `main` branch.

### 4. Manual Deployment Trigger

You can also trigger deployment manually from GitHub:
- Go to Actions tab
- Select "Deploy Lambda to AWS"
- Click "Run workflow"

## Manual AWS Deployment

If you prefer to deploy manually without GitHub Actions:

### 1. Configure AWS CLI

```bash
aws configure
```

### 2. Build and Deploy

```bash
sam build
sam deploy --guided
```

Follow the prompts:
- Stack Name: `simple-http-lambda-stack`
- AWS Region: Your preferred region
- Confirm changes before deploy: Y
- Allow SAM CLI IAM role creation: Y
- Save arguments to configuration file: Y

### 3. Get API URL

After deployment, the API URL will be shown in the outputs:
```bash
aws cloudformation describe-stacks \
  --stack-name simple-http-lambda-stack \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text
```

## Testing Deployed Lambda

Once deployed, test your Lambda function:

```bash
# Replace with your actual API URL
API_URL="https://your-api-id.execute-api.us-east-1.amazonaws.com/Prod"

# GET request
curl $API_URL

# POST request
curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from production"}'
```

## Lambda Function Features

The Lambda function:
- Handles GET and POST requests
- Processes query parameters
- Parses JSON request bodies
- Returns proper HTTP responses
- Includes CORS headers
- Logs events for debugging

## Cleanup

To remove all deployed resources:

```bash
aws cloudformation delete-stack --stack-name simple-http-lambda-stack
```

Or using SAM:

```bash
sam delete --stack-name simple-http-lambda-stack
```

## Troubleshooting

### Local Testing Issues

**Docker not running:**
```
Error: Running AWS SAM projects locally requires Docker
```
Start Docker Desktop and try again.

**Port already in use:**
```bash
sam local start-api --port 3001
```

### Deployment Issues

**Insufficient permissions:**
Ensure your AWS credentials have permissions for:
- Lambda
- API Gateway
- CloudFormation
- S3 (for deployment artifacts)
- IAM (for role creation)

**Check CloudFormation events:**
```bash
aws cloudformation describe-stack-events \
  --stack-name simple-http-lambda-stack \
  --max-items 10
```

## Customization

### Add More Routes

Edit [template.yaml](template.yaml) to add more HTTP methods or paths:

```yaml
PutRequest:
  Type: Api
  Properties:
    Path: /resource
    Method: PUT
```

### Add Environment Variables

```yaml
Environment:
  Variables:
    ENV_VAR_NAME: value
```

### Add Dependencies

Add packages to [requirements.txt](requirements.txt):
```
requests==2.31.0
boto3==1.34.0
```

## License

This project is provided as-is for educational purposes.
