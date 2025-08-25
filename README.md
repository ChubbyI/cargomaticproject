# Cargomatic project

This project is separted into 2 parts:
- The first part is a maritime dashboard app. 

- The second part is the deployment of a hugging face model through AWS sagemaker for easy AI training. 


    # Maritime Dashboard app

    # Prerequisites


    # Deploying Hugging Face Model on AWS Sagemaker

    This project demonstrates how to deploy a Hugging Face model to AWS SageMaker using the SageMaker Python SDK.
    It includes setup of the SageMaker session, IAM role handling, and deployment of a Hugging Face model for inference.

    # Prerequisites

    - An AWS account with permissions for:
        - SageMaker
        - S3
        - IAM
    - Python 3.9+
    - Installed packages:

    ```
    pip install sagemaker boto3
    ```

    # steps to recreate

    - Head over to AWS Sagemaker and crete a domain and set it up for single user (use organization if it is for an org)
    - click on the default domain which was created and launch Canvas
    - Lunch jupyterlab and deploy the "hfjupyter.ipynb" file


