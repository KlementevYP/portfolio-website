from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory='../')
app.mount('/static', StaticFiles(directory='../assets'), name='static')

@app.get('/')
async def read_index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)