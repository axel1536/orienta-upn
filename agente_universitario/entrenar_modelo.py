"""Entrenamiento reproducible del clasificador de intenciones."""
from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.pipeline import Pipeline

CARPETA = Path(__file__).resolve().parent
DATOS = CARPETA / "datos"
MODELOS = CARPETA / "modelos"
RESULTADOS = CARPETA / "resultados"
SEMILLA = 42


def crear_modelo(c):
    return Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            analyzer="char_wb",
            ngram_range=(3, 5),
            sublinear_tf=True,
            min_df=2,
        )),
        ("clasificador", LogisticRegression(
            max_iter=4000,
            C=c,
            random_state=SEMILLA,
        )),
    ])


def calibrar_umbral(modelo, consultas, etiquetas):
    probabilidades = modelo.predict_proba(consultas)
    orden = probabilidades.argsort(axis=1)
    confianza = probabilidades.max(axis=1)
    margen = (probabilidades[range(len(probabilidades)), orden[:, -1]]
              - probabilidades[range(len(probabilidades)), orden[:, -2]])
    predichas = modelo.predict(consultas).astype(str)
    reales = etiquetas.astype(str).to_numpy()

    candidatos = []
    for minimo_confianza in [0.12, 0.15, 0.18, 0.20, 0.22, 0.25, 0.30]:
        for minimo_margen in [0.02, 0.03, 0.05, 0.08, 0.10]:
            aceptada = ((confianza >= minimo_confianza)
                        & (margen >= minimo_margen))
            cobertura = float(aceptada.mean())
            precision = (float((predichas[aceptada] == reales[aceptada]).mean())
                         if aceptada.any() else 0.0)
            candidatos.append((
                precision, cobertura, -minimo_confianza, -minimo_margen,
                minimo_confianza, minimo_margen,
            ))
    elegibles = [fila for fila in candidatos
                 if fila[0] >= 0.98 and fila[1] >= 0.70]
    mejor = max(elegibles or candidatos)
    return mejor[-2], mejor[-1], mejor[0], mejor[1]


def main():
    entrenamiento = pd.read_csv(DATOS / "entrenamiento.csv")
    validacion = pd.read_csv(DATOS / "validacion.csv")
    prueba = pd.read_csv(DATOS / "prueba.csv")

    columnas = {"consulta", "intencion"}
    for nombre, datos in [
        ("entrenamiento", entrenamiento),
        ("validacion", validacion),
        ("prueba", prueba),
    ]:
        if not columnas.issubset(datos.columns):
            raise ValueError(f"Faltan columnas en {nombre}.csv")
        if datos[list(columnas)].isna().any().any():
            raise ValueError(f"Hay valores vacíos en {nombre}.csv")

    resultados = []
    mejor = None
    for c in [1.0, 2.0, 4.0, 8.0]:
        modelo = crear_modelo(c)
        modelo.fit(entrenamiento["consulta"], entrenamiento["intencion"])
        prediccion = modelo.predict(validacion["consulta"])
        fila = {
            "modelo": f"Regresión logística char TF-IDF C={c}",
            "accuracy_validacion": accuracy_score(
                validacion["intencion"], prediccion),
            "f1_macro_validacion": f1_score(
                validacion["intencion"], prediccion, average="macro"),
        }
        resultados.append(fila)
        clave = (fila["f1_macro_validacion"], fila["accuracy_validacion"])
        if mejor is None or clave > mejor[0]:
            mejor = (clave, c, modelo)

    baseline = Pipeline([
        ("tfidf", TfidfVectorizer(
            strip_accents="unicode", analyzer="char_wb", ngram_range=(3, 5))),
        ("clasificador", DummyClassifier(strategy="most_frequent")),
    ])
    baseline.fit(entrenamiento["consulta"], entrenamiento["intencion"])
    prediccion_baseline = baseline.predict(validacion["consulta"])
    resultados.append({
        "modelo": "Baseline clase más frecuente",
        "accuracy_validacion": accuracy_score(
            validacion["intencion"], prediccion_baseline),
        "f1_macro_validacion": f1_score(
            validacion["intencion"], prediccion_baseline,
            average="macro", zero_division=0),
    })

    _, mejor_c, modelo_validacion = mejor
    umbral_confianza, umbral_margen, precision_aceptada, cobertura = (
        calibrar_umbral(
            modelo_validacion,
            validacion["consulta"],
            validacion["intencion"],
        )
    )

    datos_finales = pd.concat(
        [entrenamiento, validacion], ignore_index=True)
    modelo_final = crear_modelo(mejor_c)
    modelo_final.fit(datos_finales["consulta"], datos_finales["intencion"])
    prediccion_prueba = modelo_final.predict(prueba["consulta"])
    accuracy_prueba = accuracy_score(
        prueba["intencion"], prediccion_prueba)
    f1_prueba = f1_score(
        prueba["intencion"], prediccion_prueba, average="macro")

    RESULTADOS.mkdir(exist_ok=True)
    MODELOS.mkdir(exist_ok=True)
    pd.DataFrame(resultados).to_csv(
        RESULTADOS / "seleccion_modelo_20_intenciones.csv",
        index=False, encoding="utf-8-sig")
    pd.DataFrame(classification_report(
        prueba["intencion"], prediccion_prueba,
        output_dict=True, zero_division=0,
    )).transpose().to_csv(
        RESULTADOS / "reporte_20_intenciones.csv",
        encoding="utf-8-sig")
    pd.DataFrame({
        "consulta": prueba["consulta"].to_numpy(),
        "intencion_real": prueba["intencion"].to_numpy(),
        "intencion_predicha": prediccion_prueba,
        "acierto": prueba["intencion"].to_numpy() == prediccion_prueba,
    }).to_csv(
        RESULTADOS / "predicciones_20_intenciones.csv",
        index=False, encoding="utf-8-sig")

    joblib.dump(modelo_final, MODELOS / "clasificador.joblib")
    configuracion = {
        "version": "20_intenciones",
        "cantidad_intenciones": int(
            datos_finales["intencion"].nunique()),
        "consultas_totales": int(
            len(datos_finales) + len(prueba)),
        "entrenamiento_final": int(len(datos_finales)),
        "prueba": int(len(prueba)),
        "C": mejor_c,
        "umbral_confianza": umbral_confianza,
        "umbral_margen": umbral_margen,
        "precision_aceptada_validacion": precision_aceptada,
        "cobertura_validacion": cobertura,
        "accuracy_test": accuracy_prueba,
        "f1_macro_test": f1_prueba,
        "random_state": SEMILLA,
    }
    (MODELOS / "configuracion.json").write_text(
        json.dumps(configuracion, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(configuracion, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

