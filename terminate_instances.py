import os
import boto3
from dotenv import load_dotenv

def main():
    # Load environment variables
    env_path = os.path.join("env", "dev.aws.env")
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path, override=True)
        print("✓ Environment variables loaded from dev.aws.env")
    else:
        print("⚠️ dev.aws.env file not found. Using default environment.")

    endpoint_url = os.getenv("AWS_URL", "http://localhost:4566")
    region = os.getenv("REGION", "us-east-1")
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", "test")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", "test")

    print(f"Connecting to EC2 endpoint: {endpoint_url} (Region: {region})")
    
    ec2 = boto3.resource(
        'ec2',
        endpoint_url=endpoint_url,
        region_name=region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    try:
        instances = list(ec2.instances.all())
        print(f"Found {len(instances)} total instances in the system.")
        
        active_instances = [i for i in instances if i.state['Name'] != 'terminated']
        
        if not active_instances:
            print("No active/running instances to terminate.")
            return

        print(f"Terminating {len(active_instances)} active instance(s)...")
        for instance in active_instances:
            print(f"- Terminating {instance.id} (Current state: {instance.state['Name']})...")
            instance.terminate()
            instance.wait_until_terminated()
            print(f"  ✓ Successfully terminated {instance.id} (New state: {instance.state['Name']})")

    except Exception as e:
        print(f"❌ Error terminating EC2 instances: {e}")

if __name__ == "__main__":
    main()
