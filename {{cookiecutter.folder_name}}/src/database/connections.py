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

from contextlib import contextmanager

import pandas as pd
import duckdb
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import connection


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
        return self.conn(consulta).df()


class Postgres:
    def __init__(
        self,
        host,
        user,
        password,
        port,
        dbname,
        maxconn=1,
        minconn=1,
        **kwargs,
    ):
        self.host = host
        self.port = port
        self.password = password
        self.user = user
        self.database = dbname
        self.maxconn = maxconn
        self.minconn = minconn
        self.pool = self._create_pool()

    def _create_pool(self) -> SimpleConnectionPool:
        return SimpleConnectionPool(
            minconn=self.minconn,
            maxconn=self.maxconn,
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port,
        )

    @contextmanager
    def _get_connection(self) -> connection:
        conn = self.pool.getconn()
        try:
            yield conn
        finally:
            self.pool.putconn(conn)

    def __call__(self, query: str) -> pd.DataFrame:
        """Ejecuta una consulta y devuelve un DataFrame de Polars."""
        try:
            with self._get_connection() as conn:
                return pd.read_sql(
                    query,
                    conn,
                )
        except Exception as e:
            print(f"Error ejecutando query: {e}")
            raise
