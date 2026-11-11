"""Lectura de resultados existentes. No entrena modelos ni altera los datos."""
from pathlib import Path
import pandas as pd


def cargar_evaluacion(carpeta):
    carpeta = Path(carpeta) / "resultados"
    comparacion = pd.read_csv(carpeta / "comparacion_modelos.csv", encoding="utf-8-sig")
    predicciones = pd.read_csv(carpeta / "predicciones_prueba.csv", encoding="utf-8-sig")
    requeridas = {"Modelo", "Accuracy", "Precision_macro", "Recall_macro", "F1_macro"}
    if not requeridas.issubset(comparacion.columns):
        raise ValueError("La comparación no contiene todas las métricas esperadas.")
    if not {"consulta", "intencion_real", "intencion_predicha"}.issubset(predicciones.columns):
        raise ValueError("Faltan columnas en las predicciones de prueba.")
    aciertos = predicciones["intencion_real"] == predicciones["intencion_predicha"]
    return {
        "comparacion": comparacion,
        "total": len(predicciones),
        "aciertos": int(aciertos.sum()),
        "errores": predicciones.loc[~aciertos, ["consulta", "intencion_real", "intencion_predicha"]],
        "matriz": carpeta / "matriz_confusion.png",
    }
