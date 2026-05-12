import streamlit as st
import pandas as pd

# =================================================================
# CONFIGURACIÓN GLOBAL DE LA APLICACIÓN
# =================================================================
st.set_page_config(
    page_title="Calculadora Nutricional Pro",
    page_icon="⚖️",
    layout="centered"
)

# Estilos CSS para mejorar la interfaz y las alertas
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #2e86de;
        color: white;
        font-weight: bold;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# SECCIÓN 1: ENCABEZADO Y EDUCACIÓN
# =================================================================
st.title("⚖️ Calculadora Nutricional y Metabólica")
st.markdown("### Evaluación Integral: IMC, TMB y Gasto Energético")

with st.expander("ℹ️ Información sobre los cálculos y fuentes", expanded=False):
    st.write("""
        **¿Qué medimos aquí?**
        1. **IMC (Índice de Masa Corporal):** Clasifica el estado nutricional basado en la relación entre peso y talla.
        2. **TMB (Tasa Metabólica Basal):** Calorías mínimas para funciones vitales (Mifflin-St Jeor).
        3. **GET (Gasto Energético Total):** Calorías totales según tu nivel de actividad física.
        4. **Objetivos de Peso:** Cálculo del déficit o superávit calórico recomendado para cambios de peso.
        
        **Fuentes Oficiales:**
        - Clasificaciones de peso: *Organización Mundial de la Salud (OMS)*.
        - Ecuación de TMB: *Mifflin, M. D., et al. (1990)*.
        - Recomendaciones de déficit/superávit: *American College of Sports Medicine (ACSM)*.
    """)

st.divider()

# =================================================================
# SECCIÓN 2: ENTRADA DE DATOS
# =================================================================
col_a, col_b = st.columns(2)

with col_a:
    genero = st.radio("Género biológico", ["Hombre", "Mujer"], horizontal=True)
    edad = st.number_input("Edad (años)", min_value=1, max_value=110, value=30)

with col_b:
    peso = st.number_input("Peso (kg)", min_value=20.0, max_value=250.0, value=70.0, step=0.1)
    altura = st.number_input("Altura (cm)", min_value=100, max_value=230, value=170)

nivel_actividad = st.selectbox(
    "Nivel de actividad física diaria",
    [
        "Sedentario (Poco o nada)",
        "Ligero (1-3 días/semana)",
        "Moderado (3-5 días/semana)",
        "Activo (6-7 días/semana)",
        "Muy Activo (Atleta o trabajo físico pesado)"
    ]
)

objetivo = st.selectbox(
    "¿Cuál es tu objetivo principal?",
    [
        "Mantener peso",
        "Perder peso (Déficit leve - 300 kcal)",
        "Perder peso (Déficit moderado - 500 kcal)",
        "Ganar peso (Superávit leve + 300 kcal)",
        "Ganar peso (Superávit moderado + 500 kcal)"
    ]
)

# Diccionario de factores de actividad
factores = {
    "Sedentario (Poco o nada)": 1.2,
    "Ligero (1-3 días/semana)": 1.375,
    "Moderado (3-5 días/semana)": 1.55,
    "Activo (6-7 días/semana)": 1.725,
    "Muy Activo (Atleta o trabajo físico pesado)": 1.9
}

# Mapa de ajustes calóricos por objetivo
ajustes_caloricos = {
    "Mantener peso": 0,
    "Perder peso (Déficit leve - 300 kcal)": -300,
    "Perder peso (Déficit moderado - 500 kcal)": -500,
    "Ganar peso (Superávit leve + 300 kcal)": 300,
    "Ganar peso (Superávit moderado + 500 kcal)": 500
}

# =================================================================
# SECCIÓN 3: CÁLCULOS LÓGICOS
# =================================================================
if st.button("🚀 Realizar Evaluación Completa"):
    
    # 1. Cálculo de IMC
    altura_m = altura / 100
    imc = peso / (altura_m ** 2)
    
    # Clasificación IMC según la OMS
    if imc < 18.5:
        categoria_imc = "Bajo peso"
        consejo = "Se recomienda aumentar la ingesta calórica con alimentos densos en nutrientes."
    elif 18.5 <= imc < 24.9:
        categoria_imc = "Peso saludable"
        consejo = "¡Excelente! Mantén tus hábitos actuales de alimentación y ejercicio."
    elif 25.0 <= imc < 29.9:
        categoria_imc = "Sobrepeso"
        consejo = "Considera aumentar la actividad física y revisar el tamaño de las porciones."
    else:
        categoria_imc = "Obesidad"
        consejo = "Se recomienda consultar con un médico o nutricionista para un plan de salud integral."

    # 2. Cálculo de TMB (Mifflin-St Jeor)
    if genero == "Hombre":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    else:
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161
        
    # 3. Cálculo de GET y Objetivo
    get = tmb * factores[nivel_actividad]
    calorias_objetivo = get + ajustes_caloricos[objetivo]

    # --- MOSTRAR RESULTADOS ---
    st.divider()
    
    # Resultados de IMC
    st.markdown(f"#### Estado Nutricional (IMC): **{categoria_imc}**")
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("Tu IMC", f"{imc:.1f}")
    m_col2.info(f"**Sugerencia:** {consejo}")
    
    # Requerimientos Energéticos
    st.markdown("#### Plan Energético Diario")
    c_col1, c_col2, c_col3 = st.columns(3)
    c_col1.metric("TMB (Reposo)", f"{tmb:,.0f} kcal")
    c_col2.metric("GET (Mantenimiento)", f"{get:,.0f} kcal")
    c_col3.metric("Objetivo seleccionado", f"{calorias_objetivo:,.0f} kcal", 
                  delta=ajustes_caloricos[objetivo] if ajustes_caloricos[objetivo] != 0 else None)

    # Gráfico comparativo
    st.subheader("Visualización de Gasto vs. Objetivo")
    df_data = pd.DataFrame({
        "Categoría": ["Basal (TMB)", "Mantenimiento (GET)", "Tu Objetivo"],
        "Calorías": [tmb, get, calorias_objetivo]
    })
    st.bar_chart(df_data, x="Categoría", y="Calorías", color="#2e86de")

# =================================================================
# SECCIÓN 4: ADVERTENCIAS Y NOTAS FINALES
# =================================================================
st.sidebar.title("⚠️ Notas Importantes")
st.sidebar.error("""
**DESCARGO DE RESPONSABILIDAD:** Los resultados son estimaciones basadas en promedios poblacionales. 
El IMC no distingue entre masa muscular y grasa. 
""")

st.sidebar.warning(f"**Nota sobre el objetivo:** {objetivo}. Cambios extremos en la dieta deben ser supervisados por un profesional.")

st.sidebar.markdown("""
**Fuentes Utilizadas:**
- *Organización Mundial de la Salud (OMS)* para rangos de IMC.
- *Fórmula Mifflin-St Jeor (1990)* para metabolismo.
- *Guías ACSM* para ajustes de peso saludables.
""")
