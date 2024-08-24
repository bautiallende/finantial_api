import gspread
from utils import get_sheet, obtener_fecha_actual, obtener_datos_yahoo



def actualizar_cotizaciones():
    # Obtener la hoja de cálculo
    sheet = get_sheet("Cotizaciones y Tipo de Cambio")
    
    # Obtener todos los tickers listados en la columna B, comenzando desde la fila 8
    tickers = sheet.col_values(2)[7:]
    activos = sheet.col_values(5)[7:]
    print(f'Tickers: {tickers}')
    print(f'Activos: {activos}')

    # Iterar sobre cada ticker y actualizar la información
    for i, (ticker, activo) in enumerate(zip(tickers, activos), start=8):
        if activo.lower() == "acciones":
            print(f"Procesando {ticker} - {activo}")

            # Diccionario para mapear los datos que queremos extraer
            datos = {
                "precio_apertura": {"data-field": "regularMarketOpen"},
                "precio_cierre": {"data-field": "regularMarketPreviousClose"},
                "precio_minimo": {"data-field": "regularMarketDayLow"},
                "precio_maximo": {"data-field": "regularMarketDayHigh"},
                "precio_actual": {"data-field": "regularMarketPrice"},
                "volumen": {"data-field": "regularMarketVolume"},
                "variacion_diaria": {"data-field": "regularMarketChangePercent"},
                }

            resultados = obtener_datos_yahoo(ticker, datos)

            if resultados:
                fecha = obtener_fecha_actual()
                nombre_completo = resultados.get("nombre_completo","")
                mercado = resultados.get("mercado","") 
                moneda = resultados.get("moneda","")
                precio_apertura = convertir_a_numero(resultados.get("precio_apertura", ""))
                precio_cierre = convertir_a_numero(resultados.get("precio_cierre", ""))
                precio_minimo = convertir_a_numero(resultados.get("precio_minimo", ""))
                precio_maximo = convertir_a_numero(resultados.get("precio_maximo", ""))
                cotizacion_moneda_local = convertir_a_numero(resultados.get("precio_actual", ""))
                volumen = convertir_a_numero(resultados.get("volumen", ""))
                variacion_diaria = convertir_a_numero(resultados.get("variacion_diaria", ""))
                fuente = resultados.get("fuente", "")
                
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
                if fuente:
                    sheet.update_cell(i, 16, fuente)
        else:
            print(f"Omitiendo {ticker} - {activo} (no es una acción)")

def obtener_tipo_cambio():
    # Aquí puedes implementar una función para obtener el tipo de cambio del dólar MEP
    return 945.2586  # Ejemplo estático; puedes actualizarlo dinámicamente

def calcular_variacion_diaria(cierre_anterior, precio_actual):
    if cierre_anterior and precio_actual:
        return round(((precio_actual - cierre_anterior) / cierre_anterior) * 100, 2)
    return 0.0

def convertir_a_numero(valor):
    try:
        return float(valor.replace(",", ""))
    except ValueError:
        return valor