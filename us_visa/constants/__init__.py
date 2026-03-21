import os

# ─── Database ────────────────────────────────────────────────────────────────
MYSQL_HOST_KEY        = "MYSQL_HOST"
MYSQL_PORT_KEY        = "MYSQL_PORT"
MYSQL_USER_KEY        = "MYSQL_USER"
MYSQL_PASSWORD_KEY    = "MYSQL_PASSWORD"
MYSQL_DATABASE_KEY    = "MYSQL_DATABASE"
MYSQL_TABLE_NAME      = "visa_applications"   # change to your actual table

# ─── Pipeline ────────────────────────────────────────────────────────────────
PIPELINE_NAME         = "USvisaPipeline"
ARTIFACT_DIR          = "artifact"

# ─── Data Ingestion ──────────────────────────────────────────────────────────
DATA_INGESTION_DIR_NAME        = "data_ingestion"
DATA_INGESTION_FEATURE_STORE   = "feature_store"
DATA_INGESTION_INGESTED_DIR    = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO = 0.2
TRAIN_FILE_NAME                = "train.csv"
TEST_FILE_NAME                 = "test.csv"

# ─── Data Validation ─────────────────────────────────────────────────────────
DATA_VALIDATION_DIR_NAME       = "data_validation"
DATA_VALIDATION_DRIFT_REPORT   = "drift_report"
DATA_VALIDATION_REPORT_FILE    = "report.yaml"
SCHEMA_FILE_PATH               = os.path.join("config", "schema.yaml")

# ─── Data Transformation ─────────────────────────────────────────────────────
DATA_TRANSFORMATION_DIR_NAME   = "data_transformation"
TRANSFORMED_TRAIN_FILE         = "train.npy"
TRANSFORMED_TEST_FILE          = "test.npy"
PREPROCESSOR_OBJECT_FILE       = "preprocessor.pkl"

# ─── Model Training ──────────────────────────────────────────────────────────
MODEL_TRAINER_DIR_NAME         = "model_trainer"
MODEL_FILE_NAME                = "model.pkl"
MODEL_CONFIG_FILE_PATH         = os.path.join("config", "model.yaml")

# ─── AWS / S3 ─────────────────────────────────────────────────────────────────
AWS_S3_BUCKET_NAME             = "us-visa-approval-model"
S3_MODEL_KEY                   = "model-registry/model.pkl"

# ─── Target column ───────────────────────────────────────────────────────────
TARGET_COLUMN                  = "case_status"