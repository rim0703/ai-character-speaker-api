from pydantic import BaseModel, Field
from typing import Optional


class Device(BaseModel):
    device_id: str = Field(...)
    device_name: str = Field(...)
    device_ip: str = Field(...)

    class Config:
        schema_extra = {
            "device_id": "1",
            "device_name": "짱구의 스피커",
            "device_ip": "127.0.0.1",
        }


class UpdateDevice(BaseModel):
    device_id: Optional[str]
    device_name: str = Field(...)
    device_ip: str = Field(...)

    class Config:
        schema_extra = {
            "device_id": "1",
            "device_name": "짱구의 스피커2",
            "device_ip": "127.255.255.1",
        }


class CreateDevice(BaseModel):
    device_name: str = Field(...)
    device_ip: str = Field(...)

    class Config:
        schema_extra = {
            "device_name": "짱구의 스피커3",
            "device_ip": "10.10.11.11",
        }


class ChangeDeviceName(BaseModel):
    device_name: str = Field(...)
