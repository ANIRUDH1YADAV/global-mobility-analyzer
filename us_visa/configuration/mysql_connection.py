import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from us_visa.logger import logger
from us_visa.exception import USvisaException
from us_visa.constants import (
    MYSQL_HOST_KEY,
    MYSQL_PORT_KEY,
    MYSQL_USER_KEY,
    MYSQL_PASSWORD_KEY,
    MYSQL_DATABASE_KEY,
)

load_dotenv()


class MySQLClient:
    """
    Manages MySQL connection using SQLAlchemy.
    Credentials are read from environment variables / .env file.
    """

    _engine = None  # class-level singleton engine

    def __init__(self):
        try:
            host     = os.getenv(MYSQL_HOST_KEY, "localhost")
            port     = os.getenv(MYSQL_PORT_KEY, "3306")
            user     = os.getenv(MYSQL_USER_KEY)
            password = os.getenv(MYSQL_PASSWORD_KEY)
            database = os.getenv(MYSQL_DATABASE_KEY)

            if not all([user, password, database]):
                raise ValueError(
                    "MYSQL_USER, MYSQL_PASSWORD, and MYSQL_DATABASE "
                    "must be set in your .env file."
                )

            connection_url = (
                f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
            )

            if MySQLClient._engine is None:
                MySQLClient._engine = create_engine(
                    connection_url,
                    pool_pre_ping=True,       # auto-reconnect on stale connections
                    pool_size=5,
                    max_overflow=10,
                )
                logger.info(
                    f"MySQL engine created — host={host}, db={database}"
                )

            self.engine = MySQLClient._engine

        except Exception as e:
            raise USvisaException(e, sys)

    def get_dataframe(self, table_name: str) -> pd.DataFrame:
        """
        Reads an entire table into a pandas DataFrame.

        Args:
            table_name: Name of the MySQL table to read.

        Returns:
            pd.DataFrame with all rows from the table.
        """
        try:
            logger.info(f"Fetching data from table: `{table_name}`")
            query = f"SELECT * FROM `{table_name}`"
            df = pd.read_sql(query, con=self.engine)
            logger.info(
                f"Fetched {df.shape[0]} rows × {df.shape[1]} columns "
                f"from `{table_name}`"
            )
            return df
        except Exception as e:
            raise USvisaException(e, sys)

    def get_dataframe_from_query(self, query: str) -> pd.DataFrame:
        """
        Runs a custom SQL query and returns the result as a DataFrame.

        Args:
            query: Any valid SELECT statement.

        Returns:
            pd.DataFrame with query results.
        """
        try:
            logger.info(f"Running custom query: {query[:120]}...")
            df = pd.read_sql(query, con=self.engine)
            logger.info(f"Query returned {df.shape[0]} rows")
            return df
        except Exception as e:
            raise USvisaException(e, sys)

    def test_connection(self) -> bool:
        """Verifies the database connection is alive."""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("MySQL connection test: OK")
            return True
        except Exception as e:
            raise USvisaException(e, sys)