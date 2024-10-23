from flask import Flask, request
import psycopg2
from psycopg2 import pool, OperationalError, DatabaseError
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_NAME = 'country'
DB_USER = 'postgres'
DB_PASS = 'steven123'
DB_HOST = 'localhost'
DB_PORT = '5432'

try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
except OperationalError as e:
    print(f"Error creating connection pool: {e}")

def get_db_connection():
    try:
        conn = connection_pool.getconn()
        return conn
    except Exception as e:
        print(f"Unable to get connection from pool: {e}")
        return None
    
def generate_summary(country_data):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )
    
    country_details = (
        f"Country Name: {country_data['name']}\n"
        f"GDP: {country_data['gdp']}\n"
        f"Population: {country_data['population']}\n"
        f"Imports: {country_data['imports']}\n"
        f"Exports: {country_data['exports']}\n"
        f"Tourists: {country_data['tourists']}\n"
        f"Surface Area: {country_data['surface_area']}\n"
    )

    prompt_message = '''I am going to provide you details about a country. 
        Based on the details provided, please generate a summary about that country. Based on the trade details provided \n\n
        {country_details}'''
    

    response = client.chat.completions.create(
        messages=[
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

@app.route('/createtable')
def create_table():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed.", 500

    print('Connection established with database')

    try:
        with conn.cursor() as cur:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS public.country_details (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                gdp DECIMAL(15, 2),
                population BIGINT,
                imports DECIMAL(15, 2),
                exports DECIMAL(15, 2),
                tourists BIGINT,
                surface_area DECIMAL(10, 2)
            );
            '''
            print("Executing query to create table...")
            cur.execute(create_table_query)
            conn.commit()  
            print("Table created successfully.")
            return 'Table created'
    except DatabaseError as e:
        print(f"Database error: {e}")
        return "Error executing query.", 500  
    finally:
        connection_pool.putconn(conn)


import requests

@app.route('/filltable')
def fill_table():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed.", 500

    print('Connection established with database')

    api_url = 'https://api.api-ninjas.com/v1/country?name='
    headers = {'X-Api-Key': 'PrBzs9ThknmxdWzZql/OBQ==CsnXC111sDLfvgPp'}
    
    try:
        with conn.cursor() as cur:
            response = requests.get(api_url, headers=headers)
            if response.status_code != requests.codes.ok:
                return f"Error fetching data: {response.status_code}", 500
            
            countries = response.json()
            print(f"Fetched {len(countries)} countries")
            insert_query = '''
            INSERT INTO public.country_details 
            (name, gdp, population, imports, exports, tourists, surface_area) 
            VALUES (%s, %s, %s, %s, %s, %s, %s);
            '''

            for country in countries:
                name = country.get('name')
                gdp = country.get('gdp')
                population = country.get('population')
                imports = country.get('imports')
                exports = country.get('exports')
                tourists = country.get('tourists')
                surface_area = country.get('surface_area')  
                cur.execute(insert_query, (name, gdp, population, imports, exports, tourists, surface_area))

            conn.commit()  
            print("Data inserted successfully.")
            return 'Table filled with data from external API', 201
    except DatabaseError as e:
        print(f"Database error: {e}")
        return "Error executing query.", 500  
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "An unexpected error occurred.", 500
    finally:
        connection_pool.putconn(conn)


@app.route('/summary', methods=['GET'])
def summary():
    country_name = request.args.get('name')  
    print(country_name)
    if not country_name:
        return "Country name is required.", 400

    conn = get_db_connection()
    if conn is None:
        return "Database connection failed.", 500

    try:
        with conn.cursor() as cur:
            query = '''
            SELECT * FROM public.country_details WHERE name ILIKE %s;
            '''
            cur.execute(query, (country_name,))
            result = cur.fetchone()

            if result is None:
                return f"No data found for country: {country_name}", 404
            country_data = {
                "id": result[0],
                "name": result[1],
                "gdp": result[2],
                "population": result[3],
                "imports": result[4],
                "exports": result[5],
                "tourists": result[6],
                "surface_area": result[7]
            }
            return generate_summary(country_data), 200
    except DatabaseError as e:
        print(f"Database error: {e}")
        return "Error executing query.", 500  
    finally:
        connection_pool.putconn(conn)


@app.route('/')
def index():
    return "Country data web api, use the the api's /createtable or /accessdata"

if __name__ == '__main__':
    app.run(debug=True)