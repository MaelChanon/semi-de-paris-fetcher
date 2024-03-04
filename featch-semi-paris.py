import sys
import asyncio
from fetch import getData
from fetchdeep import getDataDeep
import json 


# Use strptime to convert the string to a datetime object
def main():
    loop = asyncio.get_event_loop() 
    match len(sys.argv):
       case 2:
          loop.run_until_complete(getData(sys.argv[1]))
       case 3:
          if(sys.argv[1] != "deep"): raise Exception("unknow first argument, possible value ['deep']")
          loop.run_until_complete(getDataDeep(sys.argv[2]))
       case _:
          raise Exception("Usage: python featch-semi-paris (deep) <filename>")
    
if __name__ == "__main__":
    main()