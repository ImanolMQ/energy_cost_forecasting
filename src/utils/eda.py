import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from src.utils.config import load_config

CONFIG = load_config()

class DataFrameSummarizer:
    """
    Clase para generar resúmenes estadísticos y visualizaciones automáticas
    de un DataFrame de pandas. Separa el análisis entre variables numéricas y categóricas,
    e incluye detección de outliers, estadísticas descriptivas y gráficos de distribución.

    :param df: DataFrame a resumir.
    :type df: pandas.DataFrame
    :param tech_blues: Paleta de colores personalizada. Si no se proporciona, se cargará desde la configuración.
    :type tech_blues: list, optional
    """
    def __init__(self, df, tech_blues=None):
        self.df = df
        self.numeric_columns = df.select_dtypes(include=[np.number]).columns
        if tech_blues is None:
            self.tech_blues = CONFIG['plots']["tech_blues"]
        else:
            self.tech_blues = tech_blues

    def _is_numeric(self, col):
        """
        Verifica si una columna es numérica.

        :param col: Nombre de la columna.
        :type col: str
        :return: True si es numérica, False si no.
        :rtype: bool
        """
        return col in self.numeric_columns

    def _get_numeric_stats(self, col):
        """
        Calcula estadísticas descriptivas para una columna numérica.

        :param col: Nombre de la columna.
        :type col: str
        :return: Media, desviación estándar y cuartiles (min, 0.25, mediana, 0.75, max).
        :rtype: tuple(float, float, pandas.Series)
        """
        series = self.df[col]
        quantiles = series.quantile([0, 0.25, 0.5, 0.75, 1.0])
        quantiles.index = ['min', '0.25', 'median', '0.75', 'max']
        mean = series.mean()
        std = series.std()
        return mean, std, quantiles

    def _count_outliers_iqr(self, col, factor=1.5):
        """
        Cuenta el número de outliers en una columna numérica usando el método del rango intercuartílico (IQR).

        :param col: Nombre de la columna.
        :type col: str
        :param factor: Multiplicador del IQR para definir límites inferior y superior. Por defecto 1.5.
        :type factor: float
        :return: Número de outliers detectados.
        :rtype: int
        """
        series = self.df[col]
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - factor * iqr
        upper_bound = q3 + factor * iqr
        outliers = series[(series < lower_bound) | (series > upper_bound)]
        return len(outliers)

    def _plot_distribution(self, col, max_unique_cat=10):
        """
        Genera una visualización de la distribución de la variable. Histograma si es numérica, countplot si es categórica.

        :param col: Nombre de la columna a visualizar.
        :type col: str
        :param max_unique_cat: Número máximo de categorías únicas antes de considerar como numérica. Por defecto 10.
        :type max_unique_cat: int
        :return: None
        :rtype: NoneType
        """
        series = self.df[col]

        plt.figure(figsize=(8, 4))
        unique_vals = series.nunique(dropna=True)

        if self._is_numeric(col) and unique_vals > max_unique_cat:
            sns.histplot(series.dropna(), bins=30, kde=True)
            plt.title(f"Histograma de {series.name}")
        else:
            counts = series.value_counts(dropna=False)
            #repeated_palette = (tech_blue_palette * ((counts // len(tech_blue_palette)) + 1))[:len(df)]
            sns.countplot(x=series, order=counts.index[:max_unique_cat], palette=self.tech_blues)
            plt.title(f"Frecuencias de {series.name}")
            plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

    def _summarize_column(self, col, outlier_iqr_factor=1.5, max_unique_cat=20):
        """
        Muestra un resumen detallado de una columna: valores nulos, únicos, estadísticas y visualización.

        :param col: Nombre de la columna a resumir.
        :type col: str
        :param outlier_iqr_factor: Factor para detección de outliers mediante IQR. Por defecto 1.5.
        :type outlier_iqr_factor: float
        :param max_unique_cat: Número máximo de valores únicos para tratar como categórica. Por defecto 20.
        :type max_unique_cat: int
        :return: None
        :rtype: NoneType
        """
        df = self.df.copy()
        print(f"Columna: {col}")
        print("-" * 40)

        series = df[col]
        total = series.shape[0]
        missing = series.isna().sum()
        print(f"Total registros: {total}")
        print(f"Valores perdidos: {missing}")

        unique_vals = series.nunique(dropna=True)

        if self._is_numeric(col) and unique_vals > max_unique_cat:
            mean, std, quantiles = self._get_numeric_stats(col)
            outliers = self._count_outliers_iqr(col, outlier_iqr_factor)

            print(f"Media: {mean:.3f}")
            print(f"Desviación estándar: {std:.3f}")
            print("Quantiles:")
            print(quantiles)
            print(f"Número de outliers (IQR {outlier_iqr_factor}x): {outliers}")
        else:
            print(f"Número de valores únicos: {unique_vals}")
            print("Frecuencias:")
            print(series.value_counts(dropna=False).head(10))

        self._plot_distribution(col, max_unique_cat=max_unique_cat)
        print("\n\n")

    def run_summarize(self):
        """
        Ejecuta el resumen completo del DataFrame para todas sus columnas.

        :return: None
        :rtype: NoneType
        """
        for col in self.df.columns:
            self._summarize_column(col)