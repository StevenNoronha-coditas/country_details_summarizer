summary_prompt = '''I am going to provide you details about a country. 
        Based on the details provided, please generate a summary about that country.\n\n
        {country_details}'''

population_summary_prompt = '''I am going to provide you details related to the population of a country,
        Using the given data, i need you to generate a summary that centers around the population data
        {country_details}'''

trade_prompt = '''I am going to provide you details related to the trade details of a country,
        Using the given data, i need you to generate a summary that centers around the trades details
        {country_details}'''

import_export_prompt = '''I am going to provide you details related to the export and import details of a country,
        Using the given data, i need you to generate a summary that centers around the import export details
        {country_details}
'''