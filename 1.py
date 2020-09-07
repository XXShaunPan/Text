import asyncio
import time
import aiohttp
from useragentxxc import PersonComputer
import arrow
import json
import pandas as pd

ua=lambda:PersonComputer.random()

header={
	'Host':'insight.baidu.com', 
	'Connection':'keep-alive', 
	'User-Agent':ua(), 
	'Accept':'*/*', 
	'Referer':'http://index.baidu.com/v2/rank/index.html?', 
	'Accept-Encoding':'gzip, deflate', 
	'Accept-Language':'zh-CN,zh;q=0.9'
}
num=1
df=pd.read_csv('cc.csv',index_col=[0])
df.loc['2020-08-26']=[0]*len(list(df.columns))
async def proc(doc):	
	origin=json.loads(doc[18:-14]+'}')['data']['results']
	data=origin['current']
	time=origin['currDate']
	for i in data:
		if i['item'] not in list(df.columns):
			df[i['item']]=[0]*238
		df[i['item']][time]=i['value']
	print(f'{time}--完成')



async def spider(url,session):
	async with session.get(url,headers=header) as resp:
		html = await resp.text()
		return html

async def tasks(url,session):
	doc=await spider(url,session)
	await proc(doc)

async def get_session():
	return aiohttp.ClientSession()

loop = asyncio.get_event_loop()
session = loop.run_until_complete(get_session())

async def main():
	a=time.time()
	print(a)
	await asyncio.wait([tasks(
		'http://insight.baidu.com/base/search/rank/list?pageSize=20&source=0&toFixed=1&filterType=1&dateType='+
		# 从2020-1-1开始，第i个日子  0为1-1号
		arrow.get('2020-08-26').shift(days=i).format("YYYYMMDD")+'~'+arrow.get('2020-08-26').shift(days=i).format("YYYYMMDD")
		+'&dimensionid=11&rateType=1000&filterNodes=&callback=_jsonpzgudlsg3hym',session) for i in range(num)])
	print(time.time()-a)
	# print(df)
	df.to_csv("cc.csv", encoding="utf-8", header=True, index=True)
loop.run_until_complete(main())
loop.run_until_complete(session.close())
loop.close()

