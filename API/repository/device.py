from common.client import connectDB
from bson.objectid import ObjectId


def device_helper(device) -> dict:
    return {
        "device_id": str(device["_id"]),
        "device_name": str(device["device_name"]),
        "device_ip": str(device["device_ip"]),
    }


def device_repository():
    db = connectDB()
    device = db.get_collection("device")
    return device


async def find_all_devices():
    device = device_repository()
    devices_list = []
    async for d in device.find():
        devices_list.append(device_helper(d))
    return devices_list


async def find_one_device(id):
    device = device_repository()
    device_one = await device.find_one({"_id": ObjectId(id)})
    return device_helper(device_one)


async def change_device_name(request):
    device = device_repository()
    devices_list = []
    async for d in device.find():
        devices_list.append(d)
    devices_list[0]["device_name"] = request["device_name"]
    device.update_one({"_id": devices_list[0]["_id"]}, {"$set": devices_list[0]})
    return device_helper(devices_list[0])


async def create_device(new_device):
    device = device_repository()
    new_device = await device.insert_one(new_device)
    new_device = await device.find_one({"_id": new_device.inserted_id})
    return device_helper(new_device)


async def remove_device():
    device = device_repository()
    status = await device.delete_many({})
    return status
