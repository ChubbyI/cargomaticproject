provider "aws" {
  region = "us-east-1"
}

# EC2 instance
resource "aws_instance" "my_instance" {
  ami           = "ami-08c40ec9ead489470" # Amazon Linux 2 AMI in us-east-1
  instance_type = "ml.g5.12xlarge" #VERY EXPENSIVE SO MAKE SURE TO DESTROY WHEN NOT IN USE

  tags = {
    Name = "HFInstance"
  }
}

#  S3 bucket
resource "aws_s3_bucket" "my_bucket" {
  bucket = "ChubiHF-bucket" 
  acl    = "private"

  tags = {
    Name = "HFBucket"
  }
}
