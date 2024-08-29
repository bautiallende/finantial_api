import gspread
from utils import get_sheet, obtener_fecha_actual, obtener_datos_yahoo, obtener_cotizacion_dolar, obtener_datos_bono
import time


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
        valor_compra, valor_venta, fuente_dolar = obtener_cotizacion_dolar()

        # Construir una lista para actualizar en bloque
        fila_actualizar = [""] * 19
        # Actualizar los valores comunes de la fila
        fila_actualizar[0] = obtener_fecha_actual()  # Fecha
        fila_actualizar[1] = ticker  # Ticker
        if valor_compra and valor_venta:    
            fila_actualizar[12] = convertir_a_numero(valor_compra)  # Tipo de Cambio Compra
            fila_actualizar[13] = convertir_a_numero(valor_venta)  # Tipo de Cambio Venta
            fila_actualizar[18] = fuente_dolar  # Fuente del Dólar


        if activo.lower() == "accion":
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
                fila_actualizar[2] = resultados.get("nombre_completo", "")
                fila_actualizar[3] = resultados.get("mercado", "")
                fila_actualizar[4] = activo
                fila_actualizar[5] = resultados.get("moneda", "")
                fila_actualizar[6] = convertir_a_numero(resultados.get("precio_apertura", ""))
                fila_actualizar[7] = convertir_a_numero(resultados.get("precio_cierre", ""))
                fila_actualizar[8] = convertir_a_numero(resultados.get("precio_minimo", ""))
                fila_actualizar[9] = convertir_a_numero(resultados.get("precio_maximo", ""))

                cotizacion_moneda_local = convertir_a_numero(resultados.get("precio_actual", ""))
                if cotizacion_moneda_local:
                    if fila_actualizar[5] == "USD":
                        fila_actualizar[11] = cotizacion_moneda_local
                        if fila_actualizar[12]:
                            fila_actualizar[10] = fila_actualizar[12] * cotizacion_moneda_local 
                    elif fila_actualizar[5] == "ARS":
                        fila_actualizar[10] = cotizacion_moneda_local 
                        if fila_actualizar[13]:
                            fila_actualizar[11] = cotizacion_moneda_local / fila_actualizar[13]
                    if fila_actualizar[7]:
                        fila_actualizar[16] = ((cotizacion_moneda_local - fila_actualizar[7]) / fila_actualizar[7])
                        
                fila_actualizar[14] = convertir_a_numero(resultados.get("volumen", ""))
                fila_actualizar[15] = resultados.get("variacion_diaria", "")
                fila_actualizar[17] = resultados.get("fuente", "")

                print(f"Actualizado {ticker} - {activo}")

                if any(fila_actualizar):  # Solo actualizar si hay datos válidos
                    sheet.update(f"A{i}:S{i}", [fila_actualizar])
                    guardar_datos_historicos(fila_actualizar)
                    print(f"Actualizado {ticker} - {activo}")
                else:
                    print(f"No se actualizaron datos para {ticker} - {activo}.")



        elif activo.lower() == "bono":
            # Implementación para actualizar información de bonos
            print(f"Procesando {ticker} - {activo}")

            resultados = obtener_datos_bono(ticker)

            if resultados:
                fila_actualizar[2] = resultados.get("nombre_completo", "")
                fila_actualizar[3] = resultados.get("mercado", "")
                fila_actualizar[4] = activo
                fila_actualizar[5] = resultados.get("moneda", "")
                fila_actualizar[6] = convertir_a_numero(resultados.get("precio_apertura", ""), ',')
                fila_actualizar[7] = convertir_a_numero(resultados.get("precio_cierre", ""), ',')
                fila_actualizar[8] = convertir_a_numero(resultados.get("precio_minimo", ""), ',')
                fila_actualizar[9] = convertir_a_numero(resultados.get("precio_maximo", ""), ',')

                cotizacion_moneda_local = convertir_a_numero(resultados.get("precio_actual", ""), ',')

                if cotizacion_moneda_local:
                    if cotizacion_moneda_local <= 150:
                        fila_actualizar[11] = cotizacion_moneda_local
                        if fila_actualizar[12]:
                            fila_actualizar[10] = fila_actualizar[12] * cotizacion_moneda_local 
                    elif cotizacion_moneda_local > 150:
                        fila_actualizar[10] = cotizacion_moneda_local 
                        if fila_actualizar[13]:
                            fila_actualizar[11] = cotizacion_moneda_local / fila_actualizar[13]
                    if fila_actualizar[7]:
                        fila_actualizar[16] = ((cotizacion_moneda_local - fila_actualizar[7]) / fila_actualizar[7])
                        
                fila_actualizar[14] = convertir_a_numero(resultados.get("volumen", ""), ',')
                fila_actualizar[15] = resultados.get("variacion_diaria", "")
                fila_actualizar[17] = resultados.get("fuente", "")

                print(f"Actualizado {ticker} - {activo}")

                if any(fila_actualizar):  # Solo actualizar si hay datos válidos
                    sheet.update(f"A{i}:S{i}", [fila_actualizar])
                    guardar_datos_historicos(fila_actualizar)
                    print(f"Actualizado {ticker} - {activo}, {fila_actualizar}")
                else:
                    print(f"No se actualizaron datos para {ticker} - {activo}.")

        else:
            print(f"Omitiendo {ticker} - {activo} (no es una acción)")
        


def guardar_datos_historicos(fila_historica):
    """Guarda los datos en la hoja de Histórico de Cotizaciones."""
    sheet_historico = get_sheet("Histórico de Cotizaciones")
    next_row = len(sheet_historico.get_all_values()) + 1  # Encuentra la siguiente fila vacía
    sheet_historico.append_row(fila_historica)  # Añade la fila histórica



def obtener_tipo_cambio():
    # Aquí puedes implementar una función para obtener el tipo de cambio del dólar MEP
    return 945.2586  # Ejemplo estático; puedes actualizarlo dinámicamente


def calcular_variacion_diaria(cierre_anterior, precio_actual):
    if cierre_anterior and precio_actual:
        return round(((precio_actual - cierre_anterior) / cierre_anterior) * 100, 2)
    return 0.0


def convertir_a_numero(valor, separador_decimal="."):
    try:
        print(f"Convirtiendo '{valor}' a número...")
        if isinstance(valor, str):
            # Reemplazar caracteres específicos en función del separador decimal esperado
            valor = valor.replace(" ", "").replace("$", "")
            if separador_decimal == ",":
                valor = valor.replace(".", "").replace(",", ".")
            else:
                valor = valor.replace(",", "")
        # Convertir a float si es posible
        return float(valor)
    except (ValueError, AttributeError, TypeError):
        # Manejar casos en que la conversión falle
        print(f"Error al convertir '{valor}' a número.")
        return valor
    

