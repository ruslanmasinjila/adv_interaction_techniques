import pandas as pd
import plotly.graph_objects as go

# Sample DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
    'Age': [24, 27, 22, 29],
    'Score': [88, 92, 95, 85]
})

# Create a styled table
fig = go.Figure(data=[go.Table(
    header=dict(
        values=list(df.columns),
        fill_color='lightblue',  # Header background color
        font=dict(size=16, color='darkblue'),  # Header font size and color
        align='center',  # Align header text to center
        line_color='darkblue'  # Border color for header
    ),
    cells=dict(
        values=[df[col] for col in df.columns],
        fill_color='white',  # Cell background color
        font=dict(size=14, color='black'),  # Cell font size and color
        align='center',  # Align cell text to center
        line_color='gray'  # Border color for cells
    )
)])

# Adjust figure size and add title
fig.update_layout(
    title="Relative Trust = ANEES(automatic mode)/ANEES(manual mode) = XXX",  # Title
    width=700,  # Width of the table
    height=400,  # Height of the table
    margin=dict(l=20, r=20, t=40, b=20)  # Adjust margins to accommodate the title
)

fig.show()
