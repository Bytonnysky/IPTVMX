import re
import urllib.request

URL_ORIGINAL = "https://raw.githubusercontent.com/JMigue85/IPTV-SV/refs/heads/main/IPTVSV.m3u"
ARCHIVO_SALIDA = "mexico.m3u"

# Países que queremos reconocer como grupos de país.
PAISES = {
    "México",
    "El Salvador",
    "Guatemala",
    "Honduras",
    "Nicaragua",
    "Costa Rica",
    "Panamá",
    "Colombia",
    "Venezuela",
    "Ecuador",
    "Perú",
    "Bolivia",
    "Chile",
    "Argentina",
    "Uruguay",
    "Paraguay",
    "Brasil",
    "España",
    "Portugal",
    "Estados Unidos",
    "Canadá",
    "Puerto Rico",
    "República Dominicana",
    "Cuba",
    "Jamaica",
    "Haití",
    "Belice",
    "Trinidad y Tobago",
    "Guayana",
    "Surinam",
    "Francia",
    "Italia",
    "Alemania",
    "Reino Unido",
    "Rusia",
    "China",
    "Japón",
    "Corea del Sur",
    "India",
    "Turquía",
    "Australia",
}

def obtener_lista():
    print("Descargando lista original...")
    with urllib.request.urlopen(URL_ORIGINAL, timeout=60) as respuesta:
        return respuesta.read().decode("utf-8", errors="ignore")


def es_grupo_de_pais(group):
    """
    Detecta grupos como:
    México
    México - Noticias
    El Salvador
    El Salvador - TCS
    Guatemala
    """
    group = group.strip()

    for pais in PAISES:
        if group == pais or group.startswith(pais + " -"):
            return pais

    return None


def filtrar_lista(texto):
    lineas = texto.splitlines()
    resultado = ["#EXTM3U"]

    i = 1

    while i < len(lineas):
        linea = lineas[i]

        if not linea.startswith("#EXTINF:"):
            i += 1
            continue

        # Obtener group-title
        match = re.search(r'group-title="([^"]*)"', linea)

        if not match:
            # Si no tiene grupo, lo conservamos.
            conservar = True
        else:
            grupo = match.group(1)
            pais = es_grupo_de_pais(grupo)

            # Si es un grupo de país:
            # solamente conservamos México.
            if pais is not None:
                conservar = pais == "México"
            else:
                # No es un grupo de país:
                # Deportes, Películas, Series, Música, etc.
                # se conservan.
                conservar = True

        # Una entrada M3U puede ocupar varias líneas:
        # EXTINF + opciones VLC + URL.
        entrada = [linea]
        j = i + 1

        while j < len(lineas):
            siguiente = lineas[j]

            if siguiente.startswith("#EXTINF:"):
                break

            if siguiente.strip():
                entrada.append(siguiente)

            j += 1

        if conservar:
            resultado.extend(entrada)

        i = j

    return "\n".join(resultado) + "\n"


def main():
    original = obtener_lista()
    filtrada = filtrar_lista(original)

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as archivo:
        archivo.write(filtrada)

    print(f"Lista creada: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    main()
