import asyncio
import aioredis

loop = asyncio.get_event_loop()

async def go():
    redis = await aioredis.create_redis_pool(
        'redis://127.0.0.1',minsize=5,maxsize=10,
        loop=loop
    )
    await redis.set('my-key','key')
    val = await redis.get('my-key')
    print(val)
    redis.close()
    await redis.wait_closed()
loop.run_until_complete(go())