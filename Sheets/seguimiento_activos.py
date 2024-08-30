from utils import get_sheet, obtener_precios_historicos_scraping
import numpy as np

def actualizar_beta_para_ticker(ticker, beta):
    # Obtener la hoja de Seguimiento de Activos
    sheet = get_sheet("Seguimiento de Activos")
    
    # Obtener todas las filas que contienen el ticker
    tickers = sheet.col_values(1)  # Suponiendo que los tickers están en la columna 1 (columna A)
    
    # Iterar sobre todas las filas para encontrar las que coincidan con el ticker
    for i, t in enumerate(tickers):
        if t == ticker:
            # Actualizar la columna de Beta en la fila correspondiente
            sheet.update_cell(i + 1, 22, beta)  # Ajusta columna_beta con el índice de la columna de beta
            print(f"Actualizada Beta para {ticker} en la fila {i + 1}")



def calcular_volatilidad_historica():
    sheet = get_sheet("Seguimiento de Activos")
    tickers = sheet.col_values(1)[7:]  # Tickers desde la fila 8

    tickers_unicos = list(set(tickers))  # Obtenemos los tickers únicos para evitar duplicados

    volatilidades = {}
    rsis = {}

    for ticker in tickers_unicos:
        print(f"Calculando volatilidad histórica para {ticker}...")
        precios = obtener_precios_historicos_scraping(ticker)
        
        if precios:
            # Calcular Volatilidad Histórica y RSI
            volatilidades[ticker] = calcular_volatilidad(precios)
            rsis[ticker] = calcular_rsi(precios)
            print(f"Volatilidad histórica de {ticker}: {volatilidades[ticker]}")
            print(f"RSI de {ticker}: {rsis[ticker]}")
        else:
            volatilidades[ticker] = None
            rsis[ticker] = None


    # Ahora, actualizamos todas las filas correspondientes con la volatilidad calculada
    for i, ticker in enumerate(tickers, start=8):
        if volatilidades[ticker] is not None:
            sheet.update_cell(i, 23, volatilidades[ticker])  # Columna de volatilidad
        if rsis[ticker] is not None:
            sheet.update_cell(i, 25, rsis[ticker])


def calcular_volatilidad(precios):
    if len(precios) < 2:
        return None
    log_retornos = np.log(np.array(precios[1:]) / np.array(precios[:-1]))
    volatilidad = np.std(log_retornos) * np.sqrt(252)  # Asumiendo 252 días hábiles en un año
    return volatilidad



def calcular_rsi(precios, periodos=14):
    """
    Calcula el RSI (Índice de Fuerza Relativa) basado en los precios de cierre.
    :param precios: Lista de precios de cierre.
    :param periodos: Número de periodos para el cálculo (por defecto 14 días).
    :return: Valor del RSI.
    """
    if len(precios) < periodos:
        return None  # No hay suficientes datos para calcular el RSI

    delta = np.diff(precios)
    ganancia = np.where(delta > 0, delta, 0)
    perdida = np.where(delta < 0, -delta, 0)

    ganancia_media = np.convolve(ganancia, np.ones((periodos,)) / periodos, mode='valid')
    perdida_media = np.convolve(perdida, np.ones((periodos,)) / periodos, mode='valid')

    rs = ganancia_media / perdida_media
    rsi = 100 - (100 / (1 + rs))

    return rsi[-1]  # Devolver el RSI más reciente


