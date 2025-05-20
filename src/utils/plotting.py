import matplotlib.pyplot as plt
import seaborn as sns
from src.utils.config import load_config

CONFIG = load_config()

def show_catplot(d, x="hour", y="energy_consumption_(kwh)", col="appliance_type", kind="box",
                 title="Consumo energético por hora del día, por tipo de electrodoméstico"):
    """
    Genera un gráfico categórico (boxplot, barplot, etc.) para visualizar el consumo energético
    por una variable categórica, separado en subgráficos por otra variable.

    Además, imprime la correlación entre las variables `x` e `y` para cada categoría de la columna `col`.

    :param d: DataFrame con los datos que contienen al menos las columnas especificadas.
    :type d: pandas.DataFrame
    :param x: Nombre de la columna que se usará para el eje X. Por defecto, "hour".
    :type x: str
    :param y: Nombre de la columna que se usará para el eje Y. Por defecto, "energy_consumption_(kwh)".
    :type y: str
    :param col: Nombre de la columna por la que se separarán los subgráficos. Por defecto, "appliance_type".
    :type col: str
    :param kind: Tipo de gráfico categórico que se generará (e.g., "box", "violin", "bar", etc.). Por defecto, "box".
    :type kind: str
    :param title: Título principal del gráfico. Por defecto, "Consumo energético por hora del día, por tipo de electrodoméstico".
    :type title: str
    :return: None
    :rtype: NoneType
    """
    data = d.copy()
    data = data.sort_values(by="datetime")
    # Boxplot por hora, separado por tipo de electrodoméstico
    sns.catplot(
        x=x,
        y=y,
        col=col,                                # separa por columna (puedes usar row= también)
        data=data,
        kind=kind,
        palette=CONFIG['plots']["tech_blues"],  # tu paleta personalizada
        col_wrap=3,                             # número de gráficos por fila
        height=4,                               # tamaño del gráfico
        aspect=1.2                              # proporción ancho/alto
    )

    plt.subplots_adjust(top=0.9)
    plt.suptitle(title, color="white")
    plt.show()

    correlations = (
    data.groupby(col)
      .apply(lambda g: g[x].corr(g[y]))
    )
    print(correlations)