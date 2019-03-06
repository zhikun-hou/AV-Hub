

import ProxyPool;


#ProxyPool.RefreshPool();

import asyncio
import aiohttp


async def test(url):
    res = await aiohttp.request("GET",url);
    print(res.text);



loop = asyncio.get_event_loop();

loop.run_until_complete(test("https://www.baidu.com"));
