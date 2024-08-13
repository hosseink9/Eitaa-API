import httpx
from fastapi import HTTPException, status, UploadFile, File, Form
from fastapi.routing import APIRouter
from typing import Optional, List

router = APIRouter(tags=["Eitaa"])

@router.post('/create-post', status_code=status.HTTP_200_OK, description="You can use this function for create post or add text in Eitaa channel or group")
async def eitaa_create_post(files: Optional[List[UploadFile]] = File(None),  token: str = Form(...), chat_id: str = Form(...), post_type: Optional[str] = Form(description="Please specify the type you want, (file or text)"), caption_or_text: Optional[str] = Form(None)):
    if post_type == "file":
        if files:
            url = f"https://eitaayar.ir/api/{token}/sendFile"
            response_list = []  # Initialize the response list outside of the loop
            for file in files:
                async with httpx.AsyncClient() as client:
                    send_data = {
                        "chat_id": chat_id,
                        "caption": caption_or_text
                    }
                    response = await client.post(url, data=send_data, files={"file": file.file})
                    if response.status_code == 200:
                        response_list.append(response.json())
                    else:
                        raise HTTPException(status_code=response.status_code, detail=response.text)
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Please add your files")
        return response_list
    elif post_type == "text":
        return await eitaa_create_text(token, chat_id, caption_or_text)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Please specify the type you want, (file or text)")


async def eitaa_create_text(token: str, chat_id: str, text: str) -> list: #Use this function for send text post to eitta
    if text:
        url = f"https://eitaayar.ir/api/{token}/sendMessage"
        send_data = {
            "chat_id": chat_id,
            "text": text
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=send_data)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Please add your text")
