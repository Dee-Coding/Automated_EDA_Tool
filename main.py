import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.offline as pyo 
import warnings
import pyodbc

# Suppress UserWarnings from Seaborn
warnings.filterwarnings("ignore", category=UserWarning, module="seaborn")

def eda_tool(data):
    # Identify the data types of each column
    data_types = data.dtypes

    # Get the column names for visualization
    selected_columns = input("Enter column names (comma-separated) for visualization: ").split(",")

    # Create visualization dashboards
    dashboards = {}
    
    for column_name in selected_columns:
        column_name = column_name.strip()  # Remove extra spaces
        if column_name in data.columns:
            column_type = data_types[column_name]
            if column_type == "object":
                # Categorical column
                dashboards[column_name] = sns.catplot(
                    data=data,
                    x=column_name,
                    kind="count"
                )
                plt.show()  # For Seaborn plots
            elif column_type == "int64" or column_type == "float64":
                # Numerical column
                dashboards[column_name] = px.histogram(
                    data,
                    x=column_name
                )
                pyo.plot(dashboards[column_name])  # For Plotly plots
            else:
                print(f"Unsupported column type for '{column_name}': {column_type}")
        else:
            print(f"Column '{column_name}' not found in the dataset.")

    return dashboards

if __name__ == "__main__":
    # Get the data source choice
    data_source = input("Choose data source (csv, excel, sql): ").lower()

    # Load data
    data = None
    if data_source == "csv":
        data_file = input("Enter the CSV file path: ")
        data = pd.read_csv(data_file)
    elif data_source == "excel":
        data_file = input("Enter the Excel file path: ")
        data = pd.read_excel(data_file)
    elif data_source == "sql":
        query = input("Enter the SQL query to retrieve data: ")
        conn = pyodbc.connect('DRIVER={SQL Server};' +
                              'SERVER=your_server_name;' +
                              'DATABASE=your_database_name;' +
                              'Trusted_Connection=yes;')
        data = pd.read_sql(query, conn)
        conn.close()

    if data is not None:
        # Perform EDA on the data
        dashboards = eda_tool(data)

        # Print the visualization dashboards
        for column_name, dashboard in dashboards.items():
            print(f"Column: {column_name}")
