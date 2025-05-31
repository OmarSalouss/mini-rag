from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne # InsertOne: type of operation 

class ChunkModel(BaseDataModel):

    def __init__(self, db_client):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        # by_alias=True means use the alias name in the model, not the field name
        # exclude_unset=True means exclude the unset fields in the model
        chunk._id = result.inserted_id

        return chunk # return the Chunk object with the new _id
    
    async def get_chunk(self, chunk_id: str):
        result = await self.collection.find_one({
            "_id": ObjectId(chunk_id)
        })

        if result is None:
            return None
        
        return DataChunk(**result) # convert dict to Project object
    
    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]

            # I want to use bulk write to insert many chunks at once
            operations = [
                InsertOne(chunk.dict(by_alias=True, exclude_unset=True))
                for chunk in batch
            ]

            await self.collection.bulk_write(operations) # To save memory, I use bulk_write to insert many chunks at once
        
        return len(chunks)
    
    async def delete_chunk_by_project_id(self, project_id: ObjectId):
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })

        return result.deleted_count