from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.db.connection import user_collection
from bson import ObjectId

router = APIRouter()

# CREATE
@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    result = await user_collection.insert_one(user.model_dump())

    new_user = await user_collection.find_one({"_id": result.inserted_id})

    return {
        "id": str(new_user["_id"]),
        "name": new_user["name"],
        "age": new_user["age"]
    }

# GET ALL
@router.get("/users", response_model=list[UserResponse])
async def get_users():
    users = []
    async for user in user_collection.find():
        users.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "age": user["age"]
        })
    return users

# GET ONE
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    from bson import ObjectId

    user = await user_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "age": user["age"]
    }

# UPDATE
@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, updated_user: UserCreate):
    
    result = await user_collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": updated_user.model_dump()},
        return_document=True
    )

    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": str(result["_id"]),
        "name": result["name"],
        "age": result["age"]
    }

# DELETE
@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    from bson import ObjectId

    result = await user_collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted"}