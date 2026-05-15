import os
import json
from datetime import datetime, timezone

def find_pgta(start_path = os.path.expanduser('~')):
    snapmatics = []

    ignored_dirs = {'/proc', '/sys', '/dev', '/run', '.local/share/Trash'}

    print(f"Searching for files at path {start_path}")
    for root, dirs, files in os.walk(start_path):

        dirs[:] = [d for d in dirs if not any(ignored in os.path.join(root, d) for ignored in ignored_dirs)]

        for file in files:
            if file.startswith('PGTA') and '.' not in file and '_' not in file:
                # print(f'found {file}')
                snapmatics.append(os.path.join(root, file))

    return snapmatics

def extract_pgta_data(data):

    title = "Unknown"
    json_obj = {}

    title_idx = data.find(b'TITL')
    if title_idx != -1:
        start = title_idx + 8
        end = data.find(b'\x00', start)
        if end != -1:
            title = data[start:end].decode('utf-8', errors='ignore')
    
    json_idx = data.find(b'{"loc"')
    if json_idx != -1:
        end = data.find(b'\x00', json_idx)
        if end != -1:
            json_string = data[json_idx:end].decode('utf-8', errors='ignore')
            try:
                json_obj = json.loads(json_string)
            except json.JSONDecodeError:
                pass 

    return title, json_obj


def getJsonFields(json_obj, field_name, alt_value = 'none'):
    return json_obj.get(field_name) or alt_value

def convert_snapmatic_to_jpg(snapmatic_file_path):

    if not snapmatic_file_path:
        print("Empty file path")
        return

    try:
        with open(snapmatic_file_path, 'rb') as f:
            data = f.read()
            jpeg_start = data.find(b'\xff\xd8\xff')
    except FileNotFoundError:
        print("Invalid file path")
        return

    title, json_obj = extract_pgta_data(data)
    coords = getJsonFields(json_obj, 'loc')
    in_game_time = getJsonFields(json_obj, 'time')
    real_world_time_unix_epoch = getJsonFields(json_obj, 'creat')
    radio_station = getJsonFields(json_obj, 'rds', 'Radio Off')
    real_world_time_utc = datetime.fromtimestamp(real_world_time_unix_epoch, tz=timezone.utc)

    formatted_real_world_time = {
        "hour": real_world_time_utc.hour,
        "minute": real_world_time_utc.minute,
        "second": real_world_time_utc.second,
        "day": real_world_time_utc.day,
        "month": real_world_time_utc.month,
        "year": real_world_time_utc.year
    }

    if jpeg_start != -1:
        clean_jpg_data = data[jpeg_start:]

        # out_file = snapmatic_file_path + '.jpg'
        out_dir = os.path.join(os.getcwd(), 'converted', f'{title}_{real_world_time_unix_epoch}')

        os.makedirs(out_dir, exist_ok=True)

        out_img = os.path.join(out_dir, 'image.jpg')
        out_info = os.path.join(out_dir, 'info.txt')

        with open(out_img, 'wb') as f_out:
            f_out.write(clean_jpg_data)
            print(f"Extracted {out_img}")

        with open(out_info, 'w') as f_out:
            f_out.write(f'TITLE: {title}\nLOCATION: {coords}\nIN GAME TIME: {in_game_time}\nREAL WORLD TIME: {formatted_real_world_time}\nRADIO STATION: {radio_station}\n')
    else:
        print("failed to extract")


if __name__ == "__main__":
    # print_snapmatics(find_pgta())
    convert_snapmatic_to_jpg('/home/atri/test_prefix/drive_c/users/atri/AppData/Roaming/Goldberg SocialClub Emu Saves/GTA V/0F74F4C4/PGTA51810636364')
