import uvicorn
from fastapi import FastAPI

from app import database
from app.logging import LOGGING
from modules import routers
from modules.bot import setup_bot

app = FastAPI(title='Scrooge Bot')
for router in routers:
    app.include_router(router)


@app.on_event('startup')
async def startup():
    await database.connect()
    await setup_bot()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, log_config=LOGGING)
