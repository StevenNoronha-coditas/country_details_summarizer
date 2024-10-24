import prompts
import os
from groq import Groq

def groq_api_call(prompt_message, country_details):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"),) 
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assisstant that provides summaries bases on the user prompt request"
            },
            {
                "role": "user",
                "content": prompt_message.format(country_details=country_details)
            }
        ],
        model="llama3-8b-8192",
    )
    if response:
        return response.choices[0].message.content
    else:
        print("Error generating summary:", response.status_code, response.text)
        return {"error": "Failed to generate summary"}, 500
    

def generate_summary(country_data):
    country_details = f'''Country Name: {country_data[1]}\n
        GDP: {country_data[2]}\n
        Population: {country_data[3]}\n
        Imports: {country_data[4]}\n
        Exports: {country_data[5]}\n
        Tourists: {country_data[6]}\n
        Surface Area: {country_data[7]}\n''' 
    prompt_message = prompts.summary_prompt
    response = groq_api_call(prompt_message, country_details)
    return response
    
def generate_population_summary(country_data):
    country_details = f'''
        Country Name: {country_data[1]}\n
        Population: {country_data[3]}\n
        Population Growth: {country_data[8]}\n
        Population Density: {country_data[9]}\n
        Sex Ratio: {country_data[10]}\n
        ''' 
    prompt_message = prompts.population_summary_prompt
    response = groq_api_call(prompt_message, country_details)
    return response

def generate_trade_summary(country_data):
    country_details = f'''
        Country Name: {country_data[1]}\n
        GDP: {country_data[2]}\n
        GDP Growth: {country_data[11]}\n
        Currency: {country_data[12]}\n
        Imports: {country_data[4]}\n
        Exports: {country_data[5]}\n
        ''' 
    prompt_message = prompts.trade_prompt
    response = groq_api_call(prompt_message, country_details)
    return response

def generate_import_export_summary(country_data):
    country_details = f'''
        Country Name: {country_data[1]}\n
        GDP: {country_data[2]}\n
        Imports: {country_data[4]}\n
        Exports: {country_data[5]}\n
        ''' 
    prompt_message = prompts.import_export_prompt
    response = groq_api_call(prompt_message, country_details)
    return response