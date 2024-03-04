
from utils import string_to_time, format_time_result
import openpyxl
import asyncio
import aiohttp
async def fetch(session, url):
    async with session.get(url) as response:
        items = (await response.json())['items']
        return [getRow(items[i]) for i in range (len(items))]
def getRow(item):
    person = item['person']
    result = item['finalResult']
    return [
        person['firstName'],    
        person['lastName'],    
        person['gender'],    
        person['age'],    
        string_to_time(result['gunTime']),
        string_to_time(result['finishTime']),
        format_time_result(result['chipTimeResult']),
        format_time_result(result['gunTimeResult']),
        format_time_result(result['finalResult']),
        result['averageSpeed'],
        result['disqualified']
    ]
async def getData(outfile):
    colums = ['firstname','lastname','gender','age','gun time','finish time','ship time result','gun time result','final result','average speed','discalified']
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(colums)
    offset = 0
    limit = 100
    max_person = 47800
    urls = []
    while(offset<max_person):
        urls.append(f"https://resultscui.active.com/api/results/events/HarmonieMutuelleSemideParis2024/participants?groupId=1022082&routeId=176712&offset={offset}&limit={limit}")
        offset += limit
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(session, url)) for url in urls]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            for row in response:
                sheet.append(row)
        workbook.save(f"{outfile}.xlsx")