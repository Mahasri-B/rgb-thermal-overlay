import requests
import os

INPUT_DIR = 'input-images'
PAIR_BASE = 'DJI_20250530121540_0001'  # change if you want a different pair

thermal_path = os.path.join(INPUT_DIR, PAIR_BASE + '_T.JPG')
rgb_path = os.path.join(INPUT_DIR, PAIR_BASE + '_Z.JPG')

if not os.path.exists(thermal_path) or not os.path.exists(rgb_path):
    print('Test pair not found:', thermal_path, rgb_path)
    raise SystemExit(1)

files = {
    'thermal': open(thermal_path, 'rb'),
    'rgb': open(rgb_path, 'rb')
}

print('Uploading', thermal_path, 'and', rgb_path)
resp = requests.post('http://127.0.0.1:5000/align', files=files)
if resp.status_code != 200:
    print('Server returned', resp.status_code, resp.text)
    raise SystemExit(1)

out_zip = 'output/aligned_result.zip'
os.makedirs('output', exist_ok=True)
with open(out_zip, 'wb') as f:
    f.write(resp.content)

print('Saved result to', out_zip)

import zipfile
with zipfile.ZipFile(out_zip, 'r') as zf:
    print('Zip contents:', zf.namelist())
    zf.extractall('output')
    print('Extracted to output/')
