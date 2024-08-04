import httpx
from fastapi import HTTPException, status, UploadFile, File, Form
from fastapi.routing import APIRouter

router = APIRouter(tags=["Eitaa"])


@router.post('/send-data', status_code=status.HTTP_200_OK, description="You can use this function for create post in Eitta chanel or group")
async def create_post(files: list[UploadFile] = File(...), token: str = Form(...), chat_id: str = Form(...), caption: str = Form(None)):
    url = f"https://eitaayar.ir/api/{token}/sendFile"
    send_data = {
        "chat_id": chat_id,
        "caption": caption
    }
    for file in files:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=send_data, files={"file": file.file})
            response_list =[]
            if response.status_code == 200:
                response_list.append(response.json())
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
    return response_list

