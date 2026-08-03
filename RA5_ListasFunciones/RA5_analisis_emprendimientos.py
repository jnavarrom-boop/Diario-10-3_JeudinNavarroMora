"""Practica Semana 07: analisis de emprendimientos costarricenses.

Complete los espacios marcados con TODO. El objetivo es generar un reporte por
sede usando listas, diccionarios, funciones, ciclos y condicionales.
"""

from sedes import sedes

def calcular_total(ventas):
    """recibe una lista y retona el total de ventas."""
    return sum(ventas)

def calcular_porcentaje_logro(total, meta):
    """calcula el porcentaje de cumplimiento de un meta"""
    porcentaje = total / meta * 100
    return porcentaje 

def calcular_clasificacion(porcentaje):
    if porcentaje >= 100:
        mensaje = "meta alcanzada, felicitaciones..!"
    elif porcentaje >= 90:
        mensaje = "ADVERTENCIA: meta no lograda."
    else:
        mensaje = "URGENTE: meta no alcanzada, revisar perdidas "
    return mensaje 

def imprimir_reporte(datos_reporte):
    """imprime el reporte final de ventas por emprendimiento"""
    
    #encabezado
    print("\nREPORTE FINAL")
    print("-" * 60)
    
    for fila in datos_reporte:
        print(f"provincia: {fila["nombre"]}")
        print(f"provincia: {fila["provincia"]}")
        print(f"tipo: {fila["tipo"]}")
        
        print(f"total ventas semanal:  ₡{fila["total"]:,.2f}")
        print(f"cumpliendo de meta: {fila["porcentaje"]:.2f}%")
        print(f"promedio diario: ₡{fila["total"]/5:,.2f}")
        print(fila["clasificacion"])
        
        print("-" * 60)

reporte = []
for emprendimiento in sedes:
    ventas = emprendimiento ["ventas"]
    meta = emprendimiento["meta"]
    nombre = emprendimiento["nombre"]
    total_ventas = calcular_total(ventas)
    porcentaje_emprendimiento = calcular_porcentaje_logro(total_ventas, meta)
    clasificacion = calcular_clasificacion(porcentaje_emprendimiento)
    
    reporte.append(
        {
            "nombre" : emprendimiento["nombre"],
            "provincia" : emprendimiento["provincia"],
            "tipo": emprendimiento["tipo"],
            "total": total_ventas,
            "porcentaje": porcentaje_emprendimiento,
            "clasificacion": clasificacion 
        }
    )

imprimir_reporte(reporte)