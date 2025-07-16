# from django.shortcuts import render
# import plotly.express as px


# # Create your views here.
# #se crea funcion para renderizar  primero request, luego la pagina y el contexto
# def main_dashboard(request):
#     context = {}
#     df = px.data.gapminder().query("continent=='Oceania'")
#     fig = px.line(df, x="year", y="lifeExp", color='country')
#     plot_1 = fig.to_html()
#     print(plot_1)
#     context['plot_1'] = plot_1
#     return render(request, 'content.html', context=context)
#MODIFICADO 1
# from django.shortcuts import render
# import plotly.express as px
# import requests
# from collections import Counter
# from django.conf import settings

# def get_airtable_data():
#     """Obtiene datos de Airtable."""
#     endpoint = f'https://api.airtable.com/v0/{settings.AIRTABLE_BASE_ID}/{settings.AIRTABLE_TABLE_NAME}'
#     headers = {
#         "Authorization": f"Bearer {settings.AIRTABLE_TOKEN}"
#     }
#     response = requests.get(endpoint, headers=headers)
#     if response.status_code == 200:
#         records = response.json().get("records", [])
#         return [{
#             "id": rec["fields"].get("id", "N/A"),
#             "TIPO DOC.": rec["fields"].get("TIPO DOC.", "N/A"),
#             "N° DOCUMENTO": rec["fields"].get("N° DOCUMENTO", "N/A"),
#             "REMITENTE": rec["fields"].get("REMITENTE", "N/A"),
#             "F. EMISION": rec["fields"].get("F. EMISION", "N/A"),
#             "DESTINATARIO": rec["fields"].get("DESTINATARIO", "N/A"),
#             "F. RECEPCION": rec["fields"].get("F. RECEPCION", "N/A"),
#             "ESTADO": rec["fields"].get("ESTADO", "N/A"),
#             "TIEMPO DE ATENCION": rec["fields"].get("TIEMPO DE ATENCION", "N/A"),
#             "SEMAFORO": rec["fields"].get("SEMAFORO", "N/A"),
#             "ASUNTO": rec["fields"].get("ASUNTO", "N/A")
#         } for rec in records]
#     else:
#         return []

# def main_dashboard(request):
#     # Obtener datos de Airtable
#     data = get_airtable_data()

#     # Contar la cantidad de estados (o cualquier campo que desees contar)
#     estado_counts = Counter([entry["id"] for entry in data])
    
#     docu_counts = Counter([entry["N° DOCUMENTO"] for entry in data])

#     # Crear un gráfico con Plotly (basado en los datos de Airtable)
#     df = px.data.gapminder().query("continent=='Oceania'")  # Utiliza cualquier dataframe que necesites
#     fig = px.line(df, x="year", y="lifeExp", color='country')
#     plot_1 = fig.to_html()

#     # Pasar el gráfico y los datos a la plantilla
#     context = {
#         'plot_1': plot_1,
#         'data': data,
#         'estado_counts': estado_counts,
#         'docu_counts': docu_counts,
#     }

#     # Renderizar la página con los datos y el gráfico
#     return render(request, 'content.html', context)
#MODIFICADO 2
# views.py
# views.py
import requests
from django.shortcuts import render
import plotly.express as px
from collections import Counter
from django.conf import settings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime


#DATOS DEL API
def get_airtable_data():
    
    endpoint = f'https://api.airtable.com/v0/{settings.AIRTABLE_BASE_ID}/{settings.AIRTABLE_TABLE_NAME}'
    headers = {
        "Authorization": f"Bearer {settings.AIRTABLE_TOKEN}"
    }
    records = []
    offset = None

    # Hacer solicitudes en paginación para obtener todos los registros
    while True:
        params = {}
        if offset:
            params['offset'] = offset  # Usar el parámetro offset para obtener la siguiente página de datos
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            records.extend(data.get("records", []))  # Añadir los registros obtenidos
            offset = data.get('offset')  # Obtener el siguiente offset para la siguiente página
            if not offset:
                break  # Si no hay más datos (sin offset), salimos del bucle
        else:
            # Si la respuesta no es exitosa, puedes manejar el error aquí
            print(f"Error al obtener datos de Airtable: {response.status_code}")
            break

    return [{
        "id": rec["fields"].get("id", "N/A"),
        "TIPO_DOC": rec["fields"].get("TIPO_DOC", "").strip().upper(),
        "N_DOCUMENTO": rec["fields"].get("N_DOCUMENTO", "N/A"),
        "REMITENTE": rec["fields"].get("REMITENTE", "N/A"),
        "F_EMISION": rec["fields"].get("F_EMISION", "N/A"),
        "DESTINATARIO": rec["fields"].get("DESTINATARIO", "N/A").strip().upper(),
        "F_RECEPCION": rec["fields"].get("F_RECEPCION", "N/A"),
        "ESTADO": rec["fields"].get("ESTADO", "N/A"),
        "TIEMPO_DE_ATENCION": rec["fields"].get("TIEMPO_DE_ATENCION", "N/A"),
        "SEMAFORO": rec["fields"].get("SEMAFORO", "N/A"),
        "ASUNTO": rec["fields"].get("ASUNTO", "N/A")
    } for rec in records]

    

#GRAFICOS

def calculate_semaforo_counts(data):
  
    semaforo_counts = {'Verde': 0, 'Amarillo': 0, 'Rojo': 0, 'Negro': 0}

    for entry in data:
        tiempo_atencion = entry.get('TIEMPO_DE_ATENCION', 'N/A')
        semaforo = entry.get('SEMAFORO', 'N/A')

        if tiempo_atencion == 'N/A' or semaforo == 'N/A':
            continue

        # Verificar si el tiempo de atención no es un guion '-'
        if tiempo_atencion == '-':
            continue
        
        # Verificar si el tiempo de atención es un número válido
        try:
            tiempo_atencion_int = int(tiempo_atencion)
        except ValueError:
            # Si no es un número entero, continuar con la siguiente entrada
            continue

        # Condicionales para asignar el color al semáforo según el tiempo de atención
        if tiempo_atencion_int <= 1:
            semaforo_counts['Verde'] += 1
        elif tiempo_atencion_int == 2:
            semaforo_counts['Amarillo'] += 1
        elif 3 <= tiempo_atencion_int <= 4:
            semaforo_counts['Rojo'] += 1
        elif tiempo_atencion_int >= 5:
            semaforo_counts['Negro'] += 1

    return semaforo_counts




def contar_documentos_por_tipo(data):
   

    # Inicializar el diccionario con los tipos de documentos en 0
    tipos_documentos = {
        "CARTA": 0,
        "HOJA DE ENVIO": 0,
        "INFORME": 0,
        "MEMORANDO MULTIPLE": 0,
        "OFICIO": 0,
        "OFICIO MULTIPLE": 0,
        "PROVEIDO": 0
    }

    # Contar los documentos en los datos obtenidos
    for rec in data:
        tipo = rec.get("TIPO_DOC", "").strip().upper()
        tipo = tipo.replace("Á", "A").replace("É", "E").replace("Í", "I").replace("Ó", "O").replace("Ú", "U")
        if tipo in tipos_documentos:
            tipos_documentos[tipo] += 1

    return tipos_documentos



def generar_grafico_tiempo_atencion(data):
  
    # Filtrar destinatarios únicos y sus respectivos tiempos de atención
    destinatarios = {entry["DESTINATARIO"]: entry["TIEMPO_DE_ATENCION"] for entry in data if entry["TIEMPO_DE_ATENCION"] != "N/A" and entry["DESTINATARIO"] != "N/A"}
    destinatarios = {k: v for k, v in destinatarios.items() if v.strip() != ""}  # Eliminar los espacios en blanco

    # Convertir tiempos a tipo numérico y eliminar valores no válidos
    destinatarios_validos = {k: float(v) for k, v in destinatarios.items() if v.replace('.', '', 1).isdigit()}
    
    # Ordenar por tiempo de atención (de mayor a menor)
    destinatarios_sorted = dict(sorted(destinatarios_validos.items(), key=lambda item: item[1], reverse=True))

    # Crear los dos subgráficos
    fig3 = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True, shared_yaxes=False, vertical_spacing=0.001)

    # Subgráfico de barras para tiempo de atención
    fig3.append_trace(go.Bar(
        x=list(destinatarios_sorted.values()),  # TIEMPO_DE_ATENCION en el eje X
        y=list(destinatarios_sorted.keys()),  # DESTINATARIO en el eje Y
        marker=dict(color='rgba(50, 171, 96, 0.6)', line=dict(color='rgba(50, 171, 96, 1.0)', width=1)),
        name="Destinatario respecto al tiempo",
        orientation='h',
    ), 1, 1)

    # Subgráfico de línea para el mismo tiempo de atención
    fig3.append_trace(go.Scatter(
        x=list(destinatarios_sorted.values()),
        y=list(destinatarios_sorted.keys()),
        mode='lines+markers',
        line_color='rgb(128, 0, 128)',
        name='Tiempo de atención',
    ), 1, 2)

    # Configuración de la apariencia del gráfico
    fig3.update_layout(
        xaxis=dict(title="Tiempo de Atención"),
        yaxis=dict(title="Destinatario", tickmode='array', tickvals=list(destinatarios_sorted.keys()), ticktext=list(destinatarios_sorted.keys())),
        xaxis2=dict(title="Tiempo de Atención", side="top"),
        yaxis2=dict(title="Destinatario", showticklabels=False),
        margin=dict(l=100, r=20, t=70, b=70),
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        bargap=0.3  # Aumentamos el espacio entre las barras (de 0.2 a 0.3)
    )

    # Ajuste para aumentar el espacio entre los destinatarios en el gráfico de barras
    fig3.update_layout(
        yaxis=dict(
            tickmode="array", 
            tickvals=list(destinatarios_sorted.keys()),
            ticktext=list(destinatarios_sorted.keys()),
            scaleanchor="x",  # Esto asegura que la escala de y sea coherente con el gráfico de barras
            tickangle=0,  # Alinea los ticks del eje Y de forma horizontal para evitar superposición
            showgrid=False  # Elimina las líneas de la cuadrícula si prefieres un diseño más limpio
        ),
    )

    annotations = []

    # Agregar etiquetas a los subgráficos con un desplazamiento más a la derecha
    for destinatario, tiempo in destinatarios_sorted.items():
        annotations.append(dict(
            xref='x1', yref='y1',
            y=destinatario, x=tiempo + 1.5,  # Incrementar el valor de x para mover el texto más a la derecha
            text=f'{int(tiempo)}',
            font=dict(family='Arial', size=12, color='rgb(50, 171, 96)'),
            showarrow=False,
        ))

    # Actualizar la disposición de las anotaciones
    fig3.update_layout(annotations=annotations)

    return fig3.to_html(full_html=False)


#FILTROS 
from datetime import datetime

def filter_by_date(data, start_date=None, end_date=None, start_field='F_EMISION', end_field='F_RECEPCION'):
    filtered_data = []
    for entry in data:
        try:
            # Obtener las fechas de inicio y fin
            start_date_str = entry.get(start_field, 'N/A')
            end_date_str = entry.get(end_field, 'N/A')

            # Convertir las cadenas de fecha a objetos datetime
            start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str != 'N/A' else None
            end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str != 'N/A' else None

            if start_date_obj and end_date_obj:
                if start_date and end_date:
                    if start_date <= start_date_obj <= end_date and start_date <= end_date_obj <= end_date:
                        filtered_data.append(entry)
                elif start_date and not end_date:
                    if start_date <= start_date_obj and start_date <= end_date_obj:
                        filtered_data.append(entry)
                elif not start_date and end_date:
                    if start_date_obj <= end_date and end_date_obj <= end_date:
                        filtered_data.append(entry)
                else:
                    filtered_data.append(entry)
        except ValueError:
            continue
    return filtered_data




def filter_by_tiempo_atencion(data, tiempo_values):
    return [entry for entry in data if str(entry.get('TIEMPO_DE_ATENCION')) in tiempo_values]



def filter_by_asunto(data, keyword):
    keyword = keyword.strip()
    return [entry for entry in data if keyword.lower() in entry.get('ASUNTO', '').lower()]


def filter_by_semaforo(data, semaforo_colors):
    filtered_data = []
    for entry in data:
        tiempo_atencion = entry.get('TIEMPO_DE_ATENCION', 'N/A')
        # Convertir tiempo_atencion a un entero para las comparaciones
        try:
            tiempo_atencion = int(tiempo_atencion)
        except ValueError:
            continue  # Si no se puede convertir, saltar a la siguiente entrada

        if 'Verde' in semaforo_colors and tiempo_atencion <= 1:
            filtered_data.append(entry)
        elif 'Amarillo' in semaforo_colors and tiempo_atencion == 2:
            filtered_data.append(entry)
        elif 'Rojo' in semaforo_colors and 3 <= tiempo_atencion <= 4:
            filtered_data.append(entry)
        elif 'Negro' in semaforo_colors and tiempo_atencion >= 5:
            filtered_data.append(entry)
    return filtered_data



# Vista para el dashboard principal (manteniendo la lógica original)
def main_dashboard(request):
    data = get_airtable_data()
    context = {}

    # Contar la cantidad de estados y documentos
    estado_counts = Counter([entry["ESTADO"] for entry in data])
    docu_counts = Counter([entry["N_DOCUMENTO"] for entry in data])
    total_records = len(data)

    unique_doc_numbers = set(entry["N_DOCUMENTO"] for entry in data if entry["N_DOCUMENTO"] != "N/A")
    total_unique_documents = len(unique_doc_numbers)
    # Obtener valores únicos de "TIEMPO_DE_ATENCION" desde los datos
    tiempo_atencion_values = set(entry.get('TIEMPO_DE_ATENCION') for entry in data if entry.get('TIEMPO_DE_ATENCION') is not None)
    
    tiempo_atencion_values = sorted(tiempo_atencion_values)
     # Aplicar filtros basados en la entrada del usuario
    if request.GET.get('start_date') and request.GET.get('end_date'): 
        start_date = datetime.strptime(request.GET['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(request.GET['end_date'], "%Y-%m-%d")
        data = filter_by_date(data, start_date, end_date, start_field='F_EMISION', end_field='F_RECEPCION')




    if request.GET.getlist('tiempo_atencion[]'):
        tiempo_values = request.GET.getlist('tiempo_atencion[]')
        data = filter_by_tiempo_atencion(data, tiempo_values)
    
    if request.GET.get('keyword'):
        data = filter_by_asunto(data, request.GET['keyword'])
    
    if request.GET.getlist('semaforo[]'):
        semaforo_colors = request.GET.getlist('semaforo[]')
        data = filter_by_semaforo(data, semaforo_colors)
        

    semaforo_counts = calculate_semaforo_counts(data)

    # Crear el gráfico de pie
    fig = go.Figure(go.Pie(
        labels=['Verde', 'Amarillo', 'Rojo', 'Negro'],
        values=[semaforo_counts['Verde'], semaforo_counts['Amarillo'], semaforo_counts['Rojo'], semaforo_counts['Negro']],
        hoverinfo='label+value+percent',
        textinfo='value+label',
        marker=dict(colors=['#28a745', '#ffc107', '#dc3545', '#343a40'])
    ))

    # Crear un gráfico con Plotly
    # df = px.data.gapminder().query("continent=='Oceania'")  # Utiliza cualquier dataframe que necesites
    # fig = px.line(df, x="year", y="lifeExp", color='country')


    # fig.update_layout(showlegend=False)

    plot_1 = fig.to_html(full_html=False)
    
    # Obtener conteo de documentos por tipo
    doc_counts = contar_documentos_por_tipo(data)
    doc_counts_clean = {
        "CARTA": doc_counts.get("CARTA", 0),
        "HOJA_DE_ENVIO": doc_counts.get("HOJA DE ENVIO", 0),
        "INFORME": doc_counts.get("INFORME", 0),
        "MEMORANDO_MULTIPLE": doc_counts.get("MEMORANDO MULTIPLE", 0),
        "OFICIO": doc_counts.get("OFICIO", 0),
        "OFICIO_MULTIPLE": doc_counts.get("OFICIO MULTIPLE", 0),
        "PROVEIDO": doc_counts.get("PROVEIDO", 0)
    }

    # Crear el gráfico de barras con Plotly
    fig2 = px.bar(
        x=list(doc_counts.keys()),
        y=list(doc_counts.values()),
        text=list(doc_counts.values()),
        labels={"x": "Tipo de Documento", "y": "Cantidad"},
    )

    fig2.update_traces(texttemplate='%{text}', textposition='outside')
    fig2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    plot_2 = fig2.to_html(full_html=False)

    plot_html = generar_grafico_tiempo_atencion(data)

    # Pasar los datos y gráficos a la plantilla
    context = {
        'plot_1': plot_1,
        'data': data,
        'estado_counts': estado_counts,
        'docu_counts': docu_counts,
        'semaforo_counts': semaforo_counts,
        'plot_2': plot_2,
        # 'doc_counts': doc_counts,
        'doc_counts': doc_counts_clean,
        'plot_html': plot_html,
        'tiempo_atencion_values': tiempo_atencion_values,
        'total_records': total_records,
        'total_unique_documents': total_unique_documents,
    }

    # Renderizar la página con los datos y el gráfico
    return render(request, 'content.html', context=context)

# Vista para la tabla extraída de Airtable
def table(request):
    data = get_airtable_data()

    # return render(request, "table.html", context)
    return render(request, "table.html", {"data": data})

