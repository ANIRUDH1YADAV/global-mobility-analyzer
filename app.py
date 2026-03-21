from us_visa.pipeline.training_pipeline import TrainingPipeline
from us_visa.logger import logger

if __name__ == "__main__":
    logger.info("Starting US Visa Approval — Training Pipeline")
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()