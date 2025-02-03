I'll create a Python script that demonstrates real-time data loading into Google Cloud Firestore.



```python
from google.cloud import firestore
import datetime
import time
import random
import json
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FirestoreDataLoader:
    def __init__(self, project_id: str, collection_name: str):
        """
        Initialize Firestore client and settings
        
        Args:
            project_id: GCP project ID
            collection_name: Firestore collection to store data
        """
        self.db = firestore.Client(project=project_id)
        self.collection_name = collection_name
        logger.info(f"Initialized Firestore client for project: {project_id}")

    def generate_sample_data(self) -> Dict[str, Any]:
        """Generate sample data for demonstration"""
        return {
            "timestamp": datetime.datetime.now(),
            "temperature": round(random.uniform(20.0, 30.0), 2),
            "humidity": round(random.uniform(40.0, 80.0), 2),
            "pressure": round(random.uniform(980, 1020), 2),
            "device_id": f"device_{random.randint(1, 5)}"
        }

    def load_single_document(self, data: Dict[str, Any]) -> str:
        """
        Load a single document into Firestore
        
        Args:
            data: Dictionary containing document data
            
        Returns:
            Document ID of the created document
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document()
            doc_ref.set(data)
            logger.info(f"Successfully loaded document: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            logger.error(f"Error loading document: {str(e)}")
            raise

    def load_batch_documents(self, data_list: list[Dict[str, Any]], batch_size: int = 500):
        """
        Load multiple documents in batches using batch writes
        
        Args:
            data_list: List of dictionaries containing document data
            batch_size: Maximum number of operations in a batch
        """
        try:
            batch = self.db.batch()
            count = 0
            
            for data in data_list:
                doc_ref = self.db.collection(self.collection_name).document()
                batch.set(doc_ref, data)
                count += 1
                
                if count >= batch_size:
                    batch.commit()
                    logger.info(f"Committed batch of {count} documents")
                    batch = self.db.batch()
                    count = 0
            
            if count > 0:
                batch.commit()
                logger.info(f"Committed final batch of {count} documents")
                
        except Exception as e:
            logger.error(f"Error in batch loading: {str(e)}")
            raise

    def start_real_time_loading(self, interval: float = 1.0):
        """
        Start real-time data loading with specified interval
        
        Args:
            interval: Time between loads in seconds
        """
        logger.info(f"Starting real-time data loading with {interval}s interval")
        try:
            while True:
                data = self.generate_sample_data()
                self.load_single_document(data)
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Stopping real-time data loading")
        except Exception as e:
            logger.error(f"Error in real-time loading: {str(e)}")
            raise

def main():
    # Configuration
    PROJECT_ID = "your-project-id"  # Replace with your GCP project ID
    COLLECTION_NAME = "sensor_data"
    
    # Initialize loader
    loader = FirestoreDataLoader(PROJECT_ID, COLLECTION_NAME)
    
    # Example 1: Load single document
    data = loader.generate_sample_data()
    doc_id = loader.load_single_document(data)
    
    # Example 2: Load batch of documents
    batch_data = [loader.generate_sample_data() for _ in range(10)]
    loader.load_batch_documents(batch_data)
    
    # Example 3: Start real-time loading
    loader.start_real_time_loading(interval=2.0)

if __name__ == "__main__":
    main()

```

I've created a comprehensive Firestore data loader that includes:

1. A `FirestoreDataLoader` class with methods for:
   - Single document loading
   - Batch document loading
   - Real-time continuous loading
   - Sample data generation

2. Error handling and logging throughout the code

3. Support for both one-time and continuous data loading

To use this code, you'll need to:

1. Install the required package:
```bash
pip install google-cloud-firestore
```

2. Set up authentication:
   - Create a service account in your GCP project
   - Download the JSON key file
   - Set the environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
```

3. Replace `"your-project-id"` with your actual GCP project ID

You can customize the sample data generation method (`generate_sample_data`) to match your actual data structure.

Would you like me to explain any part of the code in more detail or add any additional functionality?