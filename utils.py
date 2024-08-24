import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_sheet(sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client.open('Inversiones').worksheet(sheet_name)




def obtener_datos_yahoo(ticker, datos):
    print(f"Iniciando scraping para {ticker}...")
    
    url = f"https://finance.yahoo.com/quote/{ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Esto lanzará un error si la respuesta no es 200 OK
    except requests.exceptions.HTTPError as http_err:
        print(f"Error HTTP al intentar acceder a {ticker}: {http_err}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error de conexión al intentar acceder a {ticker}: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        print(f"Tiempo de espera agotado al intentar acceder a {ticker}: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Error inesperado al intentar acceder a {ticker}: {req_err}")
        return None

    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        resultados = {}
        for key, value in datos.items():
            elemento = soup.find("fin-streamer", value)
            if elemento:
                resultados[key] = elemento.text
            elif key in ["precio_minimo", "precio_maximo"]:
                rango = soup.find("fin-streamer", {"data-field": "regularMarketDayRange"})
                if rango:
                    minimo, maximo = rango.text.split(" - ")
                    resultados[key] = minimo if key == "precio_minimo" else maximo
                else:
                    resultados[key] = None
            else:
                resultados[key] = None
        
        # Extract additional information
        nombre_completo = soup.find("h1", class_="yf-3a2v0c").text if soup.find("h1", class_="yf-3a2v0c") else None
        mercado_moneda = soup.find("span", class_="exchange yf-1fo0o81").text if soup.find("span", class_="exchange yf-1fo0o81") else None
        if mercado_moneda:
            mercado = mercado_moneda.split(" - ")[0].strip()
            moneda = mercado_moneda.split("•")[-1].strip()
        else:
            mercado, moneda = None, None

        resultados.update({
            "nombre_completo": nombre_completo,
            "mercado": mercado,
            "moneda": moneda,
            "fuente": "Yahoo Finance"
        })
        
        return resultados
    
    except AttributeError as attr_err:
        print(f"Error de atributo al procesar {ticker}: {attr_err}")
        return None
    except Exception as err:
        print(f"Error inesperado al procesar {ticker}: {err}")
        return None




def obtener_fecha_actual():
    from datetime import datetime
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

