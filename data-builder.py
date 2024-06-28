import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import random

# Inicializar o aplicativo Dash
app = dash.Dash(__name__)

# Constantes iniciais
W_default = 50000  # Peso da aeronave (em Newtons)
S_default = 30  # Área da asa (em metros quadrados)
rho0 = 1.225  # Densidade do ar ao nível do mar (kg/m^3)

# Layout do aplicativo
app.layout = html.Div(style={'backgroundColor': '#f0f0f0', 'color': '#333333', 'padding': '20px'}, children=[
    html.H1("MONITORAMENTO DE DESEMPENHO DE CRUZEIRO - PROJETO DE INTRODUÇÃO A ENGENHARIA",
            style={'textAlign': 'center', 'font-size': '32px', 'color': '#003366'}),

    # Tabela para entrada de valores
    html.Div([
        html.Label('Peso da Aeronave (N):', style={'color': '#003366'}),
        dcc.Input(id='input-weight', type='number', value=W_default, style={'margin': '0 10px'}),
        html.Label('Área da Asa (m²):', style={'color': '#003366'}),
        dcc.Input(id='input-area', type='number', value=S_default, style={'margin': '0 10px'}),
        html.Button('Atualizar', id='update-button', n_clicks=0, style={'margin': '0 10px'})
    ], style={'textAlign': 'center', 'margin-bottom': '20px'}),

    # Gráficos
    html.Div([
        dcc.Graph(id='speed-graph'),
        dcc.Graph(id='altitude-graph'),
        dcc.Graph(id='power-graph'),
        dcc.Graph(id='polar-graph'),  # Novo gráfico de polar de arrasto
        dcc.Graph(id='speed-histogram'),
        dcc.Graph(id='altitude-histogram')
    ], style={'textAlign': 'center'}),

    # Estatísticas
    html.Div([
        html.H3('Estatísticas Descritivas', style={'color': '#003366'}),
        html.Div(id='stats-container')
    ], style={'textAlign': 'center', 'margin-top': '20px'}),

    # Intervalo de atualização
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # Atualização a cada 1 segundo
        n_intervals=0
    ),

    # Slider para selecionar intervalo de tempo
    html.Label('Selecione o intervalo de tempo:', style={'color': '#003366'}),
    dcc.RangeSlider(
        id='time-range-slider',
        min=0,
        max=100,  # Número arbitrário para o exemplo
        step=1,
        value=[0, 10],
        marks={i: {'label': str(i), 'style': {'color': '#003366'}} for i in range(0, 101, 10)}
    ),
    html.Div(id='slider-output-container', style={'color': '#003366'})
])

# Dados simulados iniciais
times = list(range(100))
speed = [random.uniform(200, 250) for _ in range(100)]
altitude = [random.uniform(30000, 35000) for _ in range(100)]
thrust = [random.uniform(20000, 25000) for _ in range(100)]  # Substituindo potência por força de tração


# Callback para atualizar os gráficos e estatísticas
@app.callback(
    [Output('speed-graph', 'figure'),
     Output('altitude-graph', 'figure'),
     Output('power-graph', 'figure'),
     Output('polar-graph', 'figure'),  # Novo output para o gráfico de polar de arrasto
     Output('speed-histogram', 'figure'),
     Output('altitude-histogram', 'figure'),
     Output('stats-container', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('time-range-slider', 'value'),
     Input('update-button', 'n_clicks')],
    [State('input-weight', 'value'), State('input-area', 'value')]
)
def update_graphs(n, time_range, n_clicks, weight, area):
    global times, speed, altitude, thrust

    # Verificar se os valores de weight e area são válidos
    if weight is None or area is None or weight <= 0 or area <= 0:
        weight = W_default
        area = S_default

    # Atualizar constantes com os valores inseridos pelo usuário
    W = weight
    S = area

    # Simulação de dados (substituir por dados reais)
    new_time = times[-1] + 1
    times.append(new_time)
    speed.append(random.uniform(200, 250))
    altitude.append(random.uniform(30000, 35000))
    thrust.append(random.uniform(20000, 25000))  # Atualizando força de tração

    # Manter somente os últimos 100 valores para evitar sobrecarga de memória
    times = times[-100:]
    speed = speed[-100:]
    altitude = altitude[-100:]
    thrust = thrust[-100:]

    # Seleção de intervalo de tempo
    start, end = time_range
    filtered_times = times[start:end]
    filtered_speed = speed[start:end]
    filtered_altitude = altitude[start:end]
    filtered_thrust = thrust[start:end]

    # Cálculo dos coeficientes de sustentação e arrasto
    rho = [rho0 * (1 - alt / 44330) for alt in filtered_altitude]
    cl = [2 * W / (r * (v ** 2) * S) for r, v in zip(rho, filtered_speed)]
    cd = [2 * t / (r * (v ** 2) * S) for t, r, v in zip(filtered_thrust, rho, filtered_speed)]  # Usando força de tração

    # Criação das figuras
    speed_fig = go.Figure()
    speed_fig.add_trace(
        go.Scatter(x=filtered_times, y=filtered_speed, mode='lines', name='Velocidade', line=dict(color='#003366')))
    speed_fig.update_layout(title='Velocidade em Função do Tempo', xaxis_title='Tempo', yaxis_title='Velocidade',
                            title_x=0.5, title_font_size=24, paper_bgcolor='#f0f0f0', plot_bgcolor='#f0f0f0',
                            font=dict(color='#003366'))

    altitude_fig = go.Figure()
    altitude_fig.add_trace(
        go.Scatter(x=filtered_times, y=filtered_altitude, mode='lines', name='Altitude', line=dict(color='#6699cc')))
    altitude_fig.update_layout(title='Altitude em Função do Tempo', xaxis_title='Tempo', yaxis_title='Altitude',
                               title_x=0.5, title_font_size=24, paper_bgcolor='#f0f0f0', plot_bgcolor='#f0f0f0',
                               font=dict(color='#003366'))

    power_fig = go.Figure()
    power_fig.add_trace(go.Scatter(x=filtered_times, y=filtered_thrust, mode='lines', name='Força de Tração',
                                   line=dict(color='#cccccc')))
    power_fig.update_layout(title='Força de Tração em Função do Tempo', xaxis_title='Tempo',
                            yaxis_title='Força de Tração', title_x=0.5, title_font_size=24, paper_bgcolor='#f0f0f0',
                            plot_bgcolor='#f0f0f0', font=dict(color='#003366'))

    polar_fig = go.Figure()
    polar_fig.add_trace(go.Scatter(x=cl, y=cd, mode='lines', name='Polar de Arrasto', line=dict(color='#999999')))
    polar_fig.update_layout(title='Polar de Arrasto em Cruzeiro', xaxis_title='C_L', yaxis_title='C_D', title_x=0.5,
                            title_font_size=24, paper_bgcolor='#f0f0f0', plot_bgcolor='#f0f0f0',
                            font=dict(color='#003366'))

    # Histogramas
    speed_histogram = go.Figure()
    speed_histogram.add_trace(
        go.Histogram(x=filtered_speed, nbinsx=20, name='Distribuição de Velocidade', marker=dict(color='#003366')))
    speed_histogram.update_layout(title='Histograma de Velocidade', xaxis_title='Velocidade', yaxis_title='Contagem',
                                  title_x=0.5, title_font_size=24, paper_bgcolor='#f0f0f0', plot_bgcolor='#f0f0f0',
                                  font=dict(color='#003366'))

    altitude_histogram = go.Figure()
    altitude_histogram.add_trace(
        go.Histogram(x=filtered_altitude, nbinsx=20, name='Distribuição de Altitude', marker=dict(color='#6699cc')))
    altitude_histogram.update_layout(title='Histograma de Altitude', xaxis_title='Altitude', yaxis_title='Contagem',
                                     title_x=0.5, title_font_size=24, paper_bgcolor='#f0f0f0', plot_bgcolor='#f0f0f0',
                                     font=dict(color='#003366'))

    # Estatísticas Descritivas
    df = pd.DataFrame({
        'Velocidade': filtered_speed,
        'Altitude': filtered_altitude,
        'Força de Tração': filtered_thrust
    })
    stats = df.describe().to_dict()

    # Descrições das estatísticas descritivas
    descriptions = {
        'count': 'Número de Observações',
        'mean': 'Média',
        'std': 'Desvio Padrão',
        'min': 'Valor Mínimo',
        '25%': '1º Quartil (25% dos dados são menores que este valor)',
        '50%': 'Mediana (50% dos dados são menores que este valor)',
        '75%': '3º Quartil (75% dos dados são menores que este valor)',
        'max': 'Valor Máximo'
    }

    stats_table = html.Table([
        html.Thead(
            html.Tr([html.Th("Estatística")] + [html.Th(col) for col in stats.keys()])
        ),
        html.Tbody([
            html.Tr([html.Td(descriptions[stat])] + [html.Td(round(stats[col][stat], 2)) for col in stats.keys()]) for
            stat in stats['Velocidade'].keys()
        ])
    ], style={'width': '100%', 'margin': '20px 0', 'color': '#003366'})

    return speed_fig, altitude_fig, power_fig, polar_fig, speed_histogram, altitude_histogram, stats_table


# Callback para exibir intervalo de tempo selecionado
@app.callback(
    Output('slider-output-container', 'children'),
    Input('time-range-slider', 'value'))
def update_output(value):
    return f'Intervalo de Tempo Selecionado: {value}'


# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
