import uvicorn
from agendardel.main import app  # noqa: F401

if __name__ == '__main__':
    hosts = ["127.0.0.1", "192.168.1.10", "10.25.1.115"]
    reloads = [True, False]
    uvicorn.run(
        "agendardel.main:app", 
        host=hosts[0], 
        reload=reloads[1], 
        log_level="warning", 
        log_config=None
    )
