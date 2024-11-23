import matplotlib.pyplot as plt
import pandas as pd

# Example DataFrames
data1 = {'Column A': ['Short', 'Medium Text', 'A very long text entry'], 
         'Column B': [4, 5, 6]}
data2 = {'X': [7, 8, 9], 
         'Y': ['Small', 'Medium', 'Another long text entry']}

performance_variables = pd.DataFrame(data1)
system_variables = pd.DataFrame(data2)

# Create subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns

# Function to style a table
def style_table(ax, dataframe, title):
    # Turn off axis
    ax.axis('off')

    # Create table
    table = ax.table(
        cellText=dataframe.values,
        colLabels=dataframe.columns,
        loc='center',
        cellLoc='center',  # Center align text
    )

    # Style table
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=list(range(len(dataframe.columns))))  # Dynamic column width

    # Add padding to cells
    for (row, col), cell in table.get_celld().items():
        cell.PAD = 0.05  # Add padding between cells
        cell.set_height(0.1)  # Increase cell height for padding
        if row == 0:  # Header row
            cell.set_text_props(weight='bold')  # Bold header text
            cell.set_facecolor('#5fba7d')  # Header background color
            cell.set_text_props(color='white')  # Header text color
        else:
            cell.set_facecolor('#f5f5f5')  # Light gray for data rows

    # Set title
    ax.set_title(title, fontweight='bold', fontsize=14)

# Plot the first DataFrame
style_table(axes[0], performance_variables, 'DataFrame 1')

# Plot the second DataFrame
style_table(axes[1], system_variables, 'DataFrame 2')

# Adjust layout
plt.tight_layout()
plt.show()
