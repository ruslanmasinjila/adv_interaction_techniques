import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def display_results():

    ANEES_manual    = np.mean(NEES_manual)
    ANEES_automatic = np.mean(NEES_automatic)
    ANEES_RELATIVE  = ANEES_automatic/ANEES_manual

    # Sample DataFrame
    df = pd.DataFrame({
        'Measured Quantity': ['Active Time', 'Repair Time', 'Targets Acquired', 'Operational Cost',"ANEES"],
        'Automatic Mode': [live_active_time_automatic, total_repair_time_automatic, total_targets_acquired_automatic, cost_for_all_targets_automatic,ANEES_automatic],
        'Manual Mode': [live_active_time_manual, total_repair_time_manual, total_targets_acquired_manual, cost_for_all_targets_manual,ANEES_manual]
    })

    df = df.round(2)

    # Create the figure with 2 subplots (rows=2, columns=1)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.1, subplot_titles=["Table 1: ANEES Results", "Table 2: Additional Results"])

    # Add first table (current table) in the first row
    fig.add_trace(go.Table(
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
    ), row=1, col=1)

    # Sample second DataFrame (could be similar or different)
    df2 = pd.DataFrame({
        'Metric': ['Mean Active Time', 'Mean Repair Time', 'Mean Targets Acquired'],
        'Value': [np.mean(live_active_time_automatic), np.mean(total_repair_time_automatic), np.mean(total_targets_acquired_automatic)]
    })

    df2 = df2.round(2)

    # Add second table in the second row
    fig.add_trace(go.Table(
        header=dict(
            values=list(df2.columns),
            fill_color='lightgreen',  # Header background color
            font=dict(size=16, color='darkgreen'),  # Header font size and color
            align='center',  # Align header text to center
            line_color='darkgreen'  # Border color for header
        ),
        cells=dict(
            values=[df2[col] for col in df2.columns],
            fill_color='white',  # Cell background color
            font=dict(size=14, color='black'),  # Cell font size and color
            align='center',  # Align cell text to center
            line_color='gray'  # Border color for cells
        )
    ), row=2, col=1)

    # Adjust layout (size, title, etc.)
    fig.update_layout(
        title=f"RELATIVE ANEES= ANEES(Automatic Mode)/ANEES(Manual Mode) = {ANEES_RELATIVE:.2f}\n",  # Title
        width=700,  # Width of the figure
        height=800,  # Increased height to accommodate both tables
        margin=dict(l=20, r=20, t=40, b=20)  # Adjust margins to accommodate the title
    )

    # Show the plot
    fig.show()
