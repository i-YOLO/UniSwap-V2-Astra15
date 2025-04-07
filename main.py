import uvicorn
from fastapi import FastAPI
from apps.web3 import web3

"""
主文件
"""

app = FastAPI()

app.include_router(web3, prefix="/web3", tags=['UniSwap测试接口'])

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
