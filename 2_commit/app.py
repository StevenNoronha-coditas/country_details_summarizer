from flask import Flask, request
import psycopg2, os
from psycopg2 import pool, OperationalError, DatabaseError
from dotenv import load_dotenv
import summary_generator
load_dotenv()

app = Flask(__name__)

try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
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
    
@app.route('/createtable')
def create_table():
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed.", 500

    print('Connection established with database')

    try:
        with conn.cursor() as cur:
            create_table_query = '''
            CREATE TABLE IF NOT EXISTS public.country_details_extended (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                gdp DECIMAL(15, 2),
                population BIGINT,
                imports DECIMAL(15, 2),
                exports DECIMAL(15, 2),
                tourists BIGINT,
                surface_area DECIMAL(10, 2),
                pop_growth DECIMAL(10, 2),
                pop_density DECIMAL(10, 2),
                sex_ratio DECIMAL(10, 2),
                gdp_growth DECIMAL(10, 2),
                currency VARCHAR(20));
            '''
            cur.execute(create_table_query)
            conn.commit()  
            return 'Table created'
    except DatabaseError as e:
        print(f"Database error: {e}")
        return "Error executing query.", 500  
    finally:
        connection_pool.putconn(conn)


import requests

@app.route('/filltable', methods=['GET'])
def fill_table():
    country_name = request.args.get('name')  if request.args.get('name') else ""
    conn = get_db_connection()
    if conn is None:
        return "Database connection failed.", 500

    print('Connection established with database')

    api_url = 'https://api.api-ninjas.com/v1/country?name=' + country_name
    headers = {'X-Api-Key': os.environ.get("NINJA_API_KEY")}
    
    try:
        with conn.cursor() as cur:
            response = requests.get(api_url, headers=headers)
            if response.status_code != requests.codes.ok:
                return f"Error fetching data: {response.status_code}", 500
            
            countries = response.json()
            print(f"Fetched {len(countries)} countries")
            insert_query = '''
            INSERT INTO public.country_details_extended 
            (name, gdp, population, imports, exports, tourists, surface_area, pop_growth, pop_density, sex_ratio, gdp_growth, currency) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            '''

            for country in countries:
                name = country.get('name')
                gdp = country.get('gdp')
                population = country.get('population')
                imports = country.get('imports')
                exports = country.get('exports')
                tourists = country.get('tourists')
                surface_area = country.get('surface_area')  
                pop_growth = country.get('pop_growth')  
                pop_density = country.get('pop_density')  
                sex_ratio = country.get('sex_ratio')  
                gdp_growth = country.get('gdp_growth')  
                currency = country.get('currency').get("name")
                cur.execute(insert_query, (name, gdp, population, imports, exports, tourists, surface_area, pop_growth, pop_density, sex_ratio, gdp_growth, currency))

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
    topic = request.args.get('topic')  if request.args.get('topic') else "SUMARRY"
    if not country_name:
        return "Country name is required.", 400

    conn = get_db_connection()
    if conn is None:
        return "Database connection failed.", 500

    try:
        with conn.cursor() as cur:
            query = '''
            SELECT * FROM public.country_details_extended WHERE name ILIKE %s;
            '''
            cur.execute(query, (country_name,))
            result = cur.fetchone()
            if result is None:
                return f"No data found for country: {country_name}", 404
            match(topic):
                case "POPULATION": return summary_generator.generate_population_summary(result), 200
                case "TRADE": return summary_generator.generate_trade_summary(result), 200
                case "IMPORT_EXPORT": return summary_generator.generate_import_export_summary(result), 200
                case "SUMARRY": return summary_generator.generate_summary(result), 200
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