from typing import List

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from io import BytesIO
from web3 import Web3
from starlette.exceptions import HTTPException
from pydantic import BaseModel, field_validator
from starlette.requests import Request
from starlette.templating import Jinja2Templates

"""
路由文件，路径：/web3
"""

# 注：填写以main.py文件作为起始，来填目录
templates = Jinja2Templates(directory='templates')

web3 = APIRouter()

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/2a1f54e725154a56bd24606f28b283f2?enable=archive'))


# 区块信息
class Block(BaseModel):
    hash: str
    number: int
    timestamp: int
    transactions: list[str]  # 交易哈希列表


# 范围
class Range(BaseModel):
    start: int
    end: int

    @field_validator('end')
    def enforce_range(cls, v, values):
        start_value = values.data['start']
        if start_value is not None and start_value >= v:
            raise ValueError(f'起始区块号({start_value})必须小于结束区块号({v})')
        elif v - start_value > 100:
            raise ValueError(f'限制区块号相差只能在100以内!')
        return v


# 根据区块号获取区块数据
@web3.get("/{number}", response_model=Block, summary='获取特定区块的数据（number示例：22106262）')
async def get_by_block_number(number: int):
    # 连接
    if not w3.is_connected():
        raise HTTPException(status_code=404, detail="节点连接失败，请重试!")

    # 获取区块
    try:
        block = w3.eth.get_block(number)
    except Exception as e:
        raise HTTPException(status_code=404, detail="未找到对应区块!")

    # 将区块数据转换为模型实例
    block_data = Block(
        hash=block.hash.hex(),
        number=block.number,
        timestamp=block.timestamp,
        transactions=[tx.hex() for tx in block.transactions]
    )

    # 返回
    return block_data


# 获取区块范围内的数据（限制范围不要过大，如范围设定为100）
@web3.post('/range', response_model=List[Block], summary='获取区块范围内的数据（只允许获取区块号相差100的范围!）')
async def get_blocks_by_range(block_range: Range):
    # 连接
    if not w3.is_connected():
        raise HTTPException(status_code=404, detail="节点连接失败，请重试!")

    # 后续返回的结果集
    block_list = []
    for number in range(block_range.start, block_range.end):
        try:
            block = w3.eth.get_block(number)
        except Exception as e:
            print(f'部分区块找不到!')
            continue
        finally:
            # 将区块数据转换为模型实例
            block_data = Block(
                hash=block.hash.hex(),
                number=block.number,
                timestamp=block.timestamp,
                transactions=[tx.hex() for tx in block.transactions]
            )
            block_list.append(block_data)

    return block_list


# 获取一版1年的Swap事件的Log数据
@web3.get("/logs/download", summary='获取一版1年的Swap事件的Log数据（可下载）')
async def get_swap_logs_in_one_year():
    # 这个路径是相对main（也就是你创建的app所在的目录下而言的）
    file_path = "files/swap.csv"
    # 读取文件
    with open(file_path, "rb") as file:
        file_content = file.read()
    file_like = BytesIO(file_content)
    file_like.seek(0)
    headers = {"Content-Disposition": "attachment; filename=swap.csv"}
    return StreamingResponse(file_like, media_type="application/octet-stream", headers=headers)


# 获取一版1年Log数据计算出来的Swap事件绘制而成的K线
@web3.get('/kline/html',
          summary='获取一版1年Log数据计算出来的Swap事件绘制而成的K线（注：需要通过接口直接访问！测试文档无法直接跳转！）')
async def get_kline(request: Request):
    return templates.TemplateResponse('UniSwap-V2_Kline_with_Volume.html', {'request': request})
