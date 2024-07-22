from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from repository.device import find_all_devices, find_one_device, create_device
from models.device import Device, UpdateDevice, Response, ErrorResponse, CreateDevice
from utils.hardwareService import checkHardwareStatusService

router = APIRouter()


@router.get("/", response_description="Get All Devices")
async def get_devices():
    devices = await find_all_devices()
    if devices:
        return Response(devices, "success")
    return Response(devices, "empty")


@router.get("/{id}", response_description="Get One Device")
async def get_one_device(id: str):
    device = await find_one_device(id)
    if device:
        return Response(device, "sccess")


@router.get("/status/{id}", response_description="Get One Device Status")
async def get_one_device_status(id: str):
    device = await find_one_device(id)
    status = await checkHardwareStatusService(device["device_ip"])
    return Response(status, "success")


@router.post("/conn", response_description="Connect to the device")
async def connect_to_device(device: CreateDevice = Body(...)):
    device = jsonable_encoder(device)
    new_device = await create_device(device)
    status = await get_one_device_status(new_device["device_id"])
    return status
