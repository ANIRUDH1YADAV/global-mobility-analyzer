from dataclasses import dataclass
import os
from us_visa.constants import *


@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = os.path.join(ARTIFACT_DIR, PIPELINE_NAME)


@dataclass
class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_FEATURE_STORE, "visa_data.csv"
        )
        self.training_file_path = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME
        )
        self.testing_file_path = os.path.join(
            self.data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME
        )
        self.train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.table_name: str = MYSQL_TABLE_NAME


@dataclass
class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(
            training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME
        )
        self.drift_report_file_path = os.path.join(
            self.data_validation_dir,
            DATA_VALIDATION_DRIFT_REPORT,
            DATA_VALIDATION_REPORT_FILE,
        )


@dataclass
class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_transformation_dir = os.path.join(
            training_pipeline_config.artifact_dir, DATA_TRANSFORMATION_DIR_NAME
        )
        self.transformed_train_file_path = os.path.join(
            self.data_transformation_dir, TRANSFORMED_TRAIN_FILE
        )
        self.transformed_test_file_path = os.path.join(
            self.data_transformation_dir, TRANSFORMED_TEST_FILE
        )
        self.transformed_object_file_path = os.path.join(
            self.data_transformation_dir, PREPROCESSOR_OBJECT_FILE
        )


@dataclass
class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.model_trainer_dir = os.path.join(
            training_pipeline_config.artifact_dir, MODEL_TRAINER_DIR_NAME
        )
        self.trained_model_file_path = os.path.join(
            self.model_trainer_dir, MODEL_FILE_NAME
        )
        self.model_config_file_path: str = MODEL_CONFIG_FILE_PATH