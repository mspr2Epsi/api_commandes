from db_connector import connect_to_database, close_connection
from flask import Flask, request, jsonify
from roles import  read_possible,update_possible,creation_possible,delete_possible

db_connection = connect_to_database()
cursor = db_connection.cursor()
app = Flask(__name__)

#TODO  ajouter les permission les méthodes PUT DELETE et POST

@app.route('/commande', methods=['GET'])
def get_all_orders_with_products_and_clients():
    token = request.headers.get('Authorization')
    if read_possible(token) != True:
        return jsonify({'message': 'Unauthorized'}), 401    

    cursor.execute("""SELECT cmd.CommandeID, cmd.DateCommande, cmd.Statut, cmd.PrixTotal, cl.Nom AS NomClient,
    cl.Prenom AS PrenomClient, pr.Nom AS NomProduit, pr.Description AS DescriptionProduit, pr.PrixUnitaire AS PrixUnitaireProduit, 
    pr.Stock AS StockProduit, pr.Fournisseur AS FournisseurProduit, dc.Quantite FROM commandes cmd JOIN clients cl 
    ON cmd.ClientID = cl.ClientID JOIN detailsCommande dc ON cmd.CommandeID = dc.CommandeID 
    JOIN produits pr ON dc.ProduitID = pr.ProduitID;""")
    commande = cursor.fetchall()
    return jsonify({'commande': commande})

@app.route('/commande/<int:commande_id>', methods=['GET'])
def get_order_with_product_and_client(commande_id):
    token = request.headers.get('Authorization')
    if read_possible(token) != True:
        return jsonify({'message': 'Unauthorized'}), 401    

    cursor.execute("""
    SELECT cmd.CommandeID, cmd.DateCommande, cmd.Statut, cmd.PrixTotal, cl.Nom AS NomClient,
    cl.Prenom AS PrenomClient, pr.Nom AS NomProduit, pr.Description AS DescriptionProduit, pr.PrixUnitaire AS PrixUnitaireProduit, 
    pr.Stock AS StockProduit, pr.Fournisseur AS FournisseurProduit, dc.Quantite FROM commandes cmd JOIN clients cl 
    ON cmd.ClientID = cl.ClientID JOIN detailsCommande dc ON cmd.CommandeID = dc.CommandeID 
    JOIN produits pr ON dc.ProduitID = pr.ProduitID  WHERE cmd.CommandeID = %s;
    """, (commande_id,))
    commande = cursor.fetchall()
    if commande:
        return jsonify({'client': commande})
    else:
        return jsonify({'message': 'Client not found'}), 404

@app.route('/commande', methods=['POST'])
def create_order():
    token = request.headers.get('Authorization')
    if creation_possible(token) != True:
        return jsonify({'message': 'Unauthorized'}), 401  
    
    required_keys = ['ClientID', 'DateCommande', 'Statut', 'PrixTotal']
    data = request.get_json()
    if not all(key in data for key in required_keys):
        return jsonify({'message': 'Incomplete data'}), 400
    cursor.execute("""
        INSERT INTO commandes (ClientID, DateCommande, Statut, PrixTotal) 
        VALUES (%s, %s, %s, %s)
        """, (data['ClientID'], data['DateCommande'], data['Statut'], data['PrixTotal']))
    db_connection.commit()
    return jsonify({'message': 'order created successfully'}), 201    
 
@app.route('/commande/<int:id>', methods=['PUT'])
def update_order(id):
    token = request.headers.get('Authorization')
    if update_possible(token) != True:
        return jsonify({'message': 'Unauthorized'}), 401 
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    cursor.execute("""
        UPDATE commandes
        SET ClientID = %s, DateCommande = %s, Statut = %s, PrixTotal = %s
        WHERE CommandeID = %s
        """, (data.get('ClientID'), data.get('DateCommande'), data.get('Statut'), data.get('PrixTotal'), id))
    
    db_connection.commit()
    if cursor.rowcount > 0:
        return jsonify({'message': 'Order updated successfully'}), 200
    else:
        return jsonify({'message': 'Order not found'}), 404

@app.route('/commande/<int:id>', methods=['DELETE'])
def delete_order(id):
    token = request.headers.get('Authorization')
    if delete_possible(token) != True:
        return jsonify({'message': 'Unauthorized'}), 401 

    cursor.execute("SELECT * FROM commandes WHERE CommandeID = %s", (id,))
    order = cursor.fetchone()
    if order is None:
        return jsonify({'message': 'Order not found'}), 404

    cursor.execute("DELETE FROM commandes WHERE CommandeID = %s", (id,))
    db_connection.commit()

    return jsonify({'message': 'Order deleted successfully'}), 200

@app.route('/commande/detail', methods=['POST'])
def create_order_detail():
    token = request.headers.get('Authorization')
    if creation_possible(token) != True:
        return jsonify({'message': 'Unauthorized'}), 401 

    required_keys = ['CommandeID', 'ProduitID', 'Quantite']
    data = request.get_json()
    if not all(key in data for key in required_keys):
        return jsonify({'message': 'Incomplete data'}), 400
    cursor.execute("""
        INSERT INTO detailscommande (CommandeID, ProduitID, Quantite) 
        VALUES (%s, %s, %s)
        """, (data['CommandeID'], data['ProduitID'], data['Quantite']))
    db_connection.commit()
    return jsonify({'message': 'order detail created successfully'}), 201   

@app.route('/commande/detail/<int:id>', methods=['PUT'])
def update_order_detail(id):
    token = request.headers.get('Authorization')
    if update_possible(token) != True:
        return jsonify({'message': 'Unauthorized'}), 401     
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    cursor.execute("""
        UPDATE detailscommande
        SET CommandeID = %s, ProduitID = %s, Quantite = %s
        WHERE DetailID = %s
        """, (data.get('CommandeID'), data.get('ProduitID'), data.get('Quantite'), id))
    
    if cursor.rowcount == 0:
        return jsonify({'message': 'Order detail not found'}), 404
    
    db_connection.commit()
    return jsonify({'message': 'Order detail updated successfully'}), 200

@app.route('/commande/detail/<int:id>', methods=['DELETE'])
def delete_order_detail(id):
    token = request.headers.get('Authorization')
    if delete_possible(token) != True:
        return jsonify({'message': 'Unauthorized'}), 401 

    cursor.execute("SELECT * FROM detailscommande WHERE DetailID = %s", (id,))
    order_detail = cursor.fetchone()
    if order_detail is None:
        return jsonify({'message': 'Order detail not found'}), 404

    cursor.execute("DELETE FROM detailscommande WHERE DetailID = %s", (id,))
    db_connection.commit()

    return jsonify({'message': 'Order detail deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
