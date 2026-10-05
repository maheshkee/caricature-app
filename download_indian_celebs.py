import urllib.request
import urllib.parse
import json
import os

celebs = [
    "Virat Kohli", "MS Dhoni", "Allu Arjun", "Mahesh Babu", 
    "Prabhas", "Ram Charan", "N. T. Rama Rao Jr.", "Pawan Kalyan",
    "Shah Rukh Khan", "Salman Khan", "Rajinikanth", 
    "Deepika Padukone", "Samantha Ruth Prabhu", "Anushka Shetty", "Nayanthara"
]

os.makedirs("indian_celebs", exist_ok=True)

for celeb in celebs:
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(celeb)}&prop=pageimages&format=json&pithumbsize=600"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            pages = data['query']['pages']
            for page_id, page_info in pages.items():
                if 'thumbnail' in page_info:
                    img_url = page_info['thumbnail']['source']
                    img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(img_req) as img_res, open(f"indian_celebs/{celeb.replace(' ', '_')}.jpg", 'wb') as f:
                        f.write(img_res.read())
                    print(f"Downloaded {celeb}")
                else:
                    print(f"No image found for {celeb}")
    except Exception as e:
        print(f"Error downloading {celeb}: {e}")
