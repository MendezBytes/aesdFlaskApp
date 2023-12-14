from flask import Flask, request, jsonify,render_template
import psycopg2

app = Flask(__name__)


db_connection = {
    'dbname': 'postgres',
    'user': 'postgres',
    'host': 'localhost',
    'port': '5432',
}

    
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test_db')
def test_db():
    # Replace these with your PostgreSQL database details
    connection = psycopg2.connect(
        user="postgres",
        host="localhost",
        port="5432",
        database="postgres"
    )

    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

    print(f"Connected to: {db_version[0]}")
    cursor.close()
    connection.close()
    return jsonify({'message': f"{db_version[0]}"})


    
