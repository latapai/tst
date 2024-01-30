import os
import json
from dotenv import load_dotenv 

load_dotenv()

class Configuration:
    """
    Class responsible for handling the configuration of services
    """

    #def __init__(self) -> None:
    #    self.__assert_environment_variables()

    #def __assert_environment_variables(self) -> None:
    #"""
    #Verify that all the required environment variables are defined.
    #    """
     #   required_variables: dict = [
     #       "GENAI_KEY",
     #       "GENAI_ENDPOINT"
     #   ]
     #   for required_variable in required_variables:
     #       assert required_variable in os.environ, f"The environment variable {required_variable} is missing."

    #@property
    def genai_api_key(self) -> str:
        """
        Returns the api key for GENAI
        """
        GENAI_KEY="ZWNCGEZ8RgcnaYNDjx5K_WTXEZtTb8buxOwVUqrC0swd"
        #return os.environ["GENAI_KEY"]
        return GENAI_KEY
    
    #@property
    def genai_api_endpoint(self) -> str:
        """
        Returns the api endpoint for GENAI
        """
        GENAI_ENDPOINT="https://us-south.ml.cloud.ibm.com"
        #return os.environ["GENAI_ENDPOINT"]
        return GENAI_ENDPOINT
 