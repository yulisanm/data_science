import re
import nltk
import json
import gspread 
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from collections import Counter
from wordcloud import WordCloud
from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('stopwords')
nltk.download('punkt')

@st.cache_data
def get_dataframe(auth_file, sheet_name, work_sheet):
    """
    Retrieves the data from a Google Sheets worksheet and saves it as a Pandas Dataframe.

    Returns:
        DataFrame: The data from the Google Sheets worksheet.
    """
    auth = gspread.service_account(filename=auth_file)
    sheet = auth.open(sheet_name)
    work_sheet = sheet.worksheet(work_sheet)

    dataframe = pd.DataFrame(work_sheet.get_all_records())
    
    return dataframe

@st.cache_resource
def get_questions_from_json(json_file_path):
    """
    Retrieves questions from a JSON file.

    Args:
        json_file_path (str): The path to the JSON file.

    Returns:
        tuple: A tuple containing two lists. The first list contains open-ended questions,
               and the second list contains multiple-choice questions.
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
        detalles_cuestionario = json.load(file)
    
    preguntas_abiertas = [q for q in detalles_cuestionario if q['Tipo'] == 'Abierta']
    preguntas_seleccion_multiple = [q for q in detalles_cuestionario if q['Tipo'] == 'Seleccion multiple']
    
    return preguntas_abiertas, preguntas_seleccion_multiple

def preprocess_text(texto):
    """
    Preprocesses the given text by removing special characters, converting to lowercase, and removing accents.

    Args:
        texto (str): The text to be preprocessed.

    Returns:
        str: The preprocessed text.
    """
    # Eliminar caracteres especiales y convertir a minúsculas
    texto = re.sub(r'\W+', ' ', texto).lower()
    # Eliminar tildes
    texto = unidecode(texto)
    return texto

def graficas_wordcloud(dataframe, question):
    """
    Create a word cloud based on the responses to a specific question in a dataframe.

    Parameters:
    - dataframe (pandas.DataFrame): The dataframe containing the survey responses.
    - question (str): The question for which the word cloud is to be created.

    Returns:
    None
    """
    # Concatenate all the responses into a single string
    text = ' '.join(dataframe[question].dropna())
    text = preprocess_text(text)

    # Define Spanish stop words
    stop_words = set(stopwords.words('spanish'))

    # Create the word cloud excluding stop words
    wordcloud = WordCloud(width=800, height=400, background_color ='white', colormap= 'viridis', stopwords=stop_words).generate(text)
    
    # Display the word cloud
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    
    return plt
 
@st.cache_data
def conteos_seleccion_multiple(preguntas_seleccion_multiple, respuestas_cuestionario):
    """
    Calculates the frequencies of the selected answers in a multiple-choice questionnaire.

    Args:
        preguntas_seleccion_multiple (list): A list of dictionaries containing information about the multiple-choice questions.
            Each dictionary should have the following keys:
                - 'Pregunta': The text of the question.
                - 'Opciones': A list of the possible answer options.
                - 'Respuesta correcta': The correct answer for the question.
        respuestas_cuestionario (dict): A dictionary containing the answers given by the questionnaire participants.
            The keys of the dictionary should be the texts of the questions and the values should be lists of the selected answers.

    Returns:
        pandas.DataFrame: A DataFrame containing the results of the frequencies of the selected answers.
            The DataFrame has the following columns:
                - 'Pregunta': The text of the question.
                - 'Opción': The answer option.
                - 'Frecuencia': The frequency of the selected answer option.
                - 'Respuesta Correcta': A boolean value indicating whether the answer option is the correct answer.

    """
    
    # Create an empty DataFrame to store the results
    resultados_seleccion_multiple = pd.DataFrame(columns=['Pregunta', 'Opción', 'Frecuencia'])
    
    # Count the frequencies of the answers
    for pregunta in preguntas_seleccion_multiple:
        pregunta_texto = pregunta['Pregunta']
        opciones = pregunta['Opciones']
        respuesta_correcta = pregunta['Respuesta correcta']
        
        if pregunta_texto in respuestas_cuestionario:
            frecuencias = pd.Series(respuestas_cuestionario[pregunta_texto]).value_counts().reindex(opciones, fill_value=0)
            for opcion, frecuencia in frecuencias.items():
                new_row = pd.DataFrame({'Pregunta': [pregunta_texto], 'Opción': [opcion], 'Frecuencia': [frecuencia], 'Respuesta Correcta': [opcion == respuesta_correcta]})
                resultados_seleccion_multiple = pd.concat([resultados_seleccion_multiple, new_row], ignore_index=True)
                
    return resultados_seleccion_multiple

@st.cache_data
def graficas_piechart(dataframe):
    """
    Generate a pie chart based on the given dataframe.

    Args:
        dataframe (pandas.DataFrame): The dataframe containing the data for the pie chart.
            It should have two columns: 'Opción' and 'Frecuencia'.

    Returns:
        plotly.graph_objects.Figure: The generated pie chart figure.
    """
    labels = dataframe['Opción']
    values = dataframe['Frecuencia']

    def split_text(label):
        words = label.split()
        half = len(words) // 2
        return '\n'.join([' '.join(words[:half]), ' '.join(words[half:])])

    split_labels = [split_text(label) if len(label) > 140 else label for label in labels]

    fig = go.Figure(data=[go.Pie(
        labels=split_labels, 
        values=values, 
        textinfo='percent', 
        textfont=dict(size=11),
        marker_colors=px.colors.qualitative.Bold[:4]
    )])

    fig.update_layout(
        width=800,
        height=450,
        legend=dict(
            x=0,
            y=-0.4,
            traceorder='normal',
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(0,0,0,0)'
        ),
        margin=dict(t=50, b=50)
    )

    return fig

@st.cache_data
def graficas_agrupaciones(agrupacion):
    """
    Generate a pie chart showing the percentage of correct and incorrect answers for a given question group.

    Parameters:
    - agrupacion (DataFrame): The DataFrame containing the question group data.

    Returns:
    - fig (Figure): The generated pie chart figure.
    """
    # Calcular el porcentaje de respuestas correctas para cada pregunta
    respuestas_correctas = agrupacion[agrupacion['Respuesta Correcta'] == True]['Frecuencia'].sum()
    total_respuestas = agrupacion['Frecuencia'].sum()
    porcentaje_correctas = (respuestas_correctas / total_respuestas) * 100

    # Crear el gráfico de pastel
    labels = ['Correctas', 'Incorrectas']
    values = [respuestas_correctas, total_respuestas - respuestas_correctas]

    fig = go.Figure(data=[go.Pie(labels=labels, 
                                values=values, 
                                hole=.3, 
                                marker=dict(colors=['#90EE90', '#FF7F7F']))])
    fig.update_layout(
            width=800,
            height=400,
            legend=dict(
                x=0,
                y=0,
                traceorder='normal',
                bgcolor='rgba(0,0,0,0)',
                bordercolor='rgba(0,0,0,0)'
            ),
            margin=dict(t=50, b=50)
        )
    
    return fig, porcentaje_correctas

@st.cache_data
def calcular_frecuencia_palabras(dataframe, question):
    """
    Calculate the frequency of words in a given column of a dataframe.

    Args:
        dataframe (pandas.DataFrame): The dataframe containing the responses.
        question (str): The name of the column containing the responses.

    Returns:
        dict: A dictionary where the keys are words and the values are their frequencies.
    """
    # Concatenate all the responses into a single string
    text = ' '.join(dataframe[question].dropna())
    text = preprocess_text(text)
    # Tokenize the text
    palabras = word_tokenize(text)

    # Count the frequency of each word
    frecuencia_palabras = Counter(palabras)
    
    # Filter out stopwords
    stop_words = set(stopwords.words('spanish'))
    frecuencia_palabras = {word: count for word, count in frecuencia_palabras.items() if word not in stop_words}

    # Sort the dictionary by value in descending order
    frecuencia_palabras = dict(sorted(frecuencia_palabras.items(), key=lambda item: item[1], reverse=True))

    return frecuencia_palabras

@st.cache_data
def histograma_frecuencia_palabras(dataframe, question):
    """
    Generate a histogram plot using Plotly to visualize the frequency of words in a given question.

    Parameters:
    dataframe (pandas.DataFrame): The input dataframe containing the data.
    question (str): The question for which the word frequencies need to be calculated.

    Returns:
    None
    """
    # Calculate word frequencies
    frecuencia_palabras = calcular_frecuencia_palabras(dataframe, question)

    # Create a DataFrame from the dictionary
    df = pd.DataFrame.from_dict(frecuencia_palabras, orient='index', columns=['Frecuencia'])

    # Take only the first 10 rows
    df = df.head(8)
    
    fig = px.bar(df, 
                 x=df.index, 
                 y=df['Frecuencia'],
                 color_discrete_sequence=['#80BA5A'] 
                )

    fig.update_layout(   
            xaxis_title='Palabras comunes en las respuestas',
            yaxis_title='Frecuencia',
            xaxis={'title': {'standoff': 25}},
            width=800,
            height=400
        )
    
    return fig