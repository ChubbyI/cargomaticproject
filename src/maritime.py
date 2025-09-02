import os
import json
import boto3
import urllib.request
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MaritimeDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENmaritime_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto3.client('s3')

    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists")
        except:
            print(f"Creating bucket {self.bucket_name}")
        try:
            # Simpler creation for us-east-1
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Successfully created bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def fetch_maritime(self, name):
        """Fetch ship data from datalastic API"""
        base_url = "https://api.datalastic.com/api/v0/vessel_pro?api-key={YOUR_API_KEY}&{PARAMETER}={PARAMETER_NUMBER}"
        params = {
            "YOUR_API_KEY": self.api_key,
            "PARAMETER": "uuid",
            "PARAMETER_NUMBER": "b8625b67-7142-cfd1-7b85-595cebfe4191"
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching maritime data: {e}")
            return None

    def save_to_s3(self, maritime_data, name):
        """Save maritime data to S3 bucket"""
        if not maritime_data:
            return False
            
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"maritime/{name}-{timestamp}.json"
        
        try:
            maritime_data['timestamp'] = timestamp
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(maritime_data),
                ContentType='application/json'
            )
            print(f"Successfully saved data for {name} to S3")
            return True
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return False

def main():
    dashboard = MaritimeDashboard()
    
    # Create bucket if needed
    dashboard.create_bucket_if_not_exists()
    
    names = ["MAERSK CHENNAI", "MAERSK HARVEY", "MAERSK NIKOLAI", "MAERSK ROCKY"] #CASE SENSITIVE
    
    for name in names:
        print(f"\nFetching maritime for {name}...")
        maritime_data = dashboard.fetch_maritime(name)
        if maritime_data:
            type = maritime_data['main']['type']
            lat = maritime_data['main']['lat']
            lon = maritime_data['main']['lon']
            description = maritime_data['maritime'][0]['description']
            
            print(f"type: {type}°F")
            print(f"lat: {lat}°")
            print(f"lon: {lon}°")
            print(f"Conditions: {description}")
            
            # Save to S3
            success = dashboard.save_to_s3(maritime_data, name)
            if success:
                print(f"maritime data for {name} saved to S3!")
        else:
            print(f"Failed to fetch maritime data for {name}")

if __name__ == "__main__":
    main()

def lambda_handler(event, context):
    """AWS Lambda handler for maritime data processing and SNS notification"""
    # Get environment variables
    api_key = os.getenv("OPENmaritime_API_KEY")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    
    sns_client = boto3.client("sns")
    s3_client = boto3.client("s3")
    
    # Initialize maritime dashboard
    dashboard = MaritimeDashboard()
    
    # Ship names to track
    ship_names = ["MAERSK CHENNAI", "MAERSK HARVEY", "MAERSK NIKOLAI", "MAERSK ROCKY"]
    
    messages = []
    
    for ship_name in ship_names:
        print(f"Fetching maritime data for {ship_name}...")
        
        # Fetch maritime data
        maritime_data = dashboard.fetch_maritime(ship_name)
        
        if maritime_data:
            # Extract key information
            try:
                ship_type = maritime_data.get('main', {}).get('type', 'Unknown')
                lat = maritime_data.get('main', {}).get('lat', 'N/A')
                lon = maritime_data.get('main', {}).get('lon', 'N/A')
                description = maritime_data.get('maritime', [{}])[0].get('description', 'No description available')
                
                # Format message for this ship
                ship_message = f"""
Ship: {ship_name}
Type: {ship_type}
Location: {lat}°N, {lon}°E
Status: {description}
"""
                messages.append(ship_message.strip())
                
                # Save to S3
                dashboard.save_to_s3(maritime_data, ship_name)
                
            except Exception as e:
                print(f"Error processing data for {ship_name}: {e}")
                messages.append(f"Error processing data for {ship_name}: {str(e)}")
        else:
            print(f"Failed to fetch data for {ship_name}")
            messages.append(f"Failed to fetch data for {ship_name}")
    
    # Combine all messages
    final_message = "\n---\n".join(messages) if messages else "No maritime data available."
    
    # Publish to SNS
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=final_message,
            Subject="Maritime Ship Updates"
        )
        print("Maritime data published to SNS successfully.")
    except Exception as e:
        print(f"Error publishing to SNS: {e}")
        return {"statusCode": 500, "body": "Error publishing to SNS"}
    
    return {"statusCode": 200, "body": "Maritime data processed and sent to SNS"}