import gspread
from utils import get_sheet, obtener_precio_yahoo, obtener_dato_yahoo, obtener_fecha_actual, obtener_nombre_completo, obtener_mercado_moneda



def actualizar_cotizaciones():
    # Obtener la hoja de cálculo
    sheet = get_sheet("Cotizaciones y Tipo de Cambio")
    
    # Obtener todos los tickers listados en la columna B, comenzando desde la fila 8
    tickers = sheet.col_values(2)[7:]
    print(f'Tickers: {tickers}')

    # Iterar sobre cada ticker y actualizar la información
    for i, ticker in enumerate(tickers, start=8):
        fecha = obtener_fecha_actual()
        nombre_completo = obtener_nombre_completo(ticker)
        mercado, moneda = obtener_mercado_moneda(ticker)
        precio_apertura = obtener_dato_yahoo(ticker, "regularMarketOpen")
        precio_cierre = obtener_dato_yahoo(ticker, "regularMarketPreviousClose")
        precio_minimo = obtener_dato_yahoo(ticker, "regularMarketDayLow")
        precio_maximo = obtener_dato_yahoo(ticker, "regularMarketDayHigh")
        cotizacion_moneda_local = obtener_precio_yahoo(ticker)
        volumen = obtener_dato_yahoo(ticker, "regularMarketVolume")
        variacion_diaria = obtener_dato_yahoo(ticker, "regularMarketChangePercent")
        
        # Actualizar la celda solo si tenemos un valor válido
        if fecha:
            sheet.update_cell(i, 1, fecha)
        if nombre_completo:
            sheet.update_cell(i, 3, nombre_completo)
        if mercado:
            sheet.update_cell(i, 4, mercado)
        if moneda:
            sheet.update_cell(i, 6, moneda)
        if precio_apertura:
            sheet.update_cell(i, 7, precio_apertura)
        if precio_cierre:
            sheet.update_cell(i, 8, precio_cierre)
        if precio_minimo:
            sheet.update_cell(i, 9, precio_minimo)
        if precio_maximo:
            sheet.update_cell(i, 10, precio_maximo)
        if cotizacion_moneda_local:
            sheet.update_cell(i, 11, cotizacion_moneda_local)
        if volumen:
            sheet.update_cell(i, 14, volumen)
        if variacion_diaria:
            sheet.update_cell(i, 15, variacion_diaria)
        # Actualizar la fuente de la cotización
        sheet.update_cell(i, 16, "Yahoo Finance")

def obtener_tipo_cambio():
    # Aquí puedes implementar una función para obtener el tipo de cambio del dólar MEP
    return 945.2586  # Ejemplo estático; puedes actualizarlo dinámicamente

def calcular_variacion_diaria(cierre_anterior, precio_actual):
    if cierre_anterior and precio_actual:
        return round(((precio_actual - cierre_anterior) / cierre_anterior) * 100, 2)
    return 0.0