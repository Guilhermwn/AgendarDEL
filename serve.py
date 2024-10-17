import uvicorn
from agendardel.main import app

if __name__ == '__main__':
    # uvicorn.run("agendardel.main:app",reload=True)
    uvicorn.run("agendardel.main:app", host="192.168.1.10", reload=True)
#     uvicorn.run("agendardel.main:app", host="10.25.1.115",reload=True)