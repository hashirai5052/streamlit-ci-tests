from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb+srv://hashiraidevgen:hashir12@cluster12.dlqydre.mongodb.net/")

# Create or get the 'realtorsdata' database
db = client['realtorsdata']

# Define sample data for each collection
sample_documents = {
    "agents": {
        "full_name": "John Agent",
        "email": "johnagent@example.com",
        "phone": "555-1234",
        "company": "AgentCo"
    },
    "data2": {
        "full_name": "Jane Data",
        "email": "janedata@example.com",
        "listing_id": "LST12345",
        "price": 500000
    },
    "exprealty": {
        "full_name": "Mark Expo",
        "email": "markexpo@example.com",
        "office": "EXP Realty LA"
    },
    "homes": {
        "full_name": "Lucy Home",
        "email": "lucyhome@example.com",
        "address": "123 Main Street",
        "city": "Los Angeles"
    },
    "needsAttention": {
        "full_name": "Rick Attention",
        "issue": "Missing phone number",
        "priority": "High"
    },
    "posting": {
        "title": "New Home Listing",
        "description": "Beautiful 3-bedroom house available",
        "posted_by": "Lucy Home"
    },
    "realtor": {
        "full_name": "Sam Realtor",
        "email": "samrealtor@example.com",
        "brokerage": "Realtor Group"
    },
    "remax": {
        "full_name": "Ella Remax",
        "email": "ellaremax@example.com",
        "branch": "Remax Gold"
    },
    "sent": {
        "email": "client@example.com",
        "status": "sent",
        "date": "2024-04-07"
    },
    "updatedzillow": {
        "full_name": "Zara Zillow",
        "email": "zarazillow@example.com",
        "listing_status": "Sold"
    },
    "user": {
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin"
    },
    "zillow": {
        "listing_id": "ZIL98765",
        "address": "456 Park Avenue",
        "status": "Available"
    }
}

# Insert sample document into each collection
for collection_name, document in sample_documents.items():
    collection = db[collection_name]
    collection.insert_one(document)
    print(f"Inserted sample document into collection: {collection_name}")

print("✅ All collections created with sample data in 'realtorsdata' database!")
