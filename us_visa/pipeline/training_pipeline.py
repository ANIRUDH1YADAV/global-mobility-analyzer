import sys
from us_visa.logger import logger
from us_visa.exception import USvisaException
from us_visa.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
)
from us_visa.entity.artifact_entity import DataIngestionArtifact
from us_visa.components.data_ingestion import DataIngestion


class TrainingPipeline:
    """
    Orchestrates the full training pipeline.
    Each stage will be added as we build the project.
    """

    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logger.info("Starting data ingestion stage")
            config = DataIngestionConfig(self.training_pipeline_config)
            ingestion = DataIngestion(data_ingestion_config=config)
            artifact = ingestion.initiate_data_ingestion()
            logger.info(f"Data ingestion artifact: {artifact}")
            return artifact
        except Exception as e:
            raise USvisaException(e, sys)

    def run_pipeline(self):
        try:
            logger.info("══════════ Training Pipeline started ══════════")
            data_ingestion_artifact = self.start_data_ingestion()
            # Next stages will be added: validation → transformation → training
            logger.info("══════════ Training Pipeline complete ══════════")
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys)