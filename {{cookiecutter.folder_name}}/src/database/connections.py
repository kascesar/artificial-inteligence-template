"""Modulo donde se manejan las conecciones a las bases de datos.

En este módulo se manejan todas las conecciones a las bases de datos
mediante código para establecer estas conecciones de manera agnostica
en el desarrollo.

Las conecciones soportadas de momento son:


- [x] DuckDB
- [x] Postgres
- [ ] Mysql

> [!NOTE] Manejar estas conecciones mediante Hydra para garantiza la
> horizontabilidad.

"""

__docformat__ = "google"


import pandas as pd
import duckdb


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

        self.conn = duckdb.connect(path)

    def __call__(self, consulta):
        """Retorna un pandas dataframe dada la consulta SQL.

        Args:
            consulta (str): Consulta SQL
        Returns:
            instancia de pandas.DataFrame con la salida
        """
        return self.conn.sql(consulta).df()


class Postgres:
    def __init__(
        self,
        host,
        user,
        password,
        port,
        dbname,
        alias="remote_pg",
    ):
        self.alias = alias
        self.conn = duckdb.connect(database=":memory:")
        self.conn.execute("INSTALL postgres;")
        self.conn.execute("LOAD postgres;")

        self.conn.execute(
            f"""
            CREATE OR REPLACE SECRET {alias}_secret (
                TYPE postgres,
                HOST '{host}',
                PORT {port},
                DATABASE '{dbname}',
                USER '{user}',
                PASSWORD '{password}'
            );
        """
        )
        self.conn.execute(
            f"""
            ATTACH '' AS {alias} (TYPE postgres, SECRET {alias}_secret);
        """
        )

    def __call__(self, query: str) -> pd.DataFrame:
        """
        Ejecuta una consulta SQL sobre la base adjunta.

        Usa `{alias}.{schema}.tabla` para referenciar tablas.
        """
        try:
            return self.conn.sql(query).df()
        except Exception as e:
            print(f"Error ejecutando query: {e}")
            raise
