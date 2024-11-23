
    ANEES_manual    = np.mean(NEES_manual)
    ANEES_automatic = np.mean(NEES_automatic)
    ANEES_RELATIVE  = ANEES_automatic/ANEES_manual


    # Sample DataFrame
    df = pd.DataFrame({
        'Measured Quantity': ['Active Time', 'Repair Time / Active Time', 'Targets Acquired / Active Time', 'Operational Cost / Active Time',"ANEES"],
        'Automatic Mode': [live_active_time_automatic, 
                           total_repair_time_automatic/live_active_time_automatic, 
                           total_targets_acquired_automatic/live_active_time_automatic, 
                           cost_for_all_targets_automatic/live_active_time_automatic,
                           ANEES_automatic],
        'Manual Mode': [live_active_time_manual, 
                        total_repair_time_manual/live_active_time_manual, 
                        total_targets_acquired_manual/live_active_time_manual, 
                        cost_for_all_targets_manual/live_active_time_manual,
                        ANEES_manual]
    })

    df = df.round(2)



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

    trust_level = ""
    if(ANEES_RELATIVE>1):
        trust_level = " ( OVERTRUSTING ROBOT)"
    if(ANEES_RELATIVE > 0 and ANEES_RELATIVE < 1):
        trust_level = " ( UNDERTRUSTING ROBOT)"


    fig.update_layout(
        title="RELATIVE ANEES =" + str(round(ANEES_RELATIVE,5)) + f"{trust_level}",
        width=700,  # Width of the table
        height=400,  # Height of the table
        margin=dict(l=25, r=25, t=40, b=20)  # Adjust margins to accommodate the title
    )

    fig.show()
