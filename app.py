import streamlit as st
import pandas as pd

# =================================================================
# CONFIGURACIÓN GLOBAL DE LA APLICACIÓN
# =================================================================
# Definimos el título de la pestaña del navegador y el icono.
st.set_page_config(
    page_title="Calculadora de Tasa Metabólica Basal",
    page_icon="🔥",
    layout="centered"
)

# Inyectamos CSS personalizado para mejorar el aspecto visual (colores, bordes y botones)
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #3498db;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2980b9;
        border-color: #2980b9;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# SECCIÓN 1: ENCABEZADO Y TEXTOS EDUCATIVOS
# =================================================================
st.title("🔥 Calculadora Avanzada de TMB")
st.subheader("Entiende tu Gasto Energético")

# Usamos un "expander" para mostrar la explicación sin saturar la pantalla inicial
with st.expander("¿Cómo funciona esta calculadora?", expanded=True):
    st.write("""
        La **Tasa Metabólica Basal (TMB)** representa las calorías que quemas simplemente por existir (mantener órganos vivos). 
        
        **Lógica del cálculo:**
        1. **Fórmula de Mifflin-St Jeor:** Es el estándar actual de la industria para estimar el metabolismo en reposo.
        2. **Factor de Actividad:** Multiplicamos la TMB por un coeficiente según tu estilo de vida para obtener el **GET (Gasto Energético Total)**.
    """)

st.divider() # Línea divisoria visual

# =================================================================
# SECCIÓN 2: ENTRADA DE DATOS DEL USUARIO
# =================================================================
# Dividimos la entrada en dos columnas para que sea más simétrico
col1, col2 = st.columns(2)

with col1:
    genero = st.radio("Selecciona tu Género", ["Hombre", "Mujer"], horizontal=True)
    edad = st.number_input("Edad (años)", min_value=1, max_value=120, value=25)

with col2:
    peso = st.number_input("Peso actual (kg)", min_value=10.0, max_value=300.0, value=70.0, step=0.1)
    altura = st.number_input("Altura (cm)", min_value=50, max_value=250, value=170)

# Selector para el nivel de actividad física diaria
nivel_actividad = st.selectbox(
    "¿Cuál es tu nivel de actividad física?",
    [
        "Sedentario (Poco o ningún ejercicio)",
        "Ligero (Ejercicio ligero 1-3 días/semana)",
        "Moderado (Ejercicio moderado 3-5 días/semana)",
        "Activo (Ejercicio fuerte 6-7 días/semana)",
        "Muy Activo (Ejercicio muy fuerte o trabajo físico)"
    ]
)

# Diccionario que asocia cada opción con su coeficiente multiplicador científico
mapa_actividad = {
    "Sedentario (Poco o ningún ejercicio)": 1.2,
    "Ligero (Ejercicio ligero 1-3 días/semana)": 1.375,
    "Moderado (Ejercicio moderado 3-5 días/semana)": 1.55,
    "Activo (Ejercicio fuerte 6-7 días/semana)": 1.725,
    "Muy Activo (Ejercicio muy fuerte o trabajo físico)": 1.9
}

# =================================================================
# SECCIÓN 3: LÓGICA DE PROCESAMIENTO Y RESULTADOS
# =================================================================
if st.button("🚀 Calcular mis Requerimientos"):
    
    # --- Implementación de la Fórmula de Mifflin-St Jeor ---
    # La diferencia entre géneros radica en el ajuste final (+5 vs -161)
    if genero == "Hombre":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    else:
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161
    
    # Obtenemos el factor basado en la selección del usuario
    factor = mapa_actividad[nivel_actividad]
    get = tmb * factor # Gasto Energético Total

    st.divider()
    
    # Mostramos los resultados usando componentes de métricas (estilo Dashboard)
    res_col1, res_col2 = st.columns(2)
    
    with res_col1:
        st.metric(label="TMB (Metabolismo en Reposo)", value=f"{tmb:,.0f} kcal")
        st.info("Estas son las calorías que quemas sin moverte en todo el día.")
        
    with res_col2:
        st.metric(label="GET (Gasto Total Diario)", value=f"{get:,.0f} kcal")
        st.success("Calorías estimadas para mantener tu peso actual con tu actividad.")

    # --- Generación de Gráfico Comparativo ---
    st.subheader("Comparativa Visual de Energía")
    # Creamos un pequeño DataFrame para alimentar el gráfico de Streamlit
    datos_grafico = pd.DataFrame({
        "Categoría": ["Reposo (TMB)", "Total con Actividad (GET)"],
        "Calorías": [tmb, get]
    })
    
    # st.bar_chart es una forma rápida y elegante de visualizar estos datos
    st.bar_chart(data=datos_grafico, x="Categoría", y="Calorías", color="#3498db")

# =================================================================
# SECCIÓN 4: INFORMACIÓN LEGAL Y DE SALUD (BARRA LATERAL)
# =================================================================
st.sidebar.header("Información Importante")

st.sidebar.warning("""
**⚠️ ADVERTENCIA MÉDICA:** Este software es una herramienta informativa basada en fórmulas estadísticas. 
No constituye un diagnóstico médico. Los resultados pueden variar según la masa muscular, genética y estado de salud.
""")

st.sidebar.info("""
**Recomendación:**
Para planes de pérdida o ganancia de peso, consulta siempre con un nutricionista o profesional de la salud certificado.
""")