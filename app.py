from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


db_connection = {
    'dbname': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': '5432',
}

def execute_query(query, params=None, fetchone=False):
    conn = psycopg2.connect(**db_connection)
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    if fetchone:
        result = cursor.fetchone()
    else:
        result = cursor.fetchall()

    conn.commit()
    conn.close()

    return result
    
    
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'message': 'Name is required'}), 400

    query = "INSERT INTO items (name) VALUES (%s)"
    params = (name,)
    execute_query(query, params)

    return jsonify({'message': 'Item created successfully'}), 201

@app.route('/items', methods=['GET'])
def get_items():
    query = "SELECT id, name FROM items"
    items = execute_query(query)

    item_list = [{'id': item[0], 'name': item[1]} for item in items]
    return jsonify(item_list)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    query = "SELECT id, name FROM items WHERE id = %s"
    params = (item_id,)
    item = execute_query(query, params, fetchone=True)

    if not item:
        return jsonify({'message': 'Item not found'}), 404

    return jsonify({'id': item[0], 'name': item[1]})

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    new_name = data.get('name')

    if not new_name:
        return jsonify({'message': 'Name is required'}), 400

    query = "UPDATE items SET name = %s WHERE id = %s"
    params = (new_name, item_id)
    execute_query(query, params)

    return jsonify({'message': 'Item updated successfully'})

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    query = "DELETE FROM items WHERE id = %s"
    params = (item_id,)
    execute_query(query, params)

    return jsonify({'message': 'Item deleted successfully'})

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5500,debug=True)