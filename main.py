from fastapi import FastAPI, HTTPException
from fastapi import Request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from fastapi.middleware.cors import CORSMiddleware

uri = "mongodb+srv://zikriyachaudary112:zikriya112@cluster0.qh7hnez.mongodb.net/?appName=Cluster0"

app = FastAPI()

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.get_database("Developers")  
collection = db.get_collection("Developers") 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.put("/create")
async def create(request: Request):
    try:
        data = await request.json()
        resp = collection.insert_one(data)  
        return {"message": "Inserted Successfully", "id": str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert data: {str(e)}")

@app.get("/read")
async def read():
    try:
        data = collection.find()
        resp = []
        for document in data:
            document['_id'] = str(document['_id'])
            resp.append(document)
        return {"message": "Data retrieved successfully", "data": resp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve todos: {str(e)}")

@app.post("/update")
async def update(request: Request):
    try:
        data = await request.json()
        id = data.get("id")
        body = data.get("body")
        # return data
        collection.update_one({"_id": ObjectId(str(id))}, {"$set": body})
        return {"message": "Updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request data: {str(e)}")

@app.put("/delete")
async def delete(request: Request):
    try:
        data = await request.json()
        id = data.get("id")
        resp = collection.delete_one({"_id": ObjectId(id)})
        if resp.deleted_count == 1:
            return {"message": "Todo deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Todo not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete todo: {str(e)}")