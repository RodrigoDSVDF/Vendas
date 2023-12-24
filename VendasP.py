
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl


@st.cache_data# Corrigir o nome do decorador
def importar_dados():
    caminho_arquivo_excel = (r"Vendas.xlsx")
    df = pd.read_excel(caminho_arquivo_excel, parse_dates=['Data da Venda'])
    df['Mês'] = df['Data da Venda'].dt.strftime('%B')
    df['Ano'] = df['Data da Venda'].dt.year
    return df

st.title("Análises de Vendas")
st.sidebar.header("Menu")

opcoes = ["Home", "Visualização"]
escolha = st.sidebar.selectbox("Escolha uma opção", opcoes, key='unique_key1')


df = importar_dados()

faturamento_mensal = df.groupby(['Ano', 'Mês'])['Faturamento'].sum().reset_index()

if escolha == 'Visualização':
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    chart = alt.Chart(faturamento_mensal).mark_bar().encode(
        x=alt.X('Mês', sort=meses),
        y='Faturamento',
        color='Ano',
        tooltip=['Mês', 'Ano', 'Faturamento']
    ).properties(
        title='Faturamento Mensal ao Longo do Tempo',
        width=800,
        height=600
    )
    st.altair_chart(chart)

    fig = px.line(faturamento_mensal, x='Mês', y='Faturamento', color='Ano', markers=True)
    fig.update_layout(
        title='Faturamento Mensal ao Longo do Tempo',
        xaxis_title='Mês',
        yaxis_title='Faturamento',
        legend_title='Ano'
    )
    fig.update_traces(
        text=faturamento_mensal['Faturamento'].apply(lambda x: f'{x:,.2f}'),
        textposition='top center'
    )
    st.plotly_chart(fig)

    df['Data da Venda'] = pd.to_datetime(df['Data da Venda'])
    df['Mês'] = df['Data da Venda'].dt.month
    df['Ano'] = df['Data da Venda'].dt.year

    quantidade_mensal = df.groupby(['Ano', 'Mês'])['Qtd. Vendida'].sum().reset_index()
    faturamento_mensal = df.groupby(['Ano', 'Mês'])['Faturamento'].sum().reset_index()

    plt.figure(figsize=(12, 6))
    ax1 = sns.barplot(x='Mês', y='Qtd. Vendida', hue='Ano', data=quantidade_mensal, palette='deep')  # Altere a paleta para 'deep' para um azul mais profissional
    plt.title('Quantidade Vendida por Mês')
    plt.xlabel('Mês')
    plt.ylabel('Quantidade Vendida')
    plt.legend(title='Ano')

    for p in ax1.patches:
        ax1.annotate(f'{p.get_height():,.0f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha='center', va='bottom', xytext=(0, 10), textcoords='offset points', fontsize=8)

    st.pyplot(plt)

    # Agrupando os dados por produto e calculando a soma das vendas para cada produto
    quantidade_vendida_por_produto = df.groupby('Produto')['Qtd. Vendida'].sum().sort_values(ascending=False)

    # Criando um gráfico de barras para visualizar a quantidade vendida por produto
    plt.figure(figsize=(10, 6))
    bars = plt.bar(quantidade_vendida_por_produto.index, quantidade_vendida_por_produto, color='navy')

    plt.xlabel('Produto')
    plt.ylabel('Quantidade Vendida')
    plt.title('Quantidade Vendida por Produto')

    plt.xticks(rotation=45, ha='right')  # Adicione 'ha='right' para alinhar os rótulos à direita

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, round(yval, 2), ha='center', va='bottom')

    st.pyplot(plt)










