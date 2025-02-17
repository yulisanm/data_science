import streamlit as st
import pandas as pd
import plotly.express as px

# Import your functions
from utils import get_dataframe, get_questions_from_json, conteos_seleccion_multiple, graficas_agrupaciones

# Set Streamlit page configuration
st.set_page_config(page_title='Estrategia GitHub Copilot', layout="wide")

# Display title
st.markdown("<h2 style='text-align: left; color: white;'>Estrategia GitHub Copilot by Equinox AI Lab</h2>", unsafe_allow_html=True)

# Display introduction
st.write('Presentamos un resumen de los resultados de las capacitaciones de GitHub Copilot:')

# Define file paths and sheet names
auth_file = 'auth_file_cuestionario.json'
sheet_name_respuestas = 'copilot_cuestionario_evaluacion'
work_sheet_respuestas = 'Sheet1'
sheet_name_control = 'copilot_control_capacitaciones'
work_sheet_control = 'Sheet1'

# Load data from JSON file and Google Sheets
respuestas_cuestionario = get_dataframe(auth_file, sheet_name_respuestas, work_sheet_respuestas)
control_capacitaciones = get_dataframe(auth_file, sheet_name_control, work_sheet_control)

# Button to reload data
if st.button('Cargar Respuestas'):
    st.cache_data.clear()
    respuestas_cuestionario = get_dataframe(auth_file, sheet_name_respuestas, work_sheet_respuestas)
    control_capacitaciones = get_dataframe(auth_file, sheet_name_control, work_sheet_control)

# Calculate metrics
total_capacitados = control_capacitaciones[control_capacitaciones['Asistió'] == 'Sí'].shape[0]
total_respuestas = respuestas_cuestionario.shape[0]
conteo_cargos = respuestas_cuestionario['Cargo'].value_counts()
num_cargos = respuestas_cuestionario['Cargo'].nunique()
conteo_proyectos = respuestas_cuestionario['Nombre del proyecto'].value_counts()
num_proyectos = respuestas_cuestionario['Nombre del proyecto'].nunique()

# Display metrics using Streamlit columns and metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Colaboradores Capacitados", total_capacitados)
col2.metric("Proyectos Capacitados", num_proyectos)
col3.metric("Cargos Capacitados", num_cargos)
col4.metric("Respuestas al Cuestionario", total_respuestas-17)

# Create tabs for visualizations
tab1, tab2, tab3 = st.tabs(["Proyecto", "Cargo", "Fecha"])

# Visualization by date
with tab3:
    asistio_df = control_capacitaciones[control_capacitaciones['Asistió'] == 'Sí'].copy()
    asistio_df['Fecha Capacitación'] = pd.to_datetime(asistio_df['Fecha Capacitación'], format='%d/%m/%Y') 
    asistio_df['Month'] = asistio_df['Fecha Capacitación'].dt.strftime('%B')
    month_translation = {'Enero': 'January', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril', 'May': 'Mayo', 'June': 'Junio'}
    asistio_df['Month'] = asistio_df['Month'].map(month_translation)
    month_order = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
    asistio_df['Month'] = pd.Categorical(asistio_df['Month'], categories=month_order, ordered=True)
    capacitados_por_mes = asistio_df.groupby('Month').size().reset_index(name='Count')
    fig_fechas = px.bar(capacitados_por_mes,
                        x='Month', 
                        y='Count', 
                        labels={'Month': 'Mes', 'Count': 'Número de Colaboradores Capacitados'},
                        color_discrete_sequence=['#E73F74'] )
    
    fig_fechas.update_layout(   
        xaxis_title='Mes',
        yaxis_title='Número de Colaboradores Capacitados',
        width=800,
        height=450
    )
    
    st.plotly_chart(fig_fechas)

# Visualization by job position
with tab2:
    fig_cargos = px.bar(conteo_cargos, 
                        x=conteo_cargos.values, 
                        y=conteo_cargos.index, 
                        labels={'x': 'Número de Colaboradores Capacitados', 'y': 'Cargo'},
                        color_discrete_sequence=['#008695'] 
                        )

    fig_cargos.update_layout(   
        xaxis_title='Número de Colaboradores Capacitados',
        yaxis_title='Cargo',
        yaxis={'categoryorder':'total descending', 'automargin': True, 'title': {'standoff': 25}},
        width=800,
        height=450
    )

    st.plotly_chart(fig_cargos)
    
# Visualization by project
with tab1:
    fig_proyectos = px.bar(conteo_proyectos, 
                        x=conteo_proyectos.values, 
                        y=conteo_proyectos.index, 
                        labels={'x': 'Número de Colaboradores Capacitados', 'y': 'Nombre del proyecto'},  
                        color_discrete_sequence=['#7F3C8D'] 
                        )

    fig_proyectos.update_layout(   
        xaxis_title='Número de Colaboradores Capacitados',
        yaxis_title='Nombre del proyecto',
        yaxis={'categoryorder':'total descending', 'automargin': True, 'title': {'standoff': 25}},
        width=800,
        height=450
    )

    st.plotly_chart(fig_proyectos)