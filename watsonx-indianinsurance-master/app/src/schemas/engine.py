# Import streamlit for the UI 
import streamlit as st
import os, getpass
from pandas import read_csv
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models import Model
model_id = ModelTypes.FLAN_UL2

from src.schemas import Configuration
#from genai.schemas import ModelType, GenerateParams
#from genai.model import Credentials, Model
import requests
import json
import re

class Engine:
    
    def __init__(self):
        self._config = Configuration()
        
        with open("app/src/assets/data/data.json", "r") as file:
            json_config = json.load(file)
        self.claims = json_config["claims"]
        
    def __parse_enumerated_list(self, string):
        try:
            pattern = r'\d+\.\s+'
            string = re.sub(pattern, '####', string)
            items = string.split('####')
            return [item.strip() for item in items if item != '']
        except Exception as e:
            return None

    def __parse_entities(self, string):
        try:
            entities = {"Car Details": "Not Found", "Location": "Not Found", "Date": "Not Found", "Time of Incident": "Not Found"}
            lines = string.split(';')
            print("The string is :", string)
            print(lines)
            for line in lines:
                parts = line.split(':')
                print (parts)
                # if len(parts) != 2:
                #     raise Exception("Invalid format: ", string)
                key = parts[0].strip()
                value = parts[1].strip()
                entities[key] = value
                #word="Location"
                #if key=="Car Details":
                #   entities[key] = entities[key].replace(word, "")
                print(entities)
            return entities
        except Exception as e:
            return None

    def query_bam_entities(self, prompt: str) -> str:
        
        try:
            prompt_input = """Please provide Output as given below from the given paragraph.Read this Insurance claim description and extract the Car make & model, location of the incident like street,city,state,town and date time if there is any mentioned. If you don't find these details in the description, please fill it as Not Found.
            I am writing this letter to file a report for a car accident in which I was involved on the 5th of February. I was driving my Hyundai i10, 9678 in Bandra when a Honda city, 7845 came in a rush and hit me from behind. My car was totally smashed and damaged brutally. The Honda city managed to escape from the scene immediately, and I could not hold the driver at that moment. But I managed to take a note of his car number which I have stated above.

            Car Details: Hyundai i10, 9678;Location: Bandra;Date: 5th February 2023;Time of Incident: Not Found

            A car incident occurred on Jan 1st 2023 at 5pm at the intersection of woodbridge. The insured vehicle, a Honda civic, was hit by another vehicle that ran a red light 

            Car Details: Honda Civic;Location: Woodbridge;Date: Jan 1st 2023;Time of Incident: 5pm

            The insured vehicle, a Ford RAM, was stolen from Boston on Dec 2nd 2022. The vehicle was parked in a secure parking lot, and all necessary precuations were taken, such as locking the doors and activating the alarm system.

            Car Details: Ford RAM;Location: Boston;Date: Dec 2nd 2022;Time of Incident: Not Found

            The insured vehicle, a Tesla model X, was vandalized on March 23rd while parked in front of the insured's residence on Magador street. The vandalism included scratched paint, broken windows and damage to side mirrors.

            Car Details: Tesla Model X;Location: Magador street;Date: March 23rd;Time of Incident: Not Found

            The insured vehicle, caught fire on April 1st due to a mechanical malfunction. The fire resulted in significant damage to the vehicle, including damage to the engine, interior and exterior. Hence the fire service was immediately contacted by the insurer.

            Car Details: Not Found;Location: Not Found;Date: April 1st 2023;Time of Incident: Not Found

            The insured vehicle,was parked outside during a severe hailstorm. As a result the vehicle suffered extensive damage, including dents on the roof,hood and trunk. The insured promptly reported the incident and is filing a claim hence.

            Car Details: Not Found;Location: Parked outside;Date: Not Found;Time of Incident: Not Found
            
            """
            
            #project_id =  "56483d15-09e8-403e-93e5-bb503d73b57f"
            project_id = "afa20442-39b0-4d8a-8f0e-d770c63fbdd2"
            model_id="google/flan-ul2"
            #model_id="meta-llama/llama-2-70b-chat"
            parameters = {
            GenParams.MAX_NEW_TOKENS: 10,
            GenParams.DECODING_METHOD: "greedy",
            GenParams.TEMPERATURE: 0.7,
            GenParams.TOP_P: 1,
            GenParams.TOP_K: 50,
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.MAX_NEW_TOKENS:50
            }
            credentials = {
               "url": "https://us-south.ml.cloud.ibm.com",
               "apikey": "ZWNCGEZ8RgcnaYNDjx5K_WTXEZtTb8buxOwVUqrC0swd"
            }
                     
            model = Model(
            model_id=model_id,
            params=parameters,
            credentials=credentials,
            project_id=project_id)
            response=model.generate_text(prompt=" ".join([prompt_input, prompt]))
            result=response
            print("this is ",response)
        except Exception as e:
            print(e)
            result = None
        return result
    
    def query_bam_next_steps(self, prompt: str) -> str:
        try:
            prompt_input= """Act as a Auto insurance Claim manager and suggest the next steps and suggest the next  steps for this accident claim.
A car accident occurred on Jan 1st, 2023 at 5pm at the intersection of woodbridge. The insured vehicle, a Honda Civic, was hit by another vehicle that ran a red light. The insured driver, John, was driving within the speed limit and following all traffic rules. The accident resulted in significant damage to the insured vehicle, including a broken bumper and damaged front fender. There were no injuries reported. The insured is filing a claim for the repairs and any necessary medical expenses.
1. Make a claim with your insurance company
2. Provide any paperwork required to substantiate the claim.
3. Contact the insurance company and the covered driver. Keep track of the claim's progress. If more information is required, contact the insured.When all parties have agreed on a settlement, the claim is closed.

The insured vehicle, a Ford RAM, was stolen from Boston on Dec 2nd 2022. The vehicle was parked in a secure parking lot, and all necessary precautions were taken, such as locking the doors and activating the alarm system. The insured immediately reported the theft to the police and obtained a police report. The vehicle had comprehensive insurance coverage, and the insured is filing a claim for the stolen vehicle, including its estimated value, accessories, and personal belongings that were inside the vehicle at the time of theft.
1. Contact the police to file a police report.
2. Provide the insurance company with the police report
3. Provide the insurance company with any additional information that may be necessary to process the claim
4. Wait for the insurance company to contact you regarding the claim.

The insured vehicle, a Tesla model X, was vandalized on March 23rd, 2023 while parked in front of the insured's residence on Magador Street. The vandalism included scratched paint, broken windows, and damage to the side mirrors. The insured promptly reported the incident to the police and obtained a police report. The insured is filing a claim for the repairs and any necessary replacement parts. The estimated cost of repairs has been assessed by a reputable auto repair shop.
1. Verify the insured's policy coverage to ensure that it includes coverage for vandalism and the necessary repairs.
2. Review the provided information regarding the vandalism incident, including the date of occurrence, location(Magador Street), and the description of the damages.
3. Request the insured to provide the police report documenting the vandalism incident. The police report will serve as crucial evidence and help establish the validity of the claim.
4. Engage a reputable auto repair shop to assess the damages and provide an estimate for the necessary repairs and replacement parts. Consider obtaining multiple estimates to ensure accuracy and fairness.
5. Carefully review all supporting documents, including the police report and the repair shop's estimate. Verify the estimated cost of repairs and validate that the damages align with the incident described by the insured.
6. Maintain regular communication with the insured, providing updates on the claim process and addressing any questions or concerns they may have. Keep them informed about the progress and expected timeline for claim resolution.

The insured vehicle, was parked outside during a severe hailstorm. As a result, the vehicle suffered extensive hail damage, including dents on the roof, hood, and trunk. The insured promptly reported the incident and is filing a claim for the necessary repairs. The estimated cost of repairs has been assessed by an authorized auto repair shop.
1. Gather missing details like, Car Make and Model, where the car had been parked and location or street details.
2. Verify the insured's policy coverage to ensure that it includes coverage for hail damage and the necessary repairs.
3. Assess the information provided about the hail damage incident. Take note of the extent of the damage, including dents on the roof, hood, and trunk of the insured vehicle. Determine if there are any other damages caused by the hailstorm.
4. Engage an authorized auto repair shop to assess the extent of the hail damage and provide an estimate for the necessary repairs.
5. Carefully review the estimate provided by the authorized auto repair shop. Verify that the estimated cost of repairs is reasonable and necessary for restoring the vehicle to its pre-damage condition.
6. Maintain communication with the insured, keeping them informed about the claim process and any required steps. """

            project_id =  "afa20442-39b0-4d8a-8f0e-d770c63fbdd2"
            model_id="google/flan-ul2"
            parameters = {
            #GenParams.MAX_NEW_TOKENS: 10,
            GenParams.DECODING_METHOD: "greedy",
            GenParams.TEMPERATURE: 0.7,
            GenParams.TOP_P: 1,
            GenParams.TOP_K: 50,
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.MAX_NEW_TOKENS:300,
            GenParams.RANDOM_SEED:1050
            }
            credentials = {
               "url": "https://us-south.ml.cloud.ibm.com",
               "apikey": "ZWNCGEZ8RgcnaYNDjx5K_WTXEZtTb8buxOwVUqrC0swd"
            }
                     
            model = Model(
            model_id=model_id,
            params=parameters,
            credentials=credentials,
            project_id=project_id)
            response=model.generate_text(prompt=" ".join([prompt_input, prompt]))
            result=response
            print(response)
        except Exception as e:
            print(e)
            result = None
        return result
    
    def query_bam_summary(self, prompt: str) -> str:
        try:
            prompt_input="""The following document is a transcript from an insurance customer representative. Read the document and then write a short 1 paragraph summary.

Input:
A car accident occurred on Jan 1st, 2023 at 5pm at the intersection of woodbridge. The insured vehicle, a Honda Civic, was hit by another vehicle that ran a red light. The insured driver, John, was driving within the speed limit and following all traffic rules. The accident resulted in significant damage to the insured vehicle, including a broken bumper and damaged front fender. There were no injuries reported. The insured is filing a claim for the repairs and any necessary medical expenses.
A car accident at Woodbridge intersection involving a Honda Civic insured by John occurred due to another vehicle running a red light, resulting in significant damage to the insured vehicle, but no injuries. A claim is being filed for repairs and potential medical expenses.

Input:
The insured vehicle, a Ford RAM, was stolen from Boston on Dec 2nd 2022. The vehicle was parked in a secure parking lot, and all necessary precautions were taken, such as locking the doors and activating the alarm system. The insured immediately reported the theft to the police and obtained a police report. The vehicle had comprehensive insurance coverage, and the insured is filing a claim for the stolen vehicle, including its estimated value, accessories, and personal belongings that were inside the vehicle at the time of theft.
A Ford RAM insured vehicle was stolen from a secure parking lot in Boston on December 2nd, 2022, despite taking necessary precautions, and the insured is filing a comprehensive insurance claim for the stolen vehicle, its estimated value, accessories, and personal belongings inside.

Input:
The insured vehicle, a Tesla model X, was vandalized on march 23rd while parked in front of the insured's residence on Magador Street. The vandalism included scratched paint, broken windows, and damage to the side mirrors. The insured promptly reported the incident to the police and obtained a police report. The insured is filing a claim for the repairs and any necessary replacement parts. The estimated cost of repairs has been assessed by a reputable auto repair shop.
A Tesla Model X insured vehicle was vandalized on March 23rd, with damage including scratched paint, broken windows, and damaged side mirrors while parked in front of the insured's residence on Magador Street. The insured reported the incident to the police, obtained a police report, and is filing a claim for repairs and necessary replacement parts based on the assessed cost by a reputable auto repair shop.

Input:
The insured vehicle, was parked outside during a severe hailstorm. As a result, the vehicle suffered extensive hail damage, including dents on the roof, hood, and trunk. The insured promptly reported the incident and is filing a claim for the necessary repairs. The estimated cost of repairs has been assessed by an authorized auto repair shop.
Insured vehicle sustained extensive hail damage while parked outside during a severe hailstorm, prompting a claim for necessary repairs with an assessed cost by an authorized auto repair shop.

Input:
While driving on Anthony Street on 1st June, the insured vehicle, a BMW Q1, collided with a large animal (e.g., deer) that suddenly crossed the road. The accident resulted in damage to the front bumper, grille, and headlights. The insured promptly reported the incident and is filing a claim for the repairs. Additionally, the insured sought medical attention for any potential injuries resulting from the collision.
Insured BMW Q1 collided with a large animal on Anthony Street, resulting in damage to the front bumper, grille, and headlights. Claim filed for repairs, and insured sought medical attention for potential injuries.

Input:
The insured vehicle, caught fire on april 1st due to a mechanical malfunction. The fire resulted in significant damage to the vehicle, including damage to the engine, interior, and exterior. The insured immediately contacted the fire department, and the incident was reported to the police. The insured is filing a claim for the repairs and is providing the fire department report as evidence of the fire incident.
Insured vehicle caught fire on April 1st due to a mechanical malfunction, resulting in significant damage to the engine, interior, and exterior. Claim filed for repairs,supported by fire department report as evidence."""

            project_id =  "afa20442-39b0-4d8a-8f0e-d770c63fbdd2"
            model_id="google/flan-ul2"
            parameters = {
            #GenParams.MAX_NEW_TOKENS: 10,
            GenParams.DECODING_METHOD: "sample",
            GenParams.TEMPERATURE: 0.7,
            GenParams.TOP_P: 1,
            GenParams.TOP_K: 50,
            GenParams.MIN_NEW_TOKENS: 5,
            GenParams.MAX_NEW_TOKENS:100,
            GenParams.RANDOM_SEED:1050,
            GenParams.REPETITION_PENALTY:2
            }
            credentials = {
               "url": "https://us-south.ml.cloud.ibm.com",
               "apikey": "ZWNCGEZ8RgcnaYNDjx5K_WTXEZtTb8buxOwVUqrC0swd"
            }
                     
            model = Model(
            model_id=model_id,
            params=parameters,
            credentials=credentials,
            project_id=project_id)
            response=model.generate_text(prompt=" ".join([prompt_input, prompt]))
            result=response
            print(response)
        except Exception as e:
            print(e)
            result = None
        return result

    def query_bam(self, prompt: str):
        entities = self.query_bam_entities(prompt)
        if entities is not None:
            entities = self.__parse_entities(entities)
        next_steps = self.query_bam_next_steps(prompt)
        if next_steps is not None:
            next_steps = self.__parse_enumerated_list(next_steps)
        summary = self.query_bam_summary(prompt)
        return entities, next_steps, summary
    
    def query_entities(self, prompt: str):
        print("CALLED HERE")
        entities = self.query_bam_entities(prompt)
        if entities is not None:
            entities = self.__parse_entities(entities)
        return entities
    
    def query_summary(self, prompt: str):
        summary = self.query_bam_summary(prompt)
        return summary
    
    def query_next_steps(self, prompt: str):
        next_steps = self.query_bam_next_steps(prompt)
        if next_steps is not None:
            next_steps = self.__parse_enumerated_list(next_steps)
        return next_steps