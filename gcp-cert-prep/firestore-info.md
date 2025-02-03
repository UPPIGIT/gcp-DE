I'll explain Firestore with practical examples of its key concepts and operations.



# What is Firestore?
Firestore is a NoSQL document database by Google Cloud. Think of it like a giant filing cabinet where:
- Documents are like individual papers (storing data)
- Collections are like folders (containing documents)
- Each document can contain subcollections (like having folders within folders)

Let's look at practical examples:

```python
from google.cloud import firestore

# Initialize Firestore
db = firestore.Client()
```

## 1. Basic Document Structure
Documents store data as key-value pairs:

```python
# Creating a user document
user_data = {
    'name': 'John Doe',
    'age': 30,
    'email': 'john@example.com',
    'interests': ['reading', 'hiking', 'coding'],
    'address': {
        'city': 'San Francisco',
        'country': 'USA'
    }
}

# Add document with auto-generated ID
db.collection('users').add(user_data)

# Or set document with specific ID
db.collection('users').document('user123').set(user_data)
```

## 2. Reading Data
There are multiple ways to read data:

```python
# Get a single document
user_ref = db.collection('users').document('user123')
user = user_ref.get()
if user.exists:
    print(user.to_dict())

# Query multiple documents
users_ref = db.collection('users')
# Users over 25 years old
query = users_ref.where('age', '>', 25).limit(10)
results = query.stream()
for doc in results:
    print(doc.id, doc.to_dict())
```

## 3. Real-world Data Structure Example
Let's model an e-commerce system:

```python
# Store order data
order_data = {
    'order_id': 'ORD001',
    'user_id': 'user123',
    'status': 'pending',
    'total_amount': 99.99,
    'items': [
        {
            'product_id': 'prod1',
            'name': 'Blue T-shirt',
            'quantity': 2,
            'price': 29.99
        },
        {
            'product_id': 'prod2',
            'name': 'Jeans',
            'quantity': 1,
            'price': 40.01
        }
    ],
    'shipping_address': {
        'street': '123 Main St',
        'city': 'Boston',
        'state': 'MA',
        'zip': '02101'
    },
    'created_at': firestore.SERVER_TIMESTAMP
}

# Add order
db.collection('orders').document('ORD001').set(order_data)
```

## 4. Real-time Updates
One of Firestore's powerful features is real-time listening:

```python
# Listen for changes in a document
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f"Current data: {doc.to_dict()}")

doc_ref = db.collection('users').document('user123')
doc_watch = doc_ref.on_snapshot(on_snapshot)

# Listen to query results
def on_collection_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            print(f"New order: {change.document.to_dict()}")
        elif change.type.name == 'MODIFIED':
            print(f"Modified order: {change.document.to_dict()}")
        elif change.type.name == 'REMOVED':
            print(f"Removed order: {change.document.id}")

query_watch = db.collection('orders').on_snapshot(on_collection_snapshot)
```

## 5. Transactions
For operations that need to be atomic:

```python
@firestore.transactional
def transfer_funds(transaction, from_ref, to_ref, amount):
    from_snapshot = from_ref.get(transaction=transaction)
    to_snapshot = to_ref.get(transaction=transaction)
    
    from_balance = from_snapshot.get('balance')
    to_balance = to_snapshot.get('balance')
    
    if from_balance < amount:
        raise ValueError('Insufficient funds')
    
    transaction.update(from_ref, {'balance': from_balance - amount})
    transaction.update(to_ref, {'balance': to_balance + amount})

# Use the transaction
transaction = db.transaction()
from_ref = db.collection('accounts').document('user1')
to_ref = db.collection('accounts').document('user2')
transfer_funds(transaction, from_ref, to_ref, 100)
```

## Best Practices:
1. Keep document size small (< 1MB)
2. Avoid deeply nested subcollections
3. Design your data structure for your most common queries
4. Use batch operations for multiple writes
5. Consider denormalization for faster queries

For example, batch writing:

```python
batch = db.batch()
for i in range(10):
    ref = db.collection('users').document(f'user{i}')
    batch.set(ref, {'name': f'User {i}'})
batch.commit()
```

Would you like me to elaborate on any of these concepts or show more specific examples for your use case?


I'll help you implement a specific example step by step. Let's create a practical application that manages user data and their orders in Firestore.



```python
from google.cloud import firestore
import datetime
import logging
from typing import Dict, List, Optional, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FirestoreManager:
    def __init__(self, project_id: str):
        """
        Initialize Firestore client
        Args:
            project_id: Your Google Cloud project ID
        """
        try:
            self.db = firestore.Client(project=project_id)
            logger.info(f"Successfully connected to Firestore in project: {project_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Firestore client: {str(e)}")
            raise

    def create_user(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """
        Create a new user in Firestore
        Args:
            user_id: Unique identifier for the user
            user_data: Dictionary containing user information
        Returns:
            bool: Success status
        """
        try:
            user_ref = self.db.collection('users').document(user_id)
            user_data['created_at'] = firestore.SERVER_TIMESTAMP
            user_ref.set(user_data)
            logger.info(f"Successfully created user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error creating user {user_id}: {str(e)}")
            return False

    def create_order(self, user_id: str, order_data: Dict[str, Any]) -> Optional[str]:
        """
        Create a new order for a user
        Args:
            user_id: User ID who placed the order
            order_data: Dictionary containing order information
        Returns:
            str: Order ID if successful, None otherwise
        """
        try:
            # Add order to orders collection
            order_ref = self.db.collection('orders').document()
            order_data.update({
                'user_id': user_id,
                'created_at': firestore.SERVER_TIMESTAMP,
                'status': 'pending'
            })
            order_ref.set(order_data)
            
            # Add order reference to user's orders subcollection
            user_order_ref = self.db.collection('users').document(user_id)\
                               .collection('orders').document(order_ref.id)
            user_order_ref.set({
                'order_id': order_ref.id,
                'created_at': firestore.SERVER_TIMESTAMP
            })
            
            logger.info(f"Successfully created order {order_ref.id} for user {user_id}")
            return order_ref.id
        except Exception as e:
            logger.error(f"Error creating order for user {user_id}: {str(e)}")
            return None

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user data from Firestore
        Args:
            user_id: User ID to retrieve
        Returns:
            Dict: User data if found, None otherwise
        """
        try:
            user_ref = self.db.collection('users').document(user_id)
            user = user_ref.get()
            if user.exists:
                return user.to_dict()
            logger.warning(f"User {user_id} not found")
            return None
        except Exception as e:
            logger.error(f"Error retrieving user {user_id}: {str(e)}")
            return None

    def get_user_orders(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all orders for a specific user
        Args:
            user_id: User ID to retrieve orders for
        Returns:
            List[Dict]: List of order data
        """
        try:
            orders = []
            order_refs = self.db.collection('users').document(user_id)\
                            .collection('orders').order_by('created_at', direction=firestore.Query.DESCENDING)\
                            .stream()
            
            for order_ref in order_refs:
                order_data = self.db.collection('orders').document(order_ref.id).get()
                if order_data.exists:
                    orders.append(order_data.to_dict())
            
            logger.info(f"Retrieved {len(orders)} orders for user {user_id}")
            return orders
        except Exception as e:
            logger.error(f"Error retrieving orders for user {user_id}: {str(e)}")
            return []

    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update user information
        Args:
            user_id: User ID to update
            update_data: Dictionary containing fields to update
        Returns:
            bool: Success status
        """
        try:
            user_ref = self.db.collection('users').document(user_id)
            update_data['updated_at'] = firestore.SERVER_TIMESTAMP
            user_ref.update(update_data)
            logger.info(f"Successfully updated user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {str(e)}")
            return False

    def update_order_status(self, order_id: str, new_status: str) -> bool:
        """
        Update order status
        Args:
            order_id: Order ID to update
            new_status: New status for the order
        Returns:
            bool: Success status
        """
        try:
            order_ref = self.db.collection('orders').document(order_id)
            order_ref.update({
                'status': new_status,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            logger.info(f"Successfully updated order {order_id} status to {new_status}")
            return True
        except Exception as e:
            logger.error(f"Error updating order {order_id}: {str(e)}")
            return False

def main():
    # Example usage
    PROJECT_ID = "your-project-id"  # Replace with your project ID
    manager = FirestoreManager(PROJECT_ID)
    
    # Create a user
    user_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'phone': '123-456-7890',
        'address': {
            'street': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip': '10001'
        }
    }
    manager.create_user('user123', user_data)
    
    # Create an order for the user
    order_data = {
        'items': [
            {
                'product_id': 'prod1',
                'name': 'Blue T-shirt',
                'quantity': 2,
                'price': 29.99
            }
        ],
        'total_amount': 59.98,
        'shipping_address': user_data['address']
    }
    order_id = manager.create_order('user123', order_data)
    
    # Retrieve user and their orders
    user = manager.get_user('user123')
    if user:
        print("User:", user)
        
    orders = manager.get_user_orders('user123')
    print("Orders:", orders)
    
    # Update order status
    if order_id:
        manager.update_order_status(order_id, 'shipped')

if __name__ == "__main__":
    main()

```

Let me walk you through how to use this code:

1. First, make sure you have everything set up:
```bash
# Install required package
pip install google-cloud-firestore

# Set your credentials
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
```

2. Replace `"your-project-id"` with your actual Google Cloud project ID.

3. The code provides a complete `FirestoreManager` class with methods for:
   - Creating users
   - Creating orders
   - Retrieving user data
   - Retrieving user orders
   - Updating user information
   - Updating order status

4. The data structure is organized as:
   - `users` collection
     - User documents
     - `orders` subcollection for each user
   - `orders` collection (main orders collection)

5. To try it out, you can run the example code in `main()` which demonstrates:
   - Creating a new user
   - Creating an order for that user
   - Retrieving user data
   - Retrieving user's orders
   - Updating order status

Would you like me to explain any specific part in more detail or show you how to implement additional functionality?


I'll show you how to read and load multiple data from files into Firestore. Let's create a solution that can handle different file formats (CSV, JSON, Excel) and load them into Firestore.



```python
import pandas as pd
import json
from google.cloud import firestore
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import csv
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FirestoreFileLoader:
    def __init__(self, project_id: str):
        """
        Initialize Firestore client
        Args:
            project_id: Your Google Cloud project ID
        """
        self.db = firestore.Client(project=project_id)
        logger.info(f"Connected to Firestore project: {project_id}")

    def read_csv(self, file_path: str) -> List[Dict]:
        """
        Read data from CSV file
        Args:
            file_path: Path to CSV file
        Returns:
            List of dictionaries containing the data
        """
        try:
            df = pd.read_csv(file_path)
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {str(e)}")
            raise

    def read_excel(self, file_path: str, sheet_name: Optional[str] = None) -> List[Dict]:
        """
        Read data from Excel file
        Args:
            file_path: Path to Excel file
            sheet_name: Name of the sheet to read (optional)
        Returns:
            List of dictionaries containing the data
        """
        try:
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error reading Excel file {file_path}: {str(e)}")
            raise

    def read_json(self, file_path: str) -> List[Dict]:
        """
        Read data from JSON file
        Args:
            file_path: Path to JSON file
        Returns:
            List of dictionaries containing the data
        """
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {str(e)}")
            raise

    def process_data(self, data: List[Dict], collection_name: str) -> None:
        """
        Process and upload data to Firestore
        Args:
            data: List of dictionaries containing the data
            collection_name: Name of the Firestore collection
        """
        try:
            # Create a batch
            batch = self.db.batch()
            count = 0
            batch_size = 500  # Firestore batch limit is 500

            for record in data:
                # Add timestamp to each record
                record['uploaded_at'] = firestore.SERVER_TIMESTAMP

                # Create a new document reference
                doc_ref = self.db.collection(collection_name).document()
                batch.set(doc_ref, record)
                count += 1

                # If batch size is reached, commit and create new batch
                if count >= batch_size:
                    batch.commit()
                    logger.info(f"Committed batch of {count} documents")
                    batch = self.db.batch()
                    count = 0

            # Commit any remaining documents
            if count > 0:
                batch.commit()
                logger.info(f"Committed final batch of {count} documents")

        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            raise

    def load_directory(self, directory_path: str, collection_name: str) -> None:
        """
        Load all supported files from a directory
        Args:
            directory_path: Path to directory containing data files
            collection_name: Name of the Firestore collection
        """
        try:
            directory = Path(directory_path)
            files_processed = 0

            for file_path in directory.iterdir():
                if not file_path.is_file():
                    continue

                file_extension = file_path.suffix.lower()
                try:
                    if file_extension == '.csv':
                        data = self.read_csv(str(file_path))
                    elif file_extension in ['.xlsx', '.xls']:
                        data = self.read_excel(str(file_path))
                    elif file_extension == '.json':
                        data = self.read_json(str(file_path))
                    else:
                        logger.warning(f"Unsupported file type: {file_path}")
                        continue

                    logger.info(f"Processing file: {file_path}")
                    self.process_data(data, collection_name)
                    files_processed += 1

                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {str(e)}")
                    continue

            logger.info(f"Completed processing {files_processed} files")

        except Exception as e:
            logger.error(f"Error processing directory {directory_path}: {str(e)}")
            raise

def main():
    # Example usage
    PROJECT_ID = "your-project-id"  # Replace with your project ID
    loader = FirestoreFileLoader(PROJECT_ID)

    # Example 1: Load a single CSV file
    csv_file = "path/to/your/data.csv"
    try:
        data = loader.read_csv(csv_file)
        loader.process_data(data, "customers")
    except Exception as e:
        logger.error(f"Failed to process CSV file: {str(e)}")

    # Example 2: Load a single Excel file
    excel_file = "path/to/your/data.xlsx"
    try:
        data = loader.read_excel(excel_file, sheet_name="Sheet1")
        loader.process_data(data, "products")
    except Exception as e:
        logger.error(f"Failed to process Excel file: {str(e)}")

    # Example 3: Load all files from a directory
    directory_path = "path/to/your/data/directory"
    try:
        loader.load_directory(directory_path, "inventory")
    except Exception as e:
        logger.error(f"Failed to process directory: {str(e)}")

if __name__ == "__main__":
    main()

```

To use this code, follow these steps:

1. Install required packages:
```bash
pip install google-cloud-firestore pandas openpyxl
```

2. Prepare your data files:
- CSV files should have headers
- Excel files should have headers in the first row
- JSON files should contain an array of objects

3. Example data file formats:

CSV file (customers.csv):
```csv
id,name,email,phone
1,John Doe,john@example.com,123-456-7890
2,Jane Smith,jane@example.com,098-765-4321
```

JSON file (products.json):
```json
[
  {
    "product_id": "P1",
    "name": "Product 1",
    "price": 29.99,
    "stock": 100
  },
  {
    "product_id": "P2",
    "name": "Product 2",
    "price": 49.99,
    "stock": 50
  }
]
```

4. Use the loader:

```python
# Initialize the loader
loader = FirestoreFileLoader("your-project-id")

# Load single file
data = loader.read_csv("customers.csv")
loader.process_data(data, "customers")

# Or load entire directory
loader.load_directory("data_directory", "products")
```

The code provides:
1. Support for CSV, Excel, and JSON files
2. Batch processing to handle large datasets
3. Directory scanning for bulk loading
4. Error handling and logging
5. Automatic timestamp addition

Would you like me to explain any part in more detail or show you how to handle specific file formats or data structures?