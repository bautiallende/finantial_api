from Sheets.cotizaciones import actualizar_cotizaciones
# from seguimiento_activos import actualizar_seguimiento_activos
from Sheets.proyeccion_inversiones import obtener_datos_bono_rava
# from analisis_activos import actualizar_analisis_activos

def main():
    print("Actualizando cotizaciones...")
    actualizar_cotizaciones()

    #print("Actualizando seguimiento de activos...")
    #actualizar_seguimiento_activos()

    #print("Actualizando proyección de inversiones...")
    #obtener_datos_bono_rava("GD30")

    #print("Actualizando análisis de activos...")
    #actualizar_analisis_activos()

if __name__ == "__main__":
    main()


