# Cargomatic Project
This project is separted into 2 parts:

- The first part is a maritime shim tracking dashboard.

- The second part is the deployment of a hugging face model through AWS sagemaker for easy AI training.

## Maritime Ship Tracking Dashboard

A Python application for tracking maritime vessels using the Datalastic API, with AWS S3 storage and SNS notifications. This project monitors specific MAERSK ships and provides real-time location and status updates.

### Features

- **Real-time Ship Tracking**: Fetches current location and status data for maritime vessels
- **AWS S3 Integration**: Automatically stores ship data in S3 buckets with timestamps
- **SNS Notifications**: Sends formatted updates via AWS Simple Notification Service
- **AWS Lambda Support**: Deployable as a serverless function for automated monitoring
- **Error Handling**: Robust error handling for API failures and data processing issues

### Prerequisites

- Python 3.7+
- AWS Account with S3 and SNS access
- Datalastic API key
- Required Python packages (see requirements.txt)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cargomaticproject
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```env
OPENmaritime_API_KEY=your_datalastic_api_key_here
AWS_BUCKET_NAME=your_s3_bucket_name
SNS_TOPIC_ARN=your_sns_topic_arn
```

4. Configure AWS credentials:
```bash
aws configure
```


#### Local Execution

Run the main script to fetch and display ship data:

```bash
python src/maritime.py
```

This will:
- Fetch data for all configured ships
- Display ship type, location coordinates, and conditions
- Save data to S3 bucket
- Print success/failure messages

#### AWS Lambda Deployment

The `lambda_handler` function is designed for AWS Lambda deployment:

1. Package the application:
```bash
zip -r maritime-lambda.zip src/ requirements.txt
```

2. Deploy to AWS Lambda with the following configuration:
   - Runtime: Python 3.9+
   - Handler: `src.maritime.lambda_handler`
   - Environment variables: Set the same variables as in your `.env` file
   - IAM Role: Ensure the role has permissions for S3 and SNS

3. Set up CloudWatch Events or EventBridge to trigger the function on a schedule

### Project Structure

```
cargomaticproject/
├── src/
│   └── maritime.py          # Main application code
├── policies/
│   └── maritime_sns_policy.json  # SNS policy configuration
├── terra-infra/             # Terraform infrastructure code
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### API Integration

The application uses the Datalastic API to fetch vessel information:

- **Base URL**: `https://api.datalastic.com/api/v0/vessel_pro`
- **Authentication**: API key-based authentication
- **Data Format**: JSON response with vessel location, type, and status information

### AWS Services Used

#### Amazon S3
- Stores historical ship data with timestamps
- File naming convention: `maritime/{ship-name}-{timestamp}.json`
- Content type: `application/json`

#### Amazon SNS
- Sends formatted ship updates as notifications
- Subject: "Maritime Ship Updates"
- Message format includes ship name, type, location, and status


### Error Handling

The application includes comprehensive error handling for:
- API connection failures
- Invalid API responses
- AWS service errors (S3, SNS)
- Data processing exceptions
- Missing environment variables


#### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENmaritime_API_KEY` | Datalastic API key | Yes |
| `AWS_BUCKET_NAME` | S3 bucket name for data storage | Yes |
| `SNS_TOPIC_ARN` | SNS topic ARN for notifications | Yes |

#### Ship Configuration

To track different ships, modify the `ship_names` list in both the `main()` function and `lambda_handler()`:

```python
ship_names = ["YOUR_SHIP_NAME_1", "YOUR_SHIP_NAME_2"]
```

### Monitoring and Logging

The application provides detailed logging for:
- API request status
- Data processing results
- S3 upload success/failure
- SNS notification delivery
- Error conditions and stack traces




### Future Enhancements

- [ ] Add support for more shipping companies
- [ ] Implement data visualization dashboard
- [ ] Add historical data analysis
- [ ] Support for custom ship tracking criteria
- [ ] Integration with additional maritime APIs

## Deploying Hugging Face Model on AWS Sagemaker

This project demonstrates how to deploy a Hugging Face model to AWS SageMaker using the SageMaker Python SDK. It includes setup of the SageMaker session, IAM role handling, and deployment of a Hugging Face model for inference.

### Prerequisites
- An AWS account with permissions for:
    - Sagemaker
    - S3
    - IAM
- Python 3.9+
    ```
    pip install sagemaker boto3
    ```

### Steps to recreate

- Head over to AWS Sagemaker and create a domain and set it up for single user (use organization if it is for an org)
    
- Click on the default domain which was created and launch Canvas

- Launch jupyterlab and deploy the cells in the "huggingfaceproj/hfjupyter.ipynb" file