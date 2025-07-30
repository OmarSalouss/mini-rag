from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    @classmethod 
    async def create_instance(cls, db_client: object):
        """
        # we create this static method because we **can't** use await and change the __init__ method to async
        # so we use a class method to create an instance of the class in addition to initializing the
        # collection and creating indexes if not exists
        """
        instance = cls(db_client=db_client) # cls is the class itself, and takes the db_client as an argument to the constructor __init__ so that it can be used to connect to the database
        await instance.init_collection() # initialize the collection and create indexes if not exists
        return instance

    # Create indexes for the collection at first time
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_project(self, project: Project):

        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        # by_alias=True means use the alias name in the model, not the field name
        # exclude_unset=True means exclude the unset fields in the model
        project._id = result.inserted_id

        return project # return the Project object with the new _id
    
    async def get_project_or_create_one(self, project_id: str):

        record = await self.collection.find_one({
            "project_id": project_id
        })

        if record is None:
            # create new project
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)

            return project
        
        return Project(**record) # convert dict to Project object
    
    async def get_all_projects(self, page: int = 1, page_size: int = 10):

        # count total number of documents
        total_documents = await self.collection.count_documents({})

        # calculate total pages
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1
        
        # collect data from the database
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        # cursor come from motor 
        async for document in cursor:
            projects.append(
                Project(**document)
            )
        
        return projects, total_pages

