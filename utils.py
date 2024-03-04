from datetime import datetime

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

