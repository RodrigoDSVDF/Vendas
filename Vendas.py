import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Cache para otimização de carregamento dos dados
@st.cache_data
def importar_dados():
    caminho_arquivo_excel = (r'C:\Users\Rodrigo_df\Downloads\Vendas.xlsx')
    df = pd.read_excel(caminho_arquivo_excel, parse_dates=['Data da Venda'])
    df['Mês'] = df['Data da Venda'].dt.strftime('%B')
    df['Ano'] = df['Data da Venda'].dt.year
    return df

df = importar_dados()

# Mapeamento de meses para português
meses_portugues = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
map_meses = dict(zip(range(1, 13), meses_portugues))
df['Mês'] = df['Data da Venda'].dt.month.replace(map_meses)
df['Ano'] = df['Data da Venda'].dt.year

# Título e Menu
st.title("Dashboard de Análises de Vendas")
opcoes = ["Home", "Visualização de Vendas"]
escolha = st.sidebar.selectbox("Escolha uma opção", opcoes)

if escolha == "Visualização de Vendas":
    st.header("Análise Geral de Vendas")

    col1, col2 = st.columns(2)
    
    # Faturamento por Marca
    with col1:
        faturamento_marca = df.groupby('Marca')['Faturamento'].sum().reset_index()
        fig_marca = px.bar(faturamento_marca, x='Marca', y='Faturamento', title='Faturamento por Marca')
        st.plotly_chart(fig_marca, use_container_width=True)
    
    # Vendas por Região
    with col2:
        vendas_regiao = df.groupby('Região Destino')['Qtd. Vendida'].sum().reset_index()
        fig_regiao = px.bar(vendas_regiao, x='Região Destino', y='Qtd. Vendida', title='Vendas por Região')
        st.plotly_chart(fig_regiao, use_container_width=True)
    
    # Preço Médio de Venda por Produto
    st.header("Preço Médio de Venda por Produto")
    preco_medio_produto = df.groupby('Produto').apply(lambda x: (x['Preco Unitario'] * x['Qtd. Vendida']).sum() / x['Qtd. Vendida'].sum()).reset_index(name='Preço Médio')
    fig_preco_medio = px.bar(preco_medio_produto, x='Produto', y='Preço Médio', title='Preço Médio de Venda por Produto')
    st.plotly_chart(fig_preco_medio, use_container_width=True)
    
   # Continuação do código Streamlit...

# Adicionando novas análises ao dashboard
# Continuação do código Streamlit...

# Adicionando análises de vendas ao dashboard
if escolha == "Visualização de Vendas":
    st.header("Quantidade Vendida ao Longo do Tempo")

    # Agrupando os dados para análise ao longo do tempo
    vendas_ao_longo_do_tempo = df.groupby(['Ano', 'Mês'])['Qtd. Vendida'].sum().reset_index()
    
    # Gráfico de Linha - Quantidade Vendida ao Longo do Tempo
    vendas_tempo_linha = px.line(vendas_ao_longo_do_tempo, x='Mês', y='Qtd. Vendida', color='Ano', markers=True, title='Quantidade Vendida ao Longo do Tempo')
    st.plotly_chart(vendas_tempo_linha, use_container_width=True)

    st.header("Produtos Mais Vendidos")

    # Agrupando os dados para os produtos mais vendidos
    produtos_mais_vendidos = df.groupby('Produto')['Qtd. Vendida'].sum().sort_values(ascending=False).reset_index()

    # Limitando o gráfico aos top 10 produtos mais vendidos para melhor visualização
    produtos_mais_vendidos_top10 = produtos_mais_vendidos.head(10)
    
    # Gráfico de Barras - Produtos Mais Vendidos
    produtos_vendidos_barras = px.bar(produtos_mais_vendidos_top10, x='Produto', y='Qtd. Vendida', title='Top 10 Produtos Mais Vendidos')
    st.plotly_chart(produtos_vendidos_barras, use_container_width=True)
