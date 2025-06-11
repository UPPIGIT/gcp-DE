I'll create a Cloud Function that runs on a schedule (Cloud Scheduler) to process JSON files from Cloud Storage to Firestore daily.



```python
# main.py
from google.cloud import storage
from google.cloud import firestore
import functions_framework
import json
import logging
from datetime import datetime
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GCSToFirestoreProcessor:
    def __init__(self):
        self.storage_client = storage.Client()
        self.db = firestore.Client()

    def process_json_file(self, bucket_name: str, blob_name: str, collection_name: str) -> None:
        """Process a single JSON file from GCS and load to Firestore"""
        try:
            # Get the file from GCS
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            json_data = json.loads(blob.download_as_string())
            
            # Ensure data is a list
            records = json_data if isinstance(json_data, list) else [json_data]
            
            # Process in batches
            batch = self.db.batch()
            count = 0
            batch_size = 500

            for record in records:
                # Add metadata
                record.update({
                    'processed_at': firestore.SERVER_TIMESTAMP,
                    'source_file': blob_name,
                    'batch_date': datetime.now().strftime('%Y-%m-%d')
                })

                # Add to batch
                doc_ref = self.db.collection(collection_name).document()
                batch.set(doc_ref, record)
                count += 1

                # Commit if batch size reached
                if count >= batch_size:
                    batch.commit()
                    logger.info(f"Committed batch of {count} records")
                    batch = self.db.batch()
                    count = 0

            # Commit remaining records
            if count > 0:
                batch.commit()
                logger.info(f"Committed final batch of {count} records")

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
        processed_count = 0
        error_count = 0

        for blob in blobs:
            if not blob.name.endswith('.json'):
                continue

            try:
                logger.info(f"Processing file: {blob.name}")
                processor.process_json_file(BUCKET_NAME, blob.name, COLLECTION_NAME)
                processed_count += 1
            except Exception as e:
                error_count += 1
                logger.error(f"Failed to process {blob.name}: {str(e)}")
                continue

        logger.info(f"Processing complete. Processed: {processed_count}, Errors: {error_count}")
        return f"Processing complete. Processed: {processed_count}, Errors: {error_count}"

    except Exception as e:
        logger.error(f"Function error: {str(e)}")
        raise


```

And here's the deployment configuration:

```yaml
# requirements.txt
google-cloud-storage==2.14.0
google-cloud-firestore==2.14.0
functions-framework==3.5.0

# deployment steps in terminal
gcloud functions deploy gcs_to_firestore \
    --runtime python310 \
    --trigger-topic daily-process \
    --entry-point process_files \
    --memory 512MB \
    --timeout 540s \
    --region your-region

```

Here's how to set up the entire solution:

1. **Set up Cloud Storage Structure**:
```
your-bucket/
├── input/           # Place new JSON files here
├── processed/       # Successfully processed files
│   └── YYYY/MM/DD/ # Organized by date
└── error/          # Files that failed processing
    └── YYYY/MM/DD/ # Organized by date
```

2. **Deploy Cloud Function**:
```bash
# Create a new directory for your function
mkdir gcs-to-firestore
cd gcs-to-firestore

# Create the necessary files
# - Copy main.py content from first artifact
# - Copy requirements.txt content from second artifact

# Deploy the function
gcloud functions deploy gcs_to_firestore \
    --runtime python310 \
    --trigger-topic daily-process \
    --entry-point process_files \
    --memory 512MB \
    --timeout 540s \
    --region your-region
```

3. **Set up Cloud Scheduler**:
```bash
# Create a scheduler job to run daily at 1 AM
gcloud scheduler jobs create pubsub daily-processor \
    --schedule "0 1 * * *" \
    --topic daily-process \
    --message-body "Process daily files" \
    --time-zone "UTC"
```

The solution provides:

1. **Automated Processing**:
   - Runs daily at scheduled time
   - Processes all JSON files in input directory
   - Moves files to appropriate directories after processing

2. **Error Handling**:
   - Failed files are moved to error directory
   - Comprehensive logging
   - Batch processing for large files

3. **Organization**:
   - Files are organized by date
   - Clear separation of new, processed, and error files

4. **Monitoring**:
   - Logs processing counts
   - Tracks success and failure rates
   - Cloud Function metrics available in Cloud Console

To monitor the process:

1. Check Cloud Function logs:
```bash
gcloud functions logs read gcs_to_firestore
```

2. View processed files:
```bash
gsutil ls gs://your-bucket/processed/YYYY/MM/DD/
```

3. Check for errors:
```bash
gsutil ls gs://your-bucket/error/YYYY/MM/DD/
```

Would you like me to explain any specific part in more detail or show you how to add additional features like:
- Email notifications for failures
- Slack notifications for process completion
- Custom retry logic for failed files
- Data validation before processing
- Custom file naming conventions


