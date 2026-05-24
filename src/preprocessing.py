"""
Módulo de processamento e limpeza de dados.
Este arquivo contém funções responsáveis por:
- Padronizar nomes de colunas
- Converter ano acadêmico para inteiro
- Transformar faixas de horas de sono em médias numéricas
- Converter faixas de CGPA em valores médios

Dependências:
    - pandas
"""

import pandas as pd

REQUIRED_COLUMNS = [
    'academic_year',
    'average_sleep',
    'cgpa'
]

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = clean_column_names(df=df)

    validate_columns(df=df)

    df = convert_academic_year(df=df)
    df = convert_sleep_hours(df=df)
    df = convert_cgpa(df=df)

    return df

def validate_columns(df: pd.DataFrame) -> None:
    missing_columns = [ col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        raise ValueError(
            f'Colunas ausentes: {missing_columns}'
        )


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip()

    return df


def calculate_range_mean(series: pd.Series) -> pd.Series:
    return (
        series.str.split('-').apply(lambda values: pd.to_numeric(values, errors='coerce').mean())
    )


def convert_academic_year(df: pd.DataFrame) -> pd.DataFrame:
    df['academic_year'] = df['academic_year'].str.extract(r'(\d+)').astype(int)

    return df


def convert_sleep_hours(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_series = (
        df['average_sleep']
        .str.replace(' hrs', '', case=False, regex=False)
    )

    df['average_sleep'] = calculate_range_mean(cleaned_series)

    return df


def convert_cgpa(df: pd.DataFrame) -> pd.DataFrame:
    df['cgpa'] = calculate_range_mean(df['cgpa'])

    return df
