from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidationConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainerConfig,ModelTrainer
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys
if __name__ == '__main__':
    try:
       training_pipelineconfig=TrainingPipelineConfig()
       dataingestionconfig=DataIngestionConfig(training_pipelineconfig)
       data_ingestion=DataIngestion(dataingestionconfig)
       logging.info("Initiate the data ingestion")
       dataingestionartifact=data_ingestion.initiate_data_ingestion()
       print(dataingestionartifact)
       logging.info("Data Initiation Completed")
       data_validation_config=DataValidationConfig(training_pipelineconfig)
       data_validation=DataValidation(dataingestionartifact,data_validation_config)
       logging.info("Initiate the data Validation")
       data_validation_artifact=data_validation.initiate_data_validation()
       logging.info("Data Validation Completed")
       print(data_validation_artifact)
       logging.info("data Transformation started")
       data_transformation_config=DataTransformationConfig(training_pipelineconfig)
       data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
       data_transformation_artifact=data_transformation.initiate_data_transformation()
       print(data_transformation_artifact)
       logging.info("data Transformation completed")

       logging.info("Model Training started ")
       model_trainer_config=ModelTrainerConfig(training_pipelineconfig)
       model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
       model_trainer_artifact=model_trainer.initiate_model_trainer()
       print(model_trainer)
       logging.info("Model Training artifact created")

    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
     