import streamlit as st
import pandas as pd
import plotly.express as px

# Set the layout to wide
st.set_page_config(layout="wide")


# Load the SpaceX launch data
df = pd.read_csv(r'C:\Users\Tatenda\Downloads\spacex_launch_dash.csv')

# Custom CSS to change the font family to Roboto
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Title for the dashboard if you are not using a custom HTML structure
#st.title("SpaceX Launch Records Dashboard")


# Custom HTML structure to center the dashboard title
st.markdown(
    """
    <div style="display: flex; justify-content: center;">
        <h1>SpaceX Launch Records Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)


# Task 1: Add a Launch Site Drop-down Input Component
launch_sites = df['Launch Site'].unique()
launch_sites_with_all = ['All Sites'] + list(launch_sites)
selected_site = st.selectbox('', launch_sites_with_all)


# Task 2: Render success-pie-chart based on selected site dropdown
if selected_site == 'All Sites':
    success_by_site = df[df['class'] == 1].groupby('Launch Site').size().reset_index(name='Total Success')
    fig_pie = px.pie(success_by_site, values='Total Success', names='Launch Site', title='Total Success Launches by Site')
    fig_pie.update_traces(textposition='inside', textinfo='percent')
else:
    filtered_data = df[df['Launch Site'] == selected_site]
    success_count = filtered_data[filtered_data['class'] == 1].shape[0]
    fig_pie = px.pie(
        values=[success_count, 1],
        names=['Total Success', 'Remaining'],
        title=f'Success Ratio for {selected_site}',
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent')

fig_pie.update_layout(
    autosize= False,
    width=1200,
    height=500,
    font_family='Roboto Mono',
    font_size=12,
)

st.plotly_chart(fig_pie)






# Task 3: Add a Range Slider to Select Payload
payload_min = int(df['Payload Mass (kg)'].min())
payload_max = int(df['Payload Mass (kg)'].max())
payload_range = st.slider('Select Payload Range (kg)', payload_min, payload_max, (payload_min, payload_max))

# Task 4: Correlation between payload and success for all sites
fig_scatter = px.scatter(
    df,
    x='Payload Mass (kg)',
    y='class',
    color='Launch Site',
    title='Correlation between Payload and Success for All Sites',
    labels={'class': 'Class', 'Launch Site': 'Launch Site'}
)

fig_scatter.update_layout(
    autosize=True,
    width=1200,
    height=500,
    font_family='Roboto Mono',
    font_size=12
)

fig_scatter.update_yaxes(title='Class')

st.plotly_chart(fig_scatter)





