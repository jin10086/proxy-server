import os, datetime, logging
from sanic import Sanic
from sanic import response
import asyncio
import uvloop
import aioredis
from sanic.config import Config

redis_host = "localhost"
redis_port = 6379

Config.REQUEST_TIMEOUT = 120


app = Sanic(__name__)

@app.listener('before_server_start')
async def setup_db(app, loop):
	app.redis_pool = await aioredis.create_redis_pool('redis://127.0.01',
                                                      loop=loop )

@app.listener('after_server_stop')
async def close_db(app, loop):
	app.redis_pool.close()
	await app.redis_pool.wait_closed()

@app.route('/')
async def test(request):
	return response.json({"data": 'hello'})

if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    app.run(host="0.0.0.0", port=5000, workers=4, debug=False)
