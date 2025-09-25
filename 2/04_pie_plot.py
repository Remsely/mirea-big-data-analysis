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

fig = go.Figure(
    go.Pie(
        labels=counts["Season"].astype(str),
        values=counts["pit_count"],
        marker=dict(line=dict(color="black", width=2))
    )
)

fig.update_layout(
    title=dict(
        text="Доля пит-стопов по всем сезонам",
        x=0.5,
        font=dict(size=20)
    ),
    height=700,
    margin=dict(l=40, r=40, t=80, b=40)
)

fig.write_html("pie_plot.html", include_plotlyjs="cdn")
