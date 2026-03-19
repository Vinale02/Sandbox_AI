import asyncio
import base64

def encode_image(image_path: str) -> str:
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


async def async_encode_image(image_path: str):
    loop = asyncio._get_running_loop()
    encoded_data = await loop.run_in_executor(None, encode_image, image_path)
    return encoded_data