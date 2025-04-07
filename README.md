# UniSwap-V2-Astra15
UniSwap-V2-Astra15交易对——链上分析学习小demo（fastapi+pydantic+pyecharts+pandas）

该项目文件在master分支下，请自行切换到master分支下查看

## 文件目录
### main文件
为fastapi项目的启动文件

### apps目录
存放web3.py文件，对应路由“/web3”下的接口

### files目录
存放swap事件日志数据（swap.csv）以及k线数据（kline.csv）

### templates目录
存放k线图的html文件，可直接运行查看，也可通过fastapi接口访问查看

### tools目录
存放的是一些过程文件，分别用于：
1.获取swap事件日志
2.为swap日志增加时间戳
3.将swap日志数据转化为k线数据
4.将k线数据绘制成k线图并转化为html文件


