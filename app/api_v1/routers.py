import httpx
import base64
from typing import Annotated
from fastapi import HTTPException, status, UploadFile, File, Form
from fastapi.routing import APIRouter

router = APIRouter(tags=["Eitaa"])


@router.post('/send-data', status_code=status.HTTP_200_OK)
async def create_post(file: Annotated[bytes, File()], token: Annotated[str, Form()], chat_id: Annotated[str, Form()], description: Annotated[str|None, Form()]):
    file_data_base64 = base64.b64encode(file).decode('utf-8')
    url = f"https://eitaayar.ir/api/{token}/sendFile"
    send_data = {
        "chat_id": chat_id,
        "file": file_data_base64,
        "caption": description
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=send_data)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

