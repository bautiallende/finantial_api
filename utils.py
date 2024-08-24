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



def obtener_precio_yahoo(ticker):
    print(f"Obteniendo precio actual para {ticker} desde Yahoo Finance...")
    url = f"https://finance.yahoo.com/quote/{ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    print(f"Respuesta recibida de {url}, estatus: {response.status_code}")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Log para verificar el HTML recibido
    print(f"HTML recibido para {ticker}: {soup.prettify()[:500]}")
    
    # Scraping del precio actual
    precio_actual = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
    if precio_actual:
        print(f"Precio actual encontrado para {ticker}: {precio_actual.text}")
        return precio_actual.text
    else:
        print(f"No se pudo encontrar el precio para {ticker}")
        return None

def obtener_dato_yahoo(ticker, data_field):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    dato = soup.find("fin-streamer", {"data-field": data_field})
    if dato:
        return dato.text
    else:
        print(f"No se pudo encontrar {data_field} para {ticker}")

        # Intentar obtener el rango completo si no se encuentra un dato específico
        if data_field in ["regularMarketDayLow", "regularMarketDayHigh"]:
            rango = soup.find("fin-streamer", {"data-field": "regularMarketDayRange"})
            if rango:
                try:
                    minimo, maximo = rango.text.split(" - ")
                    return minimo if data_field == "regularMarketDayLow" else maximo
                except ValueError:
                    print(f"No se pudo dividir el rango para {ticker}")
                    return None
        return None

def obtener_nombre_completo(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        nombre_completo = soup.find("h1", class_="yf-3a2v0c").text
        nombre_completo = nombre_completo.split(" (")[0]  # Eliminar el ticker del nombre
        return nombre_completo
    except AttributeError:
        print(f"No se pudo encontrar el nombre completo para {ticker}")
        return None

def obtener_mercado_moneda(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        mercado_moneda = soup.find("span", class_="exchange yf-1fo0o81").text
        mercado = mercado_moneda.split(" - ")[0].strip()  # Eliminar "Delayed Quote"
        moneda = mercado_moneda.split("•")[-1].strip()  # Captura la moneda después del punto medio
        return mercado, moneda
    except AttributeError:
        print(f"No se pudo encontrar el mercado y la moneda para {ticker}")
        return None, None

def obtener_fecha_actual():
    from datetime import datetime
    return datetime.now().strftime('%d/%m/%Y')