import motor.motor_asyncio


class MongoDB:
    def __init__(self, connection: str, database: str):
        self.connection = connection
        self.database = database
        self.client = None
        self.db = None

    async def __aenter__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.connection)
        self.db = self.client[self.database]
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def get_collection(self, collection_name):
        return self.db[collection_name]

    async def insert_document(self, collection_name, document):
        collection = self.get_collection(collection_name)
        result = await collection.insert_one(document)
        return result.inserted_id

    async def find_documents(self, collection_name, query=None):
        collection = self.get_collection(collection_name)
        if query is None:
            query = {}
        cursor = collection.find(query)
        return await cursor.to_list(None)

    async def update_document(self, collection_name, query, update):
        collection = self.get_collection(collection_name)
        result = await collection.update_one(query, {'$set': update})
        return result.modified_count

    async def delete_document(self, collection_name, query):
        collection = self.get_collection(collection_name)
        result = await collection.delete_one(query)
        return result.deleted_count
