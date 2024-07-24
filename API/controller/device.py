from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

from repository.device import (
    find_all_devices,
    find_one_device,
    create_device,
    remove_device,
    change_device_name,
)
from models.device import CreateDevice, ChangeDeviceName
from utils.hardwareService import checkHardwareStatusService, connectToHardwareService
from common.response import Response

router = APIRouter()


@router.get("", response_description="Get All Devices")
async def get_devices():
    devices = await find_all_devices()
    if devices[0]:
        return Response(devices[0], "success")
    return Response(devices, "empty")


@router.post("", response_description="Change Device Name")
async def change_name(name: ChangeDeviceName = Body(...)):
    deivce = await change_device_name(jsonable_encoder(name))
    return Response(deivce, "success")


# @router.get("/{id}", response_description="Get One Device")
# async def get_one_device(id: str):
#     device = await find_one_device(id)
#     if device:
#         return Response(device, "success")


# @router.get("/status/{id}", response_description="Get One Device Status")
# async def get_one_device_status(id: str):
#     device = await find_one_device(id)
#     status = await checkHardwareStatusService(device["device_ip"])
#     return Response(status, "success")


# @router.post("/conn", response_description="Connect to the device")
# async def connect_to_device(device: CreateDevice = Body(...)):
#     await remove_device()
#     device = jsonable_encoder(device)
#     new_device = await create_device(device)
#     status = await get_one_device_status(new_device["device_id"])
#     if status["status"] == "disconnected":
#         status = await connectToHardwareService(new_device["device_ip"])
#     return status
