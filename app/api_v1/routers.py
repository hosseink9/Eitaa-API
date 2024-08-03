import httpx
from fastapi import HTTPException, status, UploadFile, File, Form
from fastapi.routing import APIRouter

router = APIRouter(tags=["Eitaa"])


@router.post('/send-data', status_code=status.HTTP_200_OK)
async def create_post(file: UploadFile = File(...), token: str = Form(...), chat_id: str = Form(...), caption: str = Form(None)):
    url = f"https://eitaayar.ir/api/{token}/sendFile"
    send_data = {
        "chat_id": chat_id,
        "caption": caption
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=send_data, files={"file": file.file})
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

