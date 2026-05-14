import os

def find_pgta(start_path = os.path.expanduser('~')):
    matches = []

    ignored_dirs = {'/proc', '/sys', '/dev', '/run', '.local/share/Trash'}

    print(f"Searching for files at path {start_path}")
    for root, dirs, files in os.walk(start_path):

        if any(ignored in root for ignored in ignored_dirs):
            continue

        for file in files:
            if file.startswith('PGTA') and '.' not in file and '_' not in file:
                # print(f'found {file}')
                matches.append(os.path.join(root, file))

    return matches

def extract_snapmatic(matches):

    if not matches or len(matches) == 0:
        print("No images found")
        return

    for file in matches:
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

def print_matches(matches):
    if not matches or len(matches) == 0:
        print("No images found")
        return
    
    print('[')

    for match in matches:
        print(f'    {match},')

    print(']')

if __name__ == "__main__":
    # extract_snapmatic()
    # print(find_pgta('/home/atri/test_prefix/drive_c/users/atri/AppData/Roaming/Goldberg SocialClub Emu Saves/GTA V/0F74F4C4'))
    print_matches(find_pgta('/home/atri/test_prefix/drive_c/users/atri/AppData/Roaming/Goldberg SocialClub Emu Saves/GTA V/0F74F4C4'))
    # print(parse_pgta_header('/home/atri/test_prefix/drive_c/users/atri/AppData/Roaming/Goldberg SocialClub Emu Saves/GTA V/0F74F4C4/PGTA5519163650'))
