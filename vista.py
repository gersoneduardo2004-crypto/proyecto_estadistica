import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide", page_title="Dashboard Estadístico", page_icon="📊")


plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['axes.titlesize'] = 22    
plt.rcParams['axes.labelsize'] = 16    
plt.rcParams['xtick.labelsize'] = 14   
plt.rcParams['ytick.labelsize'] = 14   

st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            max-width: 98% !important;
        }
        
        div[data-testid="stHorizontalBlock"] {
            width: 100% !important;
        }
        
        html, body, [class*="st-emotion-cache"] {
            font-size: 1.25rem !important;
        }
        
        h1 {
            font-size: 3.2rem !important;
            font-weight: 800 !important;
        }
        
        h3 {
            font-size: 2.2rem !important;
            margin-top: 1rem !important;
        }
        
        button[data-baseweb="tab"] div {
            font-size: 1.5rem !important;
            font-weight: bold !important;
        }
        
        .stDataFrame div table {
            font-size: 1.35rem !important;
            width: 100% !important;
        }
        
        .stExpander {
            width: 100% !important;
        }
        
        .stExpander details summary p {
            font-size: 1.5rem !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

try:
    df_est = pd.read_csv("datos_estudiantes.csv")
    n_total = len(df_est)
except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'datos_estudiantes.csv'. Verifica la ruta.")
    st.stop()

st.sidebar.image("foto.png", use_container_width=True)

st.sidebar.markdown("### Selecciona el Tipo de Variable:")

tipo_variable = st.sidebar.segmented_control(
    label="Opciones de análisis",
    options=["Variables Cualitativas", "Variables Cuantitativas"],
    default="Variables Cualitativas",
    label_visibility="collapsed" 
)

st.title("📊 Dashboard Estadístico Automatizado")

with st.expander("📋 Lista Completa de Datos Originales (Dataset)", expanded=True):
    st.dataframe(
        df_est, 
        use_container_width=True,
        hide_index=True,
        height=550                 
    )

st.markdown("---") 
st.markdown(f"### Visualizando Análisis: **{tipo_variable}**")

if tipo_variable == "Variables Cualitativas":
    
    tab_carrera, tab_genero = st.tabs(["🏫 Carreras Universitarias", "⚥ Género"])
    
    with tab_carrera:
        st.subheader("Distribución de Frecuencias: Carreras")
        
        frec_carrera = df_est["carrera"].value_counts().reset_index()
        frec_carrera.columns = ["Carrera", "fi"]
        frec_carrera["hi"] = frec_carrera["fi"] / n_total
        frec_carrera["hi%"] = frec_carrera["hi"] * 100
        
        tot_c_fi, tot_c_hi, tot_c_hip = frec_carrera["fi"].sum(), frec_carrera["hi"].sum(), frec_carrera["hi%"].sum()
        f_tot_carrera = pd.DataFrame([["Total", tot_c_fi, tot_c_hi, tot_c_hip]], columns=["Carrera", "fi", "hi", "hi%"])
        t_final_carrera = pd.concat([frec_carrera, f_tot_carrera], ignore_index=True)
        
        st.dataframe(t_final_carrera, hide_index=True, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(8, 5.5))  
            ax.bar(frec_carrera["Carrera"], frec_carrera["fi"], color='#4ea1db', edgecolor='black', width=0.4)
            ax.set_title('DISTRIBUCIÓN POR CARRERA (BARRAS)', fontweight='bold')
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots(figsize=(8, 5.5))  
            ax.pie(frec_carrera['hi'], labels=frec_carrera['Carrera'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'), textprops={'fontsize': 15})
            ax.set_title("PORCENTAJE POR CARRERA (PASTEL)", fontweight="bold")
            st.pyplot(fig)

    with tab_genero:
        st.subheader("Distribución de Frecuencias: Género")
        
        frec_genero = df_est["genero"].value_counts().reset_index()
        frec_genero.columns = ["Género", "fi"]
        frec_genero["hi"] = frec_genero["fi"] / n_total
        frec_genero["hi%"] = frec_genero["hi"] * 100
        
        tot_g_fi, tot_g_hi, tot_g_hip = frec_genero["fi"].sum(), frec_genero["hi"].sum(), frec_genero["hi%"].sum()
        f_tot_genero = pd.DataFrame([["Total", tot_g_fi, tot_g_hi, tot_g_hip]], columns=["Género", "fi", "hi", "hi%"])
        t_final_genero = pd.concat([frec_genero, f_tot_genero], ignore_index=True)
        
        st.dataframe(t_final_genero, hide_index=True, use_container_width=True)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.pie(frec_genero['hi'], labels=frec_genero['Género'], autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'], textprops={'fontsize': 15})
        ax.set_title("PORCENTAJE DE ESTUDIANTES POR GÉNERO", fontweight="bold")
        st.pyplot(fig)

else: 
    
    tab_materias, tab_promedio = st.tabs(["📚 Materias Aprobadas (Discreta)", "📈 Promedio Acumulado (Agrupada)"])
    
    with tab_materias:
        st.subheader("Distribución de Frecuencias: Materias Aprobadas")
        
        tabla_discreta = df_est['materias_aprobadas'].value_counts().sort_index().reset_index()
        tabla_discreta.columns = ['Materias_X', 'fi']
        tabla_discreta['hi'] = tabla_discreta['fi'] / n_total
        tabla_discreta['hi%'] = tabla_discreta['hi'] * 100
        tabla_discreta['Fi'] = tabla_discreta['fi'].cumsum()
        tabla_discreta['Hi'] = tabla_discreta['hi'].cumsum()
        
        tot_m_fi, tot_m_hi, tot_m_hip = tabla_discreta["fi"].sum(), tabla_discreta["hi"].sum(), tabla_discreta["hi%"].sum()
        f_tot_discreta = pd.DataFrame([["Total", tot_m_fi, tot_m_hi, tot_m_hip, "-", "-"]], columns=['Materias_X', 'fi', 'hi', 'hi%', 'Fi', 'Hi'])
        t_final_discreta = pd.concat([tabla_discreta, f_tot_discreta], ignore_index=True)
        
        st.dataframe(t_final_discreta, hide_index=True, use_container_width=True)
        
        col_grafico, col_info = st.columns(2)
        
        with col_grafico:
            fig, ax = plt.subplots(figsize=(8, 5.5))  
            ax.vlines(x=tabla_discreta['Materias_X'], ymin=0, ymax=tabla_discreta['fi'], color='navy', linewidth=3)
            ax.plot(tabla_discreta['Materias_X'], tabla_discreta['fi'], "o", color='red', markersize=8)
            ax.set_xticks(tabla_discreta['Materias_X'])
            ax.set_title('AVANCE ACADÉMICO (VARIABLES DISCRETAS)', fontweight='bold')
            ax.set_xlabel('Número de Materias Aprobadas')
            ax.set_ylabel('Frecuencia Absoluta (fi)')
            
            st.pyplot(fig)
            
        with col_info:
            st.markdown("### 📈 Resumen Estadístico")
            c1, c2 = st.columns(2)
            with c1:
                st.metric(label="Total de Estudiantes Evaluados", value=f"{n_total}")
                st.metric(label="Máximo de Materias Aprobadas", value=f"{int(df_est['materias_aprobadas'].max())}")
            with c2:
                st.metric(label="Promedio de Materias", value=f"{df_est['materias_aprobadas'].mean():.1f}")
                st.metric(label="Mínimo de Materias Aprobadas", value=f"{int(df_est['materias_aprobadas'].min())}")
    with tab_promedio:
        st.subheader("Análisis de Rendimiento: Datos Agrupados (Sturges)")
        rango_p = df_est['promedio_acumulado'].max() - df_est['promedio_acumulado'].min()
        k_p = int(np.ceil(1 + 3.322 * np.log10(n_total)))
        amplitud_p = rango_p / k_p
        
        cortes_p = np.arange(df_est["promedio_acumulado"].min(), df_est["promedio_acumulado"].max() + amplitud_p, amplitud_p)
        df_est["intervalos_promedio"] = pd.cut(
            df_est["promedio_acumulado"], 
            bins=cortes_p, 
            include_lowest=True,  
            right=False,
            precision=2          
        )
        
       
        tabla_promedio = df_est["intervalos_promedio"].value_counts().sort_index().reset_index()
        tabla_promedio.columns = ["Intervalo", "fi"]
        tabla_promedio["Xi"] = tabla_promedio["Intervalo"].apply(lambda x: float(x.mid))
        tabla_promedio["hi"] = tabla_promedio["fi"] / n_total
        tabla_promedio["hi%"] = tabla_promedio["hi"] * 100
        tabla_promedio["Fi"] = tabla_promedio["fi"].cumsum()
        tabla_promedio["Hi"] = tabla_promedio["hi"].cumsum()
        
        tabla_promedio["Intervalo"] = tabla_promedio["Intervalo"].astype(str)

        tot_p_fi = tabla_promedio["fi"].sum()
        tot_p_hi = tabla_promedio["hi"].sum()
        tot_p_hip = tabla_promedio["hi%"].sum()
        
        f_tot_promedio = pd.DataFrame([["Total", tot_p_fi, "-", tot_p_hi, tot_p_hip, "-", "-"]], 
                                      columns=["Intervalo", "fi", "Xi", "hi", "hi%", "Fi", "Hi"])
        
        t_final_agrupada = pd.concat([tabla_promedio, f_tot_promedio], ignore_index=True)
        
        st.dataframe(t_final_agrupada, hide_index=True, use_container_width=True)
        col3, col4 = st.columns(2)
        
        with col3:
            fig, ax = plt.subplots(figsize=(8, 5.5))
            ax.hist(df_est['promedio_acumulado'], bins=cortes_p, color='#11caa0', edgecolor='white', alpha=0.6, label='Histograma')
            ax.plot(tabla_promedio['Xi'], tabla_promedio['fi'], color='red', marker='D', linewidth=3, label='Polígono', markersize=8)
            ax.set_title('HISTOGRAMA Y POLÍGONO DE FRECUENCIAS', fontweight='bold')
            ax.set_xticks(cortes_p)
            st.pyplot(fig)
            
        with col4:
            fig, ax = plt.subplots(figsize=(8, 5.5))
            ax.plot(tabla_promedio['Xi'], tabla_promedio['Fi'], color='red', marker='s', linewidth=3, label='Ojiva', markersize=8)
            ax.fill_between(tabla_promedio['Xi'], tabla_promedio['Fi'], color='purple', alpha=0.3)
            ax.set_title('OJIVA (FRECUENCIA ACUMULADA Fi)', fontweight='bold')
            ax.set_xticks(cortes_p)
            st.pyplot(fig)