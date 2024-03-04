import requests
import openpyxl
import datetime
from datetime import datetime
import sys
def fetch_coureur(limit,offset):
    url = f"https://resultscui.active.com/api/results/events/HarmonieMutuelleSemideParis2024/participants?groupId=1022082&routeId=176712&offset={offset}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        test += 1
        print(f"{test}/480")
        return getRow(response.json()['items'][0])
    raise Exception("error fetching data")
def string_to_time(date_string):
    date_time_format = "%Y-%m-%d %H:%M:%S"
    return datetime.fromisoformat(date_string[:-1] + '+00:00').strftime(date_time_format)
def format_time_result(result):
    horaire = {
        "H":"0",
        "M":"0",
        "S":"0"
    }
    for i in horaire.keys():
        index = result.find(i)
        if(index != -1):
            horaire[i] = result[index-2:index] if (result[index-2] not in ["H","M","S","T"]) else f"0{result[index-1]}"
        else:
            horaire[i] = "00"
    return f"{horaire['H']}:{horaire['M']}:{horaire['S']}"
    
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
def getData(outfile):
    colums = ['firstname','lastname','gender','age','gun time','finish time','ship time result','gun time result','final result','average speed','discalified']
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(colums)
    offset = 0
    limit = 100
    max_person = 47800
    loop_count = 0
    while(offset<max_person):
      url = f"https://resultscui.active.com/api/results/events/HarmonieMutuelleSemideParis2024/participants?groupId=1022082&routeId=176712&offset={offset}&limit={limit}"
      response = requests.get(url)
      if response.status_code == 200:
        loop_count += 1
        print(f"{loop_count}/{max_person/limit}")
        for item in response.json()['items']:
          sheet.append(getRow(item))
      else: 
        raise Exception("error fetching data")
      offset += limit
    workbook.save('example.xlsx')
# Use strptime to convert the string to a datetime object
def main():
    match len(sys.argv):
       case 2: 
          getData(sys.argv[1])
       case _:
          raise Exception("Usage: python featch-semi-paris (deep) <filename>")
    
if __name__ == "__main__":
    main()