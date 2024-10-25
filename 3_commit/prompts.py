summary_prompt = '''I am going to provide you with detailed information about a country. 
Based on this information, please generate an in-depth summary that covers various aspects of the country. 

The summary should include:
1. Key facts and figures (e.g., population, area, GDP)
2. Economic indicators and trends
3. Any other relevant details

Ensure the summary is elaborative, consisting of at least 10-15 lines, and formatted in numbered bullet points for clarity. Here are the details:\n\n{country_details}'''

population_summary_prompt = '''
Consider you are a population analyst, I will provide you with detailed information regarding the population of a country. 
Using this data, generate a comprehensive summary that focuses on population dynamics. 
The summary should be detailed, at least 10-15 lines long, and presented in numbered bullet points. Here are the details:\n\n{country_details}'''


trade_prompt = '''I will provide you with information related to the trade details of a country. 
Using the provided data, please generate a detailed summary that emphasizes trade aspects. 

Your summary should cover:
1. Major exports and imports
2. Trade balance and its implications
3. Trends in trade over the past years

Ensure the summary is elaborative, at least 10-15 lines long, and formatted in numbered bullet points. Here are the details:\n\n{country_details}'''


trade_prompt = '''I will provide you with information related to the trade details of a country. 
Using the provided data, please generate a detailed summary that emphasizes trade aspects.
Ensure the summary is elaborative, at least 10-15 lines long, and formatted in numbered bullet points. Here are the details:\n\n{country_details}'''
