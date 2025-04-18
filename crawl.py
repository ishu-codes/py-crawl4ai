# tweet_fetcher.py (or whatever your filename is)
import asyncio
import re
import os
from crawl4ai import *
from utils import save_to_file, get_cookies_data, generate_filename_and_save_content
from twscrape import API, gather

crawler = None
twApi = None
_initialized = False  # <-- To make sure setup runs only once

async def setup():
    global crawler, twApi, _initialized
    if _initialized:
        return  # already initialized

    crawler = AsyncWebCrawler()
    twApi = API()

    username = os.getenv('USERNAME', '')
    if await twApi.pool.get_account(username) is None:
        await twApi.pool.add_account(
            username,
            os.getenv('PASSWORD', ''),
            os.getenv("EMAIL", ''),
            "mail_pass3",
            cookies=get_cookies_data('./cookies.txt')
        )

    _initialized = True

async def get_tweet(tweet_id=1912954389221851524):
    await setup()  # ensure setup is called
    result = await twApi.tweet_details(tweet_id)
    save_to_file('./result/tweet.txt', result)
    return result.rawContent

SOURCE_TYPES = (
    {"title": "tweet", "pattern": r'x\.com\/\w*\/status\/(\d+)', "func": get_tweet},
)

async def get_markdown(url: str, depth:int):
    await setup()  # ensure setup is called before anything

    for source in SOURCE_TYPES:
        match = re.search(source.get('pattern', ''), url)
        if match:
            tweet_id = int(match.group(1))
            return await source.get('func')(tweet_id)

    results = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=depth,
                include_external=False
            ),
            scraping_strategy=LXMLWebScrapingStrategy(),
            verbose=True
        )
    )


    # for i, result in enumerate(results, start=1):
        # generate_filename_and_save_content('./result', result, f'{url}-{i}')
    final_result = '\n\n\n-----\n\n\n'.join([result.markdown for result in results])
    generate_filename_and_save_content('./result', final_result, url)
    return final_result
