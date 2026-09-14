import os
import json
import urllib.request
import re

def limpiar_nombre_archivo(nombre):
    limpio = re.sub(r'[^a-zA-Z0-9\s]', '', nombre)
    return limpio.strip().replace(' ', '_')

# Obtener la versión más reciente de Data Dragon
version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
try:
    with urllib.request.urlopen(version_url) as response:
        versions = json.loads(response.read().decode('utf-8'))
        latest_version = versions[0]
except Exception:
    latest_version = "14.1.1"

# Idioma en_US para nombres originales en inglés
champions_data_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
req = urllib.request.Request(champions_data_url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        champions_dict = data["data"]
except Exception as e:
    print(f"Error al obtener campeones: {e}")
    champions_dict = {}

headers = {'User-Agent': 'Mozilla/5.0'}
base_skin_url = "https://ddragon.leagueoflegends.com/cdn/img/champion/loading/"

nombres_campeones = sorted(champions_dict.keys())
try:
    inicio_idx = nombres_campeones.index("Darius")
except ValueError:
    inicio_idx = 0

campeones_a_procesar = nombres_campeones[inicio_idx:]

print("Iniciando descarga limpia (excluyendo cromas y base, nombres en inglés)...")

for champ_id in campeones_a_procesar:
    detail_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion/{champ_id}.json"
    
    try:
        req_detail = urllib.request.Request(detail_url, headers=headers)
        with urllib.request.urlopen(req_detail) as resp_detail:
            champ_detail = json.loads(resp_detail.read().decode('utf-8'))
            skins = champ_detail["data"][champ_id]["skins"]
            
            dir_path = os.path.join("imagenes", "campeones", champ_id)
            os.makedirs(dir_path, exist_ok=True)
            
            for skin in skins:
                skin_num = skin["num"]
                
                # Omitir skin base (0)
                if skin_num == 0:
                    continue 
                
                # Los cromas en la API de League of Legends suelen tener un num >= 1000 
                # o se identifican explícitamente. Omitimos todo lo que sea un croma (> 1000 o con patrón de croma).
                if skin_num >= 1000 or skin.get("chromas", False):
                    continue
                
                skin_name_raw = skin["name"]
                
                if skin_name_raw.lower() == champ_id.lower() or skin_name_raw == "default":
                    skin_nombre_limpio = f"{champ_id}_Skin_{skin_num}"
                else:
                    skin_nombre_limpio = limpiar_nombre_archivo(skin_name_raw)
                
                file_path = os.path.join(dir_path, f"{skin_nombre_limpio}.webp")
                image_url = f"{base_skin_url}{champ_id}_{skin_num}.jpg"
                
                try:
                    req_img = urllib.request.Request(image_url, headers=headers)
                    with urllib.request.urlopen(req_img) as img_resp, open(file_path, 'wb') as out_file:
                        out_file.write(img_resp.read())
                    print(f"[SKIN OK] {champ_id} -> {skin_nombre_limpio}.webp")
                except Exception as img_err:
                    print(f"[AVISO] Skin '{skin_name_raw}' de {champ_id} no disponible en CDN.")
                    
    except Exception as detail_err:
        print(f"[ERROR] Falló detalles de {champ_id}: {detail_err}")

print("¡Descarga de skins puras (sin cromas) finalizada con éxito!")