import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split

from us_visa.logger import logger
from us_visa.exception import USvisaException
from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.configuration.mysql_connection import MySQLClient


class DataIngestion:
    """
    Responsible for:
      1. Pulling raw data from MySQL into a feature-store CSV.
      2. Splitting into train / test CSV files.
      3. Returning a DataIngestionArtifact with both paths.
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.mysql_client = MySQLClient()
        except Exception as e:
            raise USvisaException(e, sys)

    # ─── Step 1: pull from MySQL ───────────────────────────────────────────

    def export_data_into_feature_store(self) -> pd.DataFrame:
        """
        Reads the visa_applications table from MySQL,
        saves a raw CSV to the feature store directory, and
        returns the DataFrame.
        """
        try:
            logger.info("Exporting data from MySQL → feature store")

            df: pd.DataFrame = self.mysql_client.get_dataframe(
                self.data_ingestion_config.table_name
            )

            # Drop any unnamed index column MySQL might export
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

            feature_store_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_path), exist_ok=True)

            df.to_csv(feature_store_path, index=False)
            logger.info(
                f"Feature store CSV saved → {feature_store_path} "
                f"({df.shape[0]} rows)"
            )
            return df

        except Exception as e:
            raise USvisaException(e, sys)

    # ─── Step 2: train / test split ──────────────────────────────────────

    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        """
        Splits the raw DataFrame into stratified train and test CSVs.
        Uses TARGET_COLUMN for stratification to preserve class ratios.
        """
        try:
            from us_visa.constants import TARGET_COLUMN

            logger.info(
                f"Splitting data — test size: "
                f"{self.data_ingestion_config.train_test_split_ratio}"
            )

            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42,
                stratify=dataframe[TARGET_COLUMN] if TARGET_COLUMN in dataframe.columns else None,
            )

            # Save train
            os.makedirs(
                os.path.dirname(self.data_ingestion_config.training_file_path),
                exist_ok=True,
            )
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False
            )

            # Save test
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False
            )

            logger.info(
                f"Train: {train_set.shape[0]} rows → "
                f"{self.data_ingestion_config.training_file_path}"
            )
            logger.info(
                f"Test : {test_set.shape[0]} rows → "
                f"{self.data_ingestion_config.testing_file_path}"
            )

        except Exception as e:
            raise USvisaException(e, sys)

    # ─── Orchestrator ─────────────────────────────────────────────────────

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Full ingestion flow:
          MySQL → feature_store.csv → train.csv + test.csv
        Returns DataIngestionArtifact with both file paths.
        """
        try:
            logger.info("─── Data Ingestion started ───")

            dataframe = self.export_data_into_feature_store()
            self.split_data_as_train_test(dataframe)

            artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )

            logger.info(f"Data Ingestion artifact: {artifact}")
            logger.info("─── Data Ingestion complete ───")
            return artifact

        except Exception as e:
            raise USvisaException(e, sys)