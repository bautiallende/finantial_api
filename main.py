from Sheets.cotizaciones import actualizar_cotizaciones
from Sheets.seguimiento_activos import calcular_volatilidad_historica
# from proyeccion_inversiones import actualizar_proyeccion_inversiones
# from analisis_activos import actualizar_analisis_activos

def main():
    #print("Actualizando cotizaciones...")
    actualizar_cotizaciones()

    #print("Actualizando seguimiento de activos...")
    calcular_volatilidad_historica()

    #print("Actualizando proyección de inversiones...")
    #actualizar_proyeccion_inversiones()

    #print("Actualizando análisis de activos...")
    #actualizar_analisis_activos()

if __name__ == "__main__":
    main()
    


