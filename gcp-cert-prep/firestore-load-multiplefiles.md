I'll create a solution that reads JSON files from Google Cloud Storage and loads them into Firestore.



```python
from google.cloud import storage
from google.cloud import firestore
import json
import logging
from typing import Dict, List, Any
import tempfile
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CloudStorageToFirestore:
    def __init__(self, project_id: str):
        """
        Initialize Cloud Storage and Firestore clients
        Args:
            project_id: Your Google Cloud project ID
        """
        try:
            self.storage_client = storage.Client(project=project_id)
            self.db = firestore.Client(project=project_id)
            logger.info(f"Successfully connected to project: {project_id}")
        except Exception as e:
            logger.error(f"Failed to initialize clients: {str(e)}")
            raise

    def read_json_from_gcs(self, bucket_name: str, blob_name: str) -> List[Dict]:
        """
        Read JSON data from Cloud Storage
        Args:
            bucket_name: Name of the GCS bucket
            blob_name: Path to the JSON file in the bucket
        Returns:
            List of dictionaries containing the JSON data
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)

            # Download to temporary file
            with tempfile.NamedTemporaryFile() as temp_file:
                blob.download_to_filename(temp_file.name)
                data = json.load(temp_file)

            logger.info(f"Successfully read data from gs://{bucket_name}/{blob_name}")
            return data if isinstance(data, list) else [data]

        except Exception as e:
            logger.error(f"Error reading from Cloud Storage: {str(e)}")
            raise

    def load_to_firestore(self, data: List[Dict], collection_name: str) -> None:
        """
        Load data into Firestore using batched writes
        Args:
            data: List of dictionaries to load
            collection_name: Target Firestore collection
        """
        try:
            # Create a batch
            batch = self.db.batch()
            count = 0
            total_count = 0
            batch_size = 500  # Firestore batch limit

            for record in data:
                # Add metadata
                record['uploaded_at'] = firestore.SERVER_TIMESTAMP
                record['source'] = 'cloud_storage'

                # Create document reference
                doc_ref = self.db.collection(collection_name).document()
                batch.set(doc_ref, record)
                count += 1
                total_count += 1

                # If batch limit reached, commit and start new batch
                if count >= batch_size:
                    batch.commit()
                    logger.info(f"Committed batch of {count} documents")
                    batch = self.db.batch()
                    count = 0

            # Commit any remaining documents
            if count > 0:
                batch.commit()
                logger.info(f"Committed final batch of {count} documents")

            logger.info(f"Successfully loaded {total_count} documents to collection: {collection_name}")

        except Exception as e:
            logger.error(f"Error loading to Firestore: {str(e)}")
            raise

    def process_bucket_directory(self, bucket_name: str, directory_prefix: str, collection_name: str) -> None:
        """
        Process all JSON files in a bucket directory
        Args:
            bucket_name: Name of the GCS bucket
            directory_prefix: Directory path in the bucket
            collection_name: Target Firestore collection
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=directory_prefix)
            
            files_processed = 0
            for blob in blobs:
                # Skip if not JSON file
                if not blob.name.endswith('.json'):
                    continue

                try:
                    logger.info(f"Processing file: gs://{bucket_name}/{blob.name}")
                    data = self.read_json_from_gcs(bucket_name, blob.name)
                    self.load_to_firestore(data, collection_name)
                    files_processed += 1
                except Exception as e:
                    logger.error(f"Error processing file {blob.name}: {str(e)}")
                    continue

            logger.info(f"Completed processing {files_processed} files")

        except Exception as e:
            logger.error(f"Error processing bucket directory: {str(e)}")
            raise

    def move_processed_file(self, bucket_name: str, source_blob_name: str, 
                          processed_directory: str = "processed") -> None:
        """
        Move processed file to a processed directory
        Args:
            bucket_name: Name of the GCS bucket
            source_blob_name: Original file path
            processed_directory: Target directory for processed files
        """
        try:
            bucket = self.storage_client.bucket(bucket_name)
            source_blob = bucket.blob(source_blob_name)
            
            # Generate new path
            filename = source_blob_name.split('/')[-1]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            new_name = f"{processed_directory}/{timestamp}_{filename}"
            
            # Copy to new location
            new_blob = bucket.copy_blob(source_blob, bucket, new_name)
            # Delete original
            source_blob.delete()
            
            logger.info(f"Moved {source_blob_name} to {new_name}")

        except Exception as e:
            logger.error(f"Error moving processed file: {str(e)}")
            raise

def main():
    # Example usage
    PROJECT_ID = "your-project-id"  # Replace with your project ID
    BUCKET_NAME = "your-bucket-name"
    
    loader = CloudStorageToFirestore(PROJECT_ID)

    # Example 1: Process single JSON file
    try:
        # Read and load single file
        data = loader.read_json_from_gcs(BUCKET_NAME, "data/customers.json")
        loader.load_to_firestore(data, "customers")
        loader.move_processed_file(BUCKET_NAME, "data/customers.json")
    except Exception as e:
        logger.error(f"Failed to process single file: {str(e)}")

    # Example 2: Process all JSON files in a directory
    try:
        loader.process_bucket_directory(BUCKET_NAME, "data/", "customers")
    except Exception as e:
        logger.error(f"Failed to process directory: {str(e)}")

if __name__ == "__main__":
    main()

```

To use this code:

1. Install required packages:
```bash
pip install google-cloud-storage google-cloud-firestore
```

2. Set up your authentication:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
```

3. Make sure your JSON files in Cloud Storage are properly formatted. Example format:
```json
[
    {
        "customer_id": "C1",
        "name": "John Doe",
        "email": "john@example.com",
        "orders": [
            {
                "order_id": "O1",
                "amount": 99.99
            }
        ]
    },
    {
        "customer_id": "C2",
        "name": "Jane Smith",
        "email": "jane@example.com",
        "orders": []
    }
]
```

4. The code provides several features:
   - Reads JSON files from Cloud Storage
   - Processes files in batches to handle large datasets
   - Adds metadata (upload timestamp, source)
   - Moves processed files to a "processed" directory
   - Includes comprehensive error handling and logging

5. Basic usage:
```python
# Initialize the loader
loader = CloudStorageToFirestore("your-project-id")

# Process a single file
data = loader.read_json_from_gcs("your-bucket", "path/to/file.json")
loader.load_to_firestore(data, "customers")

# Or process entire directory
loader.process_bucket_directory("your-bucket", "data/", "customers")
```

Would you like me to explain any specific part in more detail or add additional functionality?