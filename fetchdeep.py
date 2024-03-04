from utils import string_to_time, format_time_result
import openpyxl
import asyncio
import aiohttp
import requests
def getRow(item,splits,colums):
    person = item['person']
    result = item['finalResult']
    row =  [None for i in range(len(colums))]
    row[0] = person['firstName']    
    row[1] = person['lastName']    
    row[2] = person['gender']
    row[3] = person['age']
    row[4] = string_to_time(result['gunTime'])
    row[5] = string_to_time(result['finishTime'])
    row[6] = format_time_result(result['chipTimeResult'])
    row[7] = format_time_result(result['gunTimeResult'])
    row[8] = format_time_result(result['finalResult'])
    row[9] = result['averageSpeed']
    row[10] = result['disqualified']
    row[11] = splits[0]['speed'] if 'speed' in splits[0] else None
    row[12] = splits[1]['speed'] if 'speed' in splits[1] else None
    row[13] = splits[2]['speed'] if 'speed' in splits[2] else None
    row[14] = splits[3]['speed'] if 'speed' in splits[3] else None
    row[15] = splits[4]['speed'] if 'speed' in splits[4] else None   
 
    for rank in item['groupRanks']:
        row[colums[rank['name']]] = rank['rank']
    return row

async def fetchDeep(session, url,colums):
    rows = []
    async with session.get(url) as response:
        items = (await response.json())['items']
    for item in items:
        id = item['id']
        user_url = f"https://resultscui.active.com/api/results/participants/{id}"
        result_url = f"https://resultscui.active.com/api/results/participants/{id}/splits"
        data = None
        result = None

        async with session.get(user_url) as response:
            data = (await response.json())
        async with session.get(result_url) as response:
            result = (await response.json())[1:]
        
        rows.append(getRow(data,result,colums))
    return rows
        
        
async def getDataDeep(outfile):
    colums = {
    'firstname': 0,
    'lastname': 1,
    'gender': 2,
    'age': 3,
    'gun time': 4,
    'finish time': 5,
    'ship time result': 6,
    'gun time result': 7,
    'final result': 8,
    'average speed': 9,
    'discalified': 10,
    '5 km speed': 11,
    '10 km speed': 12,
    '15 km speed': 13,
    '20 km speed': 14,
    'finish speed': 15,
    }
    index = 16
    groups = requests.get("https://resultscui.active.com/api/results/events/HarmonieMutuelleSemideParis2024").json()['routes'][0]['groups']
    for group in groups:
        colums[group["name"]] = index
        index += 1

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(list(colums.keys()))
    offset = 0
    limit = 100
    max_person = 47800
    urls = []
    while(offset<max_person):
        urls.append(f"https://resultscui.active.com/api/results/events/HarmonieMutuelleSemideParis2024/participants?groupId=1022082&routeId=176712&offset={offset}&limit={limit}")
        offset += limit
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetchDeep(session, url,colums)) for url in urls]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            for row in response:
                sheet.append(row)
        workbook.save(f"{outfile}.xlsx")
