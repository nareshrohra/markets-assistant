from flask import Flask, request, jsonify
import pandas

from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.agents import create_csv_agent
from pathlib import Path
import os
import pandas as pd

input_data_base_path = "../../_data/processed/"

def ping():
  return 'Pong!', 200
  

def ask():
  #try:
    request_body = request.json
    prompt = request_body["question"]
    datasetType = request_body["datasetType"]
    datasetName = request_body["datasetName"]
    
    answer = get_answer(prompt, datasetType, datasetName)
    return answer, 200
  #except Exception as ex:
  #  return str(ex), 500

def get_answer(prompt, datasetType, datasetName):
  data_file_path = os.path.join(input_data_base_path, datasetType, datasetName + ".csv")
  agent = create_csv_agent(OpenAI(temperature=0), data_file_path, verbose=True)
  print('Trying to answer: ' + prompt)
  context = "Answer should be embedded in html tags. Use column 'Date' for date."
  return agent.run(context + " " + prompt)
  
