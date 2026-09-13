import os
import urllib.request

dir_path = os.path.join("imagenes", "campeones", "Fiddlesticks")
os.makedirs(dir_path, exist_ok=True)

file_path = os.path.join(dir_path, "Fiddlesticks.webp")
image_url = "https://ddragon.leagueoflegends.com/cdn/img/champion/loading/Fiddlesticks_0.jpg"
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    req = urllib.request.Request(image_url, headers=headers)
    with urllib.request.urlopen(req) as response, open(file_path, 'wb') as out_file:
        out_file.write(response.read())
    print("¡Fiddlesticks actualizado a su versión moderna correctamente!")
except Exception as e:
    print(f"Error: {e}")