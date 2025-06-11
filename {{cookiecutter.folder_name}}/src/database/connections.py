"""Modulo donde se manejan las conecciones a las bases de datos.

En este módulo se manejan todas las conecciones a las bases de datos
mediante código para establecer estas conecciones de manera agnostica
en el desarrollo.

Las conecciones soportadas de momento son:


- [x] DuckDB
- [ ] Postgres
- [ ] Mysql

> [!NOTE] Manejar estas conecciones mediante Hydra para garantiza la
> horizontabilidad.

"""

__docformat__ = "google"


class DuckDB:
    """Coneccion a la base de datos local de DuckDB.

    Esta clase permite establecer coneccion a la base de datos local
    de duckdb del proyecto.

    Args:
        path (str): String que representa la ubicación de la base de
            datos
    """

    def __init__(self, path: str = ":memory:", **kwargs):
        """Inicialización de la clase.

        Esta clase permite establecer coneccion a la base de datos
        local de duckdb del proyecto.

        Args:
            path (str): String que representa la ubicación de la base
                de datos.
        """

        import duckdb

        self.conn = duckdb.connect(path)

    def __call__(self, consulta):
        """Retorna un pandas dataframe dada la consulta SQL.

        Args:
            consulta (str): Consulta SQL
        Returns:
            instancia de pandas.DataFrame con la salida
        """
        return self.conn(consulta).df()
