from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('ecommerce_estatistica.csv')
print(df.head().to_string())

lista_temporada = df['Temporada'].unique()
options = [{'label': Temporada, 'value': Temporada} for Temporada in lista_temporada]


def cria_graficos(selecao_valores):
    filtro_df = df[df['Temporada'].isin(selecao_valores)]
    # Gráfico de Barra
    fig1 = px.bar(filtro_df, x='Qtd_Vendidos_Cod', y='Desconto_MinMax', color='Temporada', barmode='group', color_discrete_sequence=px.colors.qualitative.Vivid)
    fig1.update_layout(
        title='Gráfico de Barras - Valores por Categoria',
        xaxis_title='Quantidade de Vendas',
        yaxis_title='Desconto (Normalizado)',
        legend_title='Temporada',
        bargap=0.5,
        bargroupgap=0,
        plot_bgcolor='rgba(0, 0, 255, 0.02)',
        paper_bgcolor='rgba(205, 159, 255, 0.12)'
    )
    # Gráfico de histograma
    fig2 = px.histogram(filtro_df, x='Nota', y='N_Avaliações', color='Temporada', nbins=10, color_discrete_sequence=px.colors.qualitative.Vivid)
    fig2.update_layout(
        title='Gráfico de Histograma - Frequência de Notas',
        xaxis_title='Nota',
        yaxis_title='Frequência em que aparece',
        legend_title='Temporada',
        plot_bgcolor='rgba(0, 0, 255, 0.02)',
        paper_bgcolor='rgba(205, 159, 255, 0.12)'
    )
    # Gráfico de Dispersão
    fig3 = px.scatter(filtro_df, x='Desconto', y='Qtd_Vendidos_Cod', color='Temporada', color_discrete_sequence=px.colors.qualitative.Vivid)
    fig3.update_layout(
        title='Gráfico de Dispersão - Desconto e Quantidade de Vendas',
        xaxis_title='Desconto',
        yaxis_title='Qtd_Vendidos_Cod',
        legend_title='Temporada',
        plot_bgcolor='rgba(0, 0, 255, 0.02)',
        paper_bgcolor='rgba(205, 159, 255, 0.12)'
    )
    # Mapa de Calor
    fig4 = px.density_heatmap(filtro_df, x='Preço', y='Nota', z='Desconto', color_continuous_scale=px.colors.sequential.GnBu)
    fig4.update_layout(
        title='Mapa de Calor comparando Preço, Desconto e Notas dadas',
        xaxis_title='Preço',
        yaxis_title='Notas',
        legend_title='Temporada',
        plot_bgcolor='rgba(0, 0, 255, 0.02)',
        paper_bgcolor='rgba(205, 159, 255, 0.12)'
    )
    fig5 = px.pie(filtro_df, values='Qtd_Vendidos_Cod', names='Temporada', hole=.3, color_discrete_map=px.colors.qualitative.Alphabet)
    fig5.update_layout(
        title='Gráfico mostrando a relação entre a quantidade de vendas e a temporada',
        plot_bgcolor='rgba(0, 0, 255, 0.02)',
        paper_bgcolor='rgba(205, 159, 255, 0.12)'
    )
    fig6 = px.density_contour(filtro_df, x='Preço', y='Qtd_Vendidos_Cod', color_discrete_sequence=px.colors.sequential.Magma)
    fig6.update_layout(
        title='Gráfico de Densidade da relação entre Preço e Vendas',
        yaxis_title='Quantidade de Vendas',
        plot_bgcolor='rgba(0, 0, 255, 0.02)',
        paper_bgcolor='rgba(205, 159, 255, 0.12)'
    )

    return fig1, fig2, fig3, fig4, fig5, fig6


def cria_app():
    app = Dash(__name__)
    app.layout = html.Div([
        html.H1("Dashboard Interativo com base na Temporada da Coleção"),
        dcc.Checklist(
            id='id_selecao_valores',
            options=options,
            value=[lista_temporada[0]],
        ),
        dcc.Graph(id='id_grafico_barra'),
        dcc.Graph(id='id_grafico_histograma'),
        dcc.Graph(id='id_grafico_dispersao'),
        dcc.Graph(id='id_mapa_calor'),
        dcc.Graph(id='id_grafico_pizza'),
        dcc.Graph(id='id_grafico_densidade')
    ])
    return app


if __name__ == '__main__':
    app = cria_app()


    @app.callback(
        [Output('id_grafico_barra', 'figure'),
        Output('id_grafico_histograma', 'figure'),
        Output('id_grafico_dispersao', 'figure'),
         Output('id_mapa_calor', 'figure'),
         Output('id_grafico_pizza', 'figure'),
         Output('id_grafico_densidade', 'figure')
    ],
        [Input('id_selecao_valores', 'value')]
    )
    def atualiza_grafico(selecao_valores):
        return cria_graficos(selecao_valores)


    app.run(debug=True, port=7050)