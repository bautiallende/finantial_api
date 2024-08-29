import requests
from bs4 import BeautifulSoup


def obtener_datos_bono_rava(bono):
    url = f"https://www.rava.com/perfil/{bono}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error al acceder a la página: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Depuración: Mostrar parte del HTML completo para verificar el contenido
    print(f"HTML de la página (primeros 1000 caracteres):\n{soup.prettify()[:]}")
    
    # Intentar encontrar los elementos esperados
    izq_cotiza = soup.find("div", class_="positivo")
    if izq_cotiza:
        print(f"Encontrado div Cotizacion-c: {izq_cotiza.prettify()[:200]}")
    else:
        print("No se encontró el div Cotizacion-c.")
    
    # Otros selectores se deben ajustar según la inspección manual del HTML
    # Agregar la lógica adicional aquí, basada en los nuevos hallazgos

    return None  # Temporalmente, hasta ajustar la lógica