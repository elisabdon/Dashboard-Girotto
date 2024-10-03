import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title='📊 Análise de Uso de Mídias Sociais',
    page_icon='🚀',
    layout='wide'
)

# Carregar os dados do arquivo
df_socialmedia = pd.read_csv('socialmedia.csv')

# Correção de possíveis erros de digitação nos nomes das colunas
df_socialmedia.rename(columns={'UsageDuraiton': 'UsageDuration'}, inplace=True)

# Personalização da dashboard
st.markdown("<h1 style='text-align: center; color: #00FF7F;'>🚀 Análise de Uso de Mídias Sociais 🚀</h1>", unsafe_allow_html=True)

with st.sidebar:
    st.header('🎛️ Filtros')
    
    # Filtro - país
    countries = df_socialmedia['Country'].unique()
    selected_countries = st.multiselect('🌍 Selecione os países:', countries, default=countries)
    
    # Filtro - faixa etária
    min_age = int(df_socialmedia['Age'].min())
    max_age = int(df_socialmedia['Age'].max())
    age_range = st.slider('👥 Selecione a faixa etária:', min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Filtro -país e idade
df_filtered = df_socialmedia[
    (df_socialmedia['Country'].isin(selected_countries)) &
    (df_socialmedia['Age'] >= age_range[0]) &
    (df_socialmedia['Age'] <= age_range[1])
]

age_bins = [0, 18, 25, 35, 50, 65, 100]
if age_bins != sorted(age_bins):
    st.error('..')
else:
    age_labels = ['Até 18', '19-25', '26-35', '36-50', '51-65', 'Acima de 65']
    df_filtered['Faixa Etária'] = pd.cut(df_filtered['Age'], bins=age_bins, labels=age_labels, include_lowest=True)

    # Calcular a média //CORRIGIDO
    avg_usage_by_age_group = df_filtered.groupby('Faixa Etária')['UsageDuration'].mean().reset_index()
    avg_usage_by_age_group['UsageDuration'].fillna(0, inplace=True)

    def format_duration(minutes):
        if pd.isnull(minutes) or minutes == 0:
            return '0 min'
        hours = int(minutes // 60)
        minutes = int(minutes % 60)
        if hours > 0:
            return f'{hours} h {minutes} min'
        else:
            return f'{minutes} min'

    avg_usage_by_age_group['Duração Média'] = avg_usage_by_age_group['UsageDuration'].apply(format_duration)
    st.subheader('')

    # Gráfico 1: Tempo Total de Uso por País 
    st.markdown("### 🌍 Tempo Total de Uso por País")
    country_usage = df_filtered.groupby('Country')['UsageDuration'].sum().reset_index()
    country_usage = country_usage.sort_values(by='UsageDuration', ascending=False)
    fig_country_usage = px.bar(
        country_usage,
        x='Country',
        y='UsageDuration',
        color='UsageDuration',
        color_continuous_scale='Blues',
        labels={'Country': 'País', 'UsageDuration': 'Duração Total de Uso (minutos)'},
        template='plotly_dark'
    )
    st.plotly_chart(fig_country_usage, use_container_width=True)

    # Gráfico 2: Média de Duração de Uso por Faixa Etária // CORRIGIDO PÓS AVALIAÇÃO
    st.markdown("### 👥 Média de Duração de Uso por Faixa Etária")
    fig_age_group = px.bar(
        avg_usage_by_age_group,
        x='Faixa Etária',
        y='UsageDuration',
        color='UsageDuration',
        color_continuous_scale='Purples',
        labels={'Faixa Etária': 'Faixa Etária', 'UsageDuration': 'Duração Média (minutos)'},
        template='plotly_dark',
        text='Duração Média'
    )
    fig_age_group.update_traces(textposition='outside')
    st.plotly_chart(fig_age_group, use_container_width=True)

    # Gráfico 3: Total de Usuários por Faixa Etária //CORRIGIDO PÓS AVALIAÇÃO
    st.markdown("### 📈 Total de Usuários por Faixa Etária")
    users_by_age_group = df_filtered.groupby('Faixa Etária')['UserId'].nunique().reset_index()
    users_by_age_group = users_by_age_group.sort_values('Faixa Etária')
    fig_users_age = px.bar(
        users_by_age_group,
        x='Faixa Etária',
        y='UserId',
        color='UserId',
        color_continuous_scale='Greens',
        labels={'Faixa Etária': 'Faixa Etária', 'UserId': 'Número de Usuários'},
        template='plotly_dark'
    )
    st.plotly_chart(fig_users_age, use_container_width=True)

    # Gráfico 4: Idade vs Duração de Uso // CORRIGIDO PÓS AVALIAÇÃO
    st.markdown("### 📊 Idade vs Duração de Uso")
    age_usage = df_filtered.groupby('Age')['UsageDuration'].mean().reset_index()
    fig_age_usage = px.bar(
        age_usage,
        x='Age',
        y='UsageDuration',
        color='UsageDuration',
        color_continuous_scale='Turbo',
        labels={'Age': 'Idade', 'UsageDuration': 'Duração Média de Uso (hora)'},
        template='plotly_dark'
    )
    st.plotly_chart(fig_age_usage, use_container_width=True)

    # rodapé bonitinho
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Atividade de Probabilidade e Estatistica por Renan e Elissandra - 2024</p>", unsafe_allow_html=True)
