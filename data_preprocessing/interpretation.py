import pandas as pd

def analyze_employee_data(df):
    """
    Analyzes employee data to provide insights.
    :param df: Pandas DataFrame of employee data
    :return: Summary statistics and insights
    """
    insights = {
        "total_employees": len(df),
        "average_age": df['age'].mean() if 'age' in df.columns else None,
        "gender_distribution": df['gender'].value_counts().to_dict() if 'gender' in df.columns else None
    }

    return insights
