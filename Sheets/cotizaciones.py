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
            fila_actualizar[13] = valor_compra  # Tipo de Cambio Compra
            fila_actualizar[14] = valor_venta  # Tipo de Cambio Venta
            fila_actualizar[19] = fuente_dolar  # Fuente del Dólar


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
                        fila_actualizar[12] = cotizacion_moneda_local
                        if valor_compra:
                            sheet.update_cell(i, 11, valor_compra * cotizacion_moneda_local)
                    elif moneda == "ARS":
                        sheet.update_cell(i, 11, cotizacion_moneda_local)
                        if valor_venta:
                            sheet.update_cell(i, 12, cotizacion_moneda_local/valor_venta)
                    if precio_cierre:
                        sheet.update_cell(i, 17, ((cotizacion_moneda_local - precio_cierre) / precio_cierre) )




                fila_actualizar[10] = convertir_a_numero(resultados.get("precio_actual", ""))
                
                
                
                fila_actualizar[14] = convertir_a_numero(resultados.get("volumen", ""))
                
                fila_actualizar[15] = resultados.get("variacion_diaria", "")
                
                fila_actualizar[17] = resultados.get("fuente", "")






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
                sheet.update_cell(i, 2, ticker)
                if nombre_completo:
                    sheet.update_cell(i, 3, nombre_completo)
                if mercado:
                    sheet.update_cell(i, 4, mercado)
                sheet.update_cell(i, 5, activo)
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
                    if moneda == "USD":
                        sheet.update_cell(i, 12, cotizacion_moneda_local)
                        if valor_compra:
                            sheet.update_cell(i, 11, valor_compra * cotizacion_moneda_local)
                    elif moneda == "ARS":
                        sheet.update_cell(i, 11, cotizacion_moneda_local)
                        if valor_venta:
                            sheet.update_cell(i, 12, cotizacion_moneda_local/valor_venta)
                    if precio_cierre:
                        sheet.update_cell(i, 17, ((cotizacion_moneda_local - precio_cierre) / precio_cierre) )
                if volumen:
                    sheet.update_cell(i, 15, volumen)
                if variacion_diaria:
                    sheet.update_cell(i, 16, variacion_diaria)
                if fuente:
                    sheet.update_cell(i, 18, fuente)
                print(f"Actualizado {ticker} - {activo}")
        elif activo.lower() == "bono":
            # Implementación para actualizar información de bonos
            print(f"Procesando {ticker} - {activo}")

            bonos = obtener_datos_bono(ticker)

            if bonos:
                fecha = obtener_fecha_actual()
                nombre_completo = bonos.get("nombre_completo","")
                mercado = bonos.get("mercado","") 
                moneda = bonos.get("moneda","")
                precio_apertura = convertir_a_numero(bonos.get("precio_apertura", ""), ".")
                precio_cierre = convertir_a_numero(bonos.get("precio_cierre", ""), ".")
                precio_minimo = convertir_a_numero(bonos.get("precio_minimo", ""), ".")
                precio_maximo = convertir_a_numero(bonos.get("precio_maximo", ""), ".")
                cotizacion_moneda_local = convertir_a_numero(bonos.get("precio_actual", ""), ".")
                print(f"cotizacion_moneda_local {cotizacion_moneda_local}")
                volumen = convertir_a_numero(bonos.get("volumen", ""), ".")
                variacion_diaria = convertir_a_numero(bonos.get("variacion_diaria", ""), ".")
                fuente = bonos.get("fuente", "")

                
                
                # Actualizar la celda solo si tenemos un valor válido
                if fecha:
                    sheet.update_cell(i, 1, fecha)
                sheet.update_cell(i, 2, ticker)
                if nombre_completo:
                    sheet.update_cell(i, 3, nombre_completo)
                if mercado:
                    sheet.update_cell(i, 4, mercado)
                sheet.update_cell(i, 5, activo)
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
                    # if moneda in ["USD", "Dólares"]:
                    #     sheet.update_cell(i, 12, cotizacion_moneda_local)
                    #     if valor_compra:
                    #         sheet.update_cell(i, 11, valor_compra * cotizacion_moneda_local)
                    # elif moneda == "ARS":
                    #     sheet.update_cell(i, 11, cotizacion_moneda_local)
                    #     if valor_venta:
                    #         sheet.update_cell(i, 12, cotizacion_moneda_local/valor_venta)
                    if precio_cierre:
                        sheet.update_cell(i, 17, ((cotizacion_moneda_local - precio_cierre) / precio_cierre))
                if volumen:
                    sheet.update_cell(i, 15, volumen)
                if variacion_diaria:
                    sheet.update_cell(i, 16, variacion_diaria)
                if fuente:
                    sheet.update_cell(i, 18, fuente)

            

        else:
            print(f"Omitiendo {ticker} - {activo} (no es una acción)")
        time.sleep(2)



def guardar_datos_historicos(datos):
    # Obtener la hoja "Históricos"
    sheet = get_sheet("Históricos")

    # Añadir los datos al final de la hoja
    last_row = len(sheet.col_values(1)) + 1  # Encuentra la última fila para agregar nuevos datos
    sheet.insert_row(datos, last_row)




def obtener_tipo_cambio():
    # Aquí puedes implementar una función para obtener el tipo de cambio del dólar MEP
    return 945.2586  # Ejemplo estático; puedes actualizarlo dinámicamente


def calcular_variacion_diaria(cierre_anterior, precio_actual):
    if cierre_anterior and precio_actual:
        return round(((precio_actual - cierre_anterior) / cierre_anterior) * 100, 2)
    return 0.0


def convertir_a_numero(valor, decimal_separator="."):
    try:
        # Eliminar caracteres no numéricos, excepto puntos y comas
        valor = valor.replace(" ", "").replace("$", "")
        if decimal_separator == ",":
            valor = valor.replace(".", "").replace(",", ".")
        else:
            valor = valor.replace(",", "")
        return float(valor)
    except ValueError:
        return valor
    

