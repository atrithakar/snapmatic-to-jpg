import os

def extract_snapmatic():
    files = [f for f in os.listdir('.') if f.startswith('PGTA') and not f.endswith('.jpg')]

    if not files:
        print("No files found to convert")

    for file in files:
        with open(file, 'rb') as f:
            data = f.read()
            jpeg_start = data.find(b'\xff\xd8\xff')

            if jpeg_start != -1:
                clean_jpg_data = data[jpeg_start:]

                out_file = file + '.jpg'

                with open(out_file, 'wb') as f_out:
                    f_out.write(clean_jpg_data)
                    print("Extracted {out_file}")
            else:
                print("failed to extract")


if __name__ == "__main__":
    extract_snapmatic()
