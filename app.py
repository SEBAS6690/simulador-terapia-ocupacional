# app.py
import streamlit as st
from data.preguntas import BANCO_DATOS

# Inicializar estados de renderizado web
st.set_page_config(
    page_title="Simulador Terapia Ocupacional 2026",
    page_icon="🧠",
    layout="wide"
)

if 'respuestas' not in st.session_state:
    st.session_state.respuestas = {}
if 'evaluado' not in st.session_state:
    st.session_state.evaluado = False

# Encabezado
st.title("🧠 Simulador de Aptitud Técnica: Terapia Ocupacional")
st.markdown("##### *Baremo de Preguntas y Respuestas para el Concurso de Reclutamiento*")
st.markdown("---")

# Panel lateral de navegación
st.sidebar.markdown("### 📋 Navegación")
tema_elegido = st.sidebar.selectbox("Selecciona la unidad de estudio:", list(BANCO_DATOS.keys()))

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Glosario Clínico")
with st.sidebar.expander("Ver Definiciones"):
    st.markdown("**Dipléjica:** PC con afectación simétrica bilateral, mayor en miembros inferiores.")
    st.markdown("**Flapping:** Movimientos involuntarios rápidos y rítmicos de flexo-extensión de muñeca.")
    st.markdown("**Normotonicidad:** Estado de equilibrio óptimo en el tono de reposo neuromuscular.")

datos_tema = BANCO_DATOS[tema_elegido]

st.header(f"📍 {tema_elegido}")
st.write("")  # Espacio en blanco seguro

# BLOQUE I: VERDADERO O FALSO
st.markdown("#### 📝 Bloque I: Preguntas de Verdadero o Falso")
for item in datos_tema["verdadero_falso"]:
    # VALIDACIÓN DE SEGURIDAD PARA EL ÍNDICE
    v_guardado = st.session_state.respuestas.get(item["id"], None)
    if v_guardado and v_guardado in item["op"]:
        ans_index = item["op"].index(v_guardado)
    else:
        ans_index = None
        
    res = st.radio(item["p"], item["op"], index=ans_index, key=f"r_{item['id']}", disabled=st.session_state.evaluado)
    st.session_state.respuestas[item["id"]] = res
st.markdown("---")

# BLOQUE II: EMPAREJAMIENTO
st.markdown("#### 🔗 Bloque II: Preguntas de Combinación y Emparejamiento")
for item in datos_tema["emparejamiento"]:
    # VALIDACIÓN DE SEGURIDAD PARA EL ÍNDICE
    v_guardado_emp = st.session_state.respuestas.get(item["id"], None)
    if v_guardado_emp and v_guardado_emp in item["op"]:
        ans_index = item["op"].index(v_guardado_emp)
    else:
        ans_index = None
        
    res = st.selectbox(item["p"], item["op"], index=ans_index, key=f"s_{item['id']}", disabled=st.session_state.evaluado)
    st.session_state.respuestas[item["id"]] = res
st.markdown("---")

# BLOQUE III: SELECCIÓN MÚLTIPLE
st.markdown("#### 🗂️ Bloque III: Selección Múltiple")
for item in datos_tema["seleccion"]:
    # VALIDACIÓN DE SEGURIDAD PARA EL ÍNDICE
    v_guardado_sm = st.session_state.respuestas.get(item["id"], None)
    if v_guardado_sm and v_guardado_sm in item["op"]:
        ans_index = item["op"].index(v_guardado_sm)
    else:
        ans_index = None
        
    res = st.radio(item["p"], item["op"], index=ans_index, key=f"m_{item['id']}", disabled=st.session_state.evaluado)
    st.session_state.respuestas[item["id"]] = res

st.markdown("<br>", unsafe_allow_html=True)

# Botones de control
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if not st.session_state.evaluado:
        if st.button("🚀 Finalizar y Evaluar Todo el Cuestionario", use_container_width=True):
            st.session_state.evaluado = True
            st.rerun()
    else:
        if st.button("🔄 Reiniciar Todo el Simulador", use_container_width=True):
            st.session_state.respuestas = {}
            st.session_state.evaluado = False
            st.rerun()

# Resultados
if st.session_state.evaluado:
    st.markdown("---")
    st.header("📊 Reporte de Calificación y Rendimiento")
    
    total_q = 0
    correctas = 0
    desglose = []
    
    for t_name, t_content in BANCO_DATOS.items():
        for cat in ["verdadero_falso", "emparejamiento", "seleccion"]:
            for question in t_content[cat]:
                total_q += 1
                u_res = st.session_state.respuestas.get(question["id"])
                ok = u_res == question["c"]
                if ok:
                    correctas += 1
                desglose.append({
                    "eje": t_name,
                    "pregunta": question["p"],
                    "u_ans": u_res if u_res else "Sin responder",
                    "c_ans": question["c"],
                    "status": ok,
                    "info": question.get("det", "Validado según los criterios bibliográficos oficiales.")
                })
                
    porcentaje = (correctas / total_q) * 100
    nota_final = (correctas / total_q) * 20
    
    col_r1, col_r2, col_r3 = st.columns(3)
    col_r1.metric("Aciertos Totales", f"{correctas} / {total_q}")
    col_r2.metric("Efectividad", f"{porcentaje:.1f}%")
    col_r3.metric("Nota Final", f"{nota_final:.2f} / 20")
    
    if nota_final >= 14.0:
        st.success("🎉 **Criterio de Idoneidad Cumplido.**")
    else:
        st.warning("⚠️ **Revisión Requerida:** Revisa el desglose de abajo.")
        
    st.subheader("🔍 Desglose detallado por reactivo:")
    for item in desglose:
        icon = "✅" if item["status"] else "❌"
        with st.expander(f"{icon} [{item['eje']}] — {item['pregunta'][:70]}..."):
            st.write(f"**Tu selección:** `{item['u_ans']}`")
            st.write(f"**Solución correcta:** `{item['c_ans']}`")
            st.info(f"💡 **Justificación del Baremo:** {item['info']}")