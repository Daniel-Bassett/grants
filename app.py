import pandas as pd
import plotly_express as px
import streamlit as st
from streamlit_option_menu import option_menu

@st.cache_data
def load_data(filepath):
    return pd.read_parquet(filepath)

df = load_data('processed_data/nsf.parquet')

# create sidebar menu with options
selected = option_menu(
    menu_title=None,
    menu_icon='cast',
    default_index=0,
    options=['Year', 'State', 'Organization'],
    orientation='horizontal',
    icons=['graph-up', 'globe', 'bank'],
    styles= {'container': {
                'font-size': '12px'
    }}
)

years = st.slider('Year Range', value=(2000, 2022), min_value=2000, max_value=2022 )

year_filter = year_filter = df['start_year'].between(years[0], years[1])

terms_options = sorted([
    'Electric Vehicles', 'Automotive', 'IT ',
    'Biotech', 'Energy', 'Agriculture', 'Ocean',
    'Health',
    'Robotics', 'Automation', 'Electronics',
    'Climate', 'Aerospace', 'Cybersecurity',
    'Blockchain', ' (All)'
])



term = st.selectbox('Choose a term', options=terms_options)
term_filter = term_filter = df['Title'].str.contains(term)

if term != ' (All)':
    filtered_df = df[year_filter & term_filter].copy()
else:
    filtered_df = df[year_filter].copy()

if selected == 'Year':
    # by year
    filtered_df = filtered_df.groupby('start_year', as_index=False).size()
    filtered_df = filtered_df.rename(columns={'size': 'Number_Awards'})

    fig = px.line(
        data_frame=filtered_df,
        title=f'Number of Awards - {term}',
        x='start_year',
        y='Number_Awards'
        )

    fig.update_layout(
        yaxis_title="Number of Awards", 
        xaxis_title='Year',
        title_x=0.35,
        showlegend=False,
        dragmode=False
        )

    st.plotly_chart(fig)


if selected == 'State':
    # top 10 by state
    filtered_df = filtered_df.groupby('State', as_index=False).size().sort_values(by='size', ascending=False).head(10)

    fig = px.bar(
        data_frame=filtered_df,
        x='State',
        y='size',
        title=f'Top 10 States - {term}'
    )

    fig.update_layout(
        yaxis_title="Number of Awards", 
        xaxis_title='State',
        title_x=0.4,
        showlegend=False,
        dragmode=False
        )

    st.plotly_chart(fig)


if selected == 'Organization':
    # by organizaton
    filtered_df = filtered_df.groupby('Organization', as_index=False).size().sort_values(by='size', ascending=False).head(10).sort_values(by='size', ascending=True)

    fig = px.bar(
        data_frame=filtered_df,
        y='Organization',
        x='size',
        title=f'Top 10 Organizations - {term}',
        orientation='h'
    )

    fig.update_layout(
        xaxis_title="Number of Awards", 
        yaxis_title='Organization',
        title_x=0.4,
        showlegend=False,
        dragmode=False
        )

    st.plotly_chart(fig)