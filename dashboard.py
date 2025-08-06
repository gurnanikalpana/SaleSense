import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import sqlite3

# Connect to database
def load_data():
    conn = sqlite3.connect("sales.db")
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    return df

app = dash.Dash(__name__)

df = load_data()

app.layout = html.Div([
    html.H1("📊 SaleSense – Sales Analytics Dashboard", style={'textAlign': 'center'}),
    html.Label("Select Category:"),
    dcc.Dropdown(
        id='category_filter',
        options=[{'label': cat, 'value': cat} for cat in df['category'].unique()],
        multi=True
    ),
    dcc.Graph(id="sales_trend"),
    dcc.Graph(id="category_distribution")
])

@app.callback(
    [Output("sales_trend", "figure"),
     Output("category_distribution", "figure")],
    [Input("category_filter", "value")]
)
def update_graph(selected_categories):
    filtered_df = df
    if selected_categories:
        filtered_df = df[df['category'].isin(selected_categories)]

    sales_trend = px.line(filtered_df, x="date", y="price", title="Sales Trend Over Time")
    cat_dist = filtered_df.groupby("category", as_index=False)["price"].sum()
    category_distribution = px.bar(cat_dist, x="category", y="price", title="Sales by Category")

    return sales_trend, category_distribution

if __name__ == "__main__":
    app.run_server(debug=True)
