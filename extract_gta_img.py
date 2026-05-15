import os
from extracting_data_from_pgta.extract3 import *
from datetime import datetime, timezone

def find_pgta(start_path = os.path.expanduser('~')):
    snapmatics = []

    ignored_dirs = {'/proc', '/sys', '/dev', '/run', '.local/share/Trash'}

    print(f"Searching for files at path {start_path}")
    for root, dirs, files in os.walk(start_path):

        if any(ignored in root for ignored in ignored_dirs):
            continue

        for file in files:
            if file.startswith('PGTA') and '.' not in file and '_' not in file:
                # print(f'found {file}')
                snapmatics.append(os.path.join(root, file))

    return snapmatics

def extract_snapmatic(snapmatics):

    if not snapmatics or len(snapmatics) == 0:
        print("No images found")
        return

    for file in snapmatics:
        with open(file, 'rb') as f:
            data = f.read()
            jpeg_start = data.find(b'\xff\xd8\xff')

            if jpeg_start != -1:
                clean_jpg_data = data[jpeg_start:]

                out_file = file + '.jpg'

                with open(out_file, 'wb') as f_out:
                    f_out.write(clean_jpg_data)
                    print(f"Extracted {out_file}")
            else:
                print("failed to extract")


def print_snapmatics(snapmatics):
    if not snapmatics or len(snapmatics) == 0:
        print("No images found")
        return

    for snapmatic in snapmatics:
        print(f'FILE_PATH: {snapmatic}')
        title, json_obj = extract_pgta_data(snapmatic)
        # json_obj = extractJSON(snapmatic)
        print(f'TITLE: {title}')

        coords = getJsonFields(json_obj, 'loc')
        in_game_time = getJsonFields(json_obj, 'time')
        real_world_time_unix_epoch = getJsonFields(json_obj, 'creat')
        radio_station = getJsonFields(json_obj, 'rds', 'Radio Off')
        real_world_time_utc = datetime.fromtimestamp(real_world_time_unix_epoch, tz=timezone.utc)

        formatted_real_world_time = json.loads(
            f'''
            {{
                "hour" : {real_world_time_utc.hour},
                "minute" : {real_world_time_utc.minute},
                "second" : {real_world_time_utc.second},
                "day" : {real_world_time_utc.day},
                "month" : {real_world_time_utc.month},
                "year" : {real_world_time_utc.year}
            }}
            '''
        )

        print(f'LOCATION: {coords}\nIN GAME TIME: {in_game_time}\nREAL WORLD TIME: {formatted_real_world_time}\nRADIO STATION: {radio_station}\n')


if __name__ == "__main__":
    print_snapmatics(find_pgta())
