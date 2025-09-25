import pandas as pd
import plotly.graph_objs as go
import ast

df = pd.read_csv("Formula1_Pitstop_Data_clean.csv")

def count_stops(text):
    if pd.isna(text) or text.strip() == "":
        return 0
    try:
        return len(ast.literal_eval(text))
    except Exception:
        return 0

df["PitStopCount"] = df["PitStops"].apply(count_stops)

counts = df.groupby("Season")["PitStopCount"].sum().reset_index(name="pit_count")

trace = go.Bar(
    x=counts["Season"],
    y=counts["pit_count"],
    marker=dict(
        color=counts["pit_count"],
        coloraxis="coloraxis",
        line=dict(color="black", width=2)
    )
)

layout = go.Layout(
    title=dict(
        text="Общее количество пит-стопов по сезонам",
        x=0.5,
        font=dict(size=20)
    ),
    xaxis=dict(
        title=dict(text="Сезон", font=dict(size=16)),
        tickangle=315,
        tickfont=dict(size=14),
        showgrid=True,
        gridwidth=2,
        gridcolor="ivory"
    ),
    yaxis=dict(
        title=dict(text="Число пит-стопов", font=dict(size=16)),
        tickfont=dict(size=14),
        showgrid=True,
        gridwidth=2,
        gridcolor="ivory"
    ),
    coloraxis=dict(colorscale="Viridis"),
    height=700,
    margin=dict(l=40, r=40, t=80, b=80)
)

fig = go.Figure(data=[trace], layout=layout)
fig.write_html("bar_plot.html", include_plotlyjs="cdn")
