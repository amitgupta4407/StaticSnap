import os
import glob
from fastapi import FastAPI,  Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

STATIC_FOLDER = "static"

app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")

@app.get("/")
async def image_count():
    image_files = glob.glob(os.path.join(STATIC_FOLDER, '*.*'))
    return {'msg': f'Total number of images: {len(image_files)}'}

@app.get("/images")
async def get_images():
    image_files = glob.glob(os.path.join(STATIC_FOLDER, '*.*'))
    image_names = [os.path.basename(img) for img in image_files]
    return image_names

@app.get("/static/{filename}")
async def serve_static(filename: str):
    path = os.path.join(STATIC_FOLDER, filename)
    if os.path.exists(path):
        return FileResponse(path)
    else:
        return Response(status_code=404)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)