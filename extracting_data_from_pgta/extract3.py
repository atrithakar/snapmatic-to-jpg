import os
import json

def extractTitle(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    # print(data)
    titleIdx = data.index(b'TITL')
    # title = data[start:end].
    start = titleIdx + 8
    end = data.find(b'\x00', start)

    title = data[start:end].decode('utf-8', errors='ignore')
    return title

def extractJSON(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    # print(data)
    start = data.index(b'{"loc"')
    # title = data[start:end].

    end = data.find(b'\x00', start)

    json_data = data[start:end].decode('utf-8', errors='ignore')
    return json.loads(json_data)

    # return data[jsonIdx:jsonIdx+600].decode('utf-8', errors='ignore')

def extractLocation(json):
    return json['loc']

def extractIngameTime(json):
    return json['time']

def extractRealWorldTimestamp(json):
    return json['creat']

def extractRadioStation(json):
    return json['rds'] or 'none'

json1 = extractJSON('/home/atri/test_prefix/drive_c/users/atri/AppData/Roaming/Goldberg SocialClub Emu Saves/GTA V/0F74F4C4/PGTA51098123832')
json2 = extractJSON('/home/atri/Desktop/snapmatic_to_jpg/PGTA5236660974copy')

print(f'{extractLocation(json1)}    {extractLocation(json2)}')
print(f'{extractIngameTime(json1)}    {extractIngameTime(json2)}')
print(f'{extractRealWorldTimestamp(json1)}    {extractRealWorldTimestamp(json2)}')
print(f'{extractRadioStation(json1)}    {extractRadioStation(json2)}')