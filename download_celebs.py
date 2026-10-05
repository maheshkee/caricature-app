import urllib.request
import os

os.makedirs("celebrities", exist_ok=True)
celebs = {
    "Brad_Pitt.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Brad_Pitt_2019_by_Glenn_Francis.jpg/400px-Brad_Pitt_2019_by_Glenn_Francis.jpg",
    "Zendaya.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Zendaya_-_2019_by_Glenn_Francis.jpg/400px-Zendaya_-_2019_by_Glenn_Francis.jpg",
    "Kevin_Hart.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Kevin_Hart_2014.jpg/400px-Kevin_Hart_2014.jpg",
    "Tom_Cruise.jpg": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Tom_Cruise_by_Gage_Skidmore_2.jpg/400px-Tom_Cruise_by_Gage_Skidmore_2.jpg"
}

for name, url in celebs.items():
    print(f"Downloading {name}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(os.path.join("celebrities", name), 'wb') as out_file:
        out_file.write(response.read())
print("Done downloading celebrities.")
