import os
import json
import urllib.request
import re

def limpiar_nombre_visible(nombre_archivo):
    return nombre_archivo.replace('_', ' ')

# 1. Obtener versión y datos de Data Dragon para orden cronológico y biografía
version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
try:
    with urllib.request.urlopen(version_url) as response:
        latest_version = json.loads(response.read().decode('utf-8'))[0]
except:
    latest_version = "14.1.1"

champions_data_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
req = urllib.request.Request(champions_data_url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        champions_dict = json.loads(response.read().decode('utf-8'))["data"]
except Exception as e:
    print(f"Error al obtener datos de campeones: {e}")
    champions_dict = {}

# Ruta local de las imágenes de los campeones
imagenes_base_dir = os.path.join("imagenes", "campeones")

if not os.path.exists(imagenes_base_dir):
    print(f"No se encontró la ruta {imagenes_base_dir}.")
    exit()

carpetas_campeones = [d for d in os.listdir(imagenes_base_dir) if os.path.isdir(os.path.join(imagenes_base_dir, d))]

print(f"Generando páginas HTML en la carpeta 'campeones' para {len(carpetas_campeones)} campeones...\n")

for champ_id in sorted(carpetas_campeones):
    dir_champ = os.path.join(imagenes_base_dir, champ_id)
    archivos_webp = [f for f in os.listdir(dir_champ) if f.endswith('.webp')]
    
    if not archivos_webp:
        continue
    
    api_id = "MonkeyKing" if champ_id == "Wukong" else champ_id
    detail_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion/{api_id}.json"
    
    lore_texto = f"{champ_id} es un campeón de League of Legends con un poder formidable en la Grieta del Invocador."
    orden_skins_nums = {}
    
    try:
        req_detail = urllib.request.Request(detail_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_detail) as resp_detail:
            champ_detail = json.loads(resp_detail.read().decode('utf-8'))
            info_campeon = champ_detail["data"][list(champ_detail["data"].keys())[0]]
            
            if "blurb" in info_campeon:
                lore_texto = info_campeon["blurb"]
            
            for skin in info_campeon["skins"]:
                skin_num = skin["num"]
                skin_name_raw = skin["name"]
                
                if skin_num == 0 or skin_name_raw.lower() == api_id.lower() or skin_name_raw.lower() == "default":
                    nombre_limpio = champ_id
                else:
                    nombre_limpio = re.sub(r'[^a-zA-Z0-9\s]', '', skin_name_raw).strip().replace(' ', '_')
                
                orden_skins_nums[nombre_limpio] = skin_num
    except Exception:
        pass

    # Ordenar cronológicamente basándonos en la API
    def criterio_orden(archivo):
        nombre_sin_ext = os.path.splitext(archivo)[0]
        return orden_skins_nums.get(nombre_sin_ext, 999)

    archivos_webp.sort(key=criterio_orden)

    # Construir las tarjetas HTML
    tarjetas_html = ""
    for archivo in archivos_webp:
        nombre_sin_ext = os.path.splitext(archivo)[0]
        nombre_bonito = limpiar_nombre_visible(nombre_sin_ext)
        
        # Como el HTML estará dentro de la carpeta 'campeones', para llegar a imagenes subimos un nivel con '../'
        ruta_img = f"../imagenes/campeones/{champ_id}/{archivo}"
        
        tarjetas_html += f"""                <article class="campeon-tarjeta">
                    <img src="{ruta_img}" alt="{nombre_bonito}">
                    <p>{nombre_bonito}</p>
                </article>\n"""

    # Estructura del HTML adaptada a tus carpetas (estilos y enlaces relativos)
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skins {champ_id}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.4/css/bulma.min.css">
    <link rel="stylesheet" href="../estilos/estilo-campeon.css">
</head>
<body>
     <header>
        <h1>SummonerCloset</h1>
        <nav>
            <a class="inicio" onclick="window.location.href='../index.html'">inicio</a>
            <a href="#footer">nosotros</a>
            <a href="#footer">contacto</a>
        </nav>
    <a href="#">iniciar sesión</a>
    </header>
    <main>
        <section class="campeones">
            <div class="campeones-tarjetas">
{tarjetas_html}            </div>
            <section class="texto">
                <p>{lore_texto}</p>
            </section>
        </section>
    </main>
    <footer id="footer">
        <div class="footer-paginas">
            <h3>NUESTRAS REDES</h3>
            <a href="https://www.facebook.com/RiotGames">Facebook</a>
            <a href="https://www.instagram.com/riotgames">Instagram</a>
        </div>
        <div class="derechos">
            <p>Todos los derechos reservados a tilinazo67</p>
        </div>
        <div class="riot">
            <h3>PÁGINA OFICIAL</h3>
            <a href="https://www.riotgames.com" class="riot-link">Página oficial</a>
        </div>
    </footer>
</body>
</html>
"""

    # Guardar directamente dentro de la carpeta 'campeones' que ya tienes creada en la raíz
    os.makedirs("campeones", exist_ok=True)
    archivo_html_path = os.path.join("campeones", f"{champ_id.lower()}.html")
    
    with open(archivo_html_path, 'w', encoding='utf-8') as f:
        f.write(html_template)

print("\n¡Listo! Todos los archivos HTML de los campeones se han creado ordenados y con sus imágenes locales dentro de tu carpeta 'campeones'.")