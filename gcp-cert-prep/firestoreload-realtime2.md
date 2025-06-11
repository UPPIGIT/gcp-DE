I'll modify the code to process all files without batch size limitations. Here's the updated Cloud Function:



```python
# main.py
from google.cloud import storage
from google.cloud import firestore
import functions_framework
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GCSToFirestoreProcessor:
    def __init__(self):
        self.storage_client = storage.Client()
        self.db = firestore.Client()

    def process_json_file(self, bucket_name: str, blob_name: str, collection_name: str) -> None:
        """Process a JSON file from GCS and load to Firestore"""
        try:
            # Get the file from GCS
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            json_data = json.loads(blob.download_as_string())
            
            # Ensure data is a list
            records = json_data if isinstance(json_data, list) else [json_data]
            
            # Create a transaction for atomic writes
            transaction = self.db.transaction()
            
            @firestore.transactional
            def commit_in_transaction(transaction, records):
                for record in records:
                    # Add metadata
                    record.update({
                        'processed_at': firestore.SERVER_TIMESTAMP,
                        'source_file': blob_name,
                        'batch_date': datetime.now().strftime('%Y-%m-%d')
                    })
                    
                    # Add to Firestore
                    doc_ref = self.db.collection(collection_name).document()
                    transaction.set(doc_ref, record)
                
                logger.info(f"Processed {len(records)} records from {blob_name}")
            
            # Execute transaction
            commit_in_transaction(transaction, records)
            
            # Move processed file
            self._move_to_processed(bucket, blob)

        except Exception as e:
            logger.error(f"Error processing file {blob_name}: {str(e)}")
            self._move_to_error(bucket, blob)
            raise

    def _move_to_processed(self, bucket, blob):
        """Move processed file to 'processed' folder"""
        new_name = f"processed/{datetime.now().strftime('%Y/%m/%d')}/{blob.name.split('/')[-1]}"
        bucket.copy_blob(blob, bucket, new_name)
        blob.delete()
        logger.info(f"Moved {blob.name} to {new_name}")

    def _move_to_error(self, bucket, blob):
        """Move failed file to 'error' folder"""
        new_name = f"error/{datetime.now().strftime('%Y/%m/%d')}/{blob.name.split('/')[-1]}"
        bucket.copy_blob(blob, bucket, new_name)
        blob.delete()
        logger.info(f"Moved {blob.name} to {new_name}")

@functions_framework.cloud_event
def process_files(cloud_event):
    """Cloud Function triggered by Cloud Scheduler"""
    try:
        # Configuration
        BUCKET_NAME = "your-bucket-name"  # Replace with your bucket
        INPUT_DIRECTORY = "input/"
        COLLECTION_NAME = "your_collection"  # Replace with your collection

        processor = GCSToFirestoreProcessor()
        bucket = processor.storage_client.bucket(BUCKET_NAME)

        # List all JSON files in input directory
        blobs = bucket.list_blobs(prefix=INPUT_DIRECTORY)
        processed_files = []
        error_files = []

        for blob in blobs:
            if not blob.name.endswith('.json'):
                continue

            try:
                logger.info(f"Processing file: {blob.name}")
                processor.process_json_file(BUCKET_NAME, blob.name, COLLECTION_NAME)
                processed_files.append(blob.name)
            except Exception as e:
                error_files.append(blob.name)
                logger.error(f"Failed to process {blob.name}: {str(e)}")
                continue

        # Log summary
        summary = {
            'processed_files': len(processed_files),
            'error_files': len(error_files),
            'processed_list': processed_files,
            'error_list': error_files,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store summary in Firestore
        summary_ref = processor.db.collection('processing_summary').document()
        summary_ref.set(summary)
        
        logger.info(f"Processing complete. Processed: {len(processed_files)}, Errors: {len(error_files)}")
        return f"Processing complete. Processed: {len(processed_files)}, Errors: {len(error_files)}"

    except Exception as e:
        logger.error(f"Function error: {str(e)}")
        raise

```

Key changes made:
1. Removed batch size limitations
2. Using transactions for atomic writes
3. Processing entire files at once
4. Added detailed processing summary storage in Firestore

To deploy the function:

```bash
# requirements.txt
google-cloud-storage==2.14.0
google-cloud-firestore==2.14.0
functions-framework==3.5.0

# Deploy command
gcloud functions deploy gcs_to_firestore \
    --runtime python310 \
    --trigger-topic daily-process \
    --entry-point process_files \
    --memory 2048MB \  # Increased memory
    --timeout 540s \
    --region your-region
```

Set up Cloud Scheduler:
```bash
gcloud scheduler jobs create pubsub daily-processor \
    --schedule "0 1 * * *" \
    --topic daily-process \
    --message-body "Process daily files" \
    --time-zone "UTC"
```

Storage structure:
```
your-bucket/
├── input/           # New JSON files
├── processed/       # Successfully processed files
│   └── YYYY/MM/DD/ 
└── error/          # Failed files
    └── YYYY/MM/DD/
```

You can monitor the process:
1. Check Firestore's `processing_summary` collection for run details
2. View Cloud Function logs:
```bash
gcloud functions logs read gcs_to_firestore
```

The function now:
- Processes all records in each file together
- Uses transactions for data consistency
- Stores detailed processing summaries
- Organizes files by date
- Provides comprehensive logging

Would you like me to add any additional features or explain any part in more detail?