
from google.cloud import storage
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'friendly-chat-test-alfa2tr-firebase-adminsdk-tu82o-7dec33160d.json')

def list_buckets():
    """Lists all buckets."""

    storage_client = storage.Client(credentials=credentials)
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket.name)

if __name__ == "__main__":
    list_buckets()