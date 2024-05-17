from db_connector import connect_to_database, close_connection
from flask import Flask, request, jsonify
from roles import  read_possible,update_possible,creation_possible,delete_possible
import pika
from datetime import datetime

#pour le message broker
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='message_broker_client')

db_connection = connect_to_database()
cursor = db_connection.cursor()
app = Flask(__name__)



@app.route('/commande', methods=['GET'])
def get_all_orders_with_products_and_clients():
    begin_time = datetime.now()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f" {begin_time.strftime("%Y-%m-%d %H:%M:%S")} Debut du traitement  get_all_orders_with_products_and_clients")    
    token = request.headers.get('Authorization')
    if read_possible(token) != True:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 401 traitement get_all_orders_with_products_and_clients termine")        
        return jsonify({'message': 'Unauthorized'}), 401    

    cursor.execute("""SELECT cmd.CommandeID, cmd.DateCommande, cmd.Statut, cmd.PrixTotal, cl.Nom AS NomClient,
    cl.Prenom AS PrenomClient, pr.Nom AS NomProduit, pr.Description AS DescriptionProduit, pr.PrixUnitaire AS PrixUnitaireProduit, 
    pr.Stock AS StockProduit, pr.Fournisseur AS FournisseurProduit, dc.Quantite FROM commandes cmd JOIN clients cl 
    ON cmd.ClientID = cl.ClientID JOIN detailsCommande dc ON cmd.CommandeID = dc.CommandeID 
    JOIN produits pr ON dc.ProduitID = pr.ProduitID;""")
    commande = cursor.fetchall()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 200 traitement get_all_orders_with_products_and_clients termine")       
    return jsonify({'commande': commande})

@app.route('/commande/<int:commande_id>', methods=['GET'])
def get_order_with_product_and_client(commande_id):
    begin_time = datetime.now()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f" {begin_time.strftime("%Y-%m-%d %H:%M:%S")} Debut du traitement  get_order_with_product_and_client by ID")        
    token = request.headers.get('Authorization')
    if read_possible(token) != True:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 401 traitement get_order_with_product_and_client by ID termine")             
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
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 200 traitement get_order_with_product_and_client by ID termine")            
        return jsonify({'client': commande})
    else:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 404 traitement get_order_with_product_and_client by ID termine")           
        return jsonify({'message': 'Client not found'}), 404

@app.route('/commande', methods=['POST'])
def create_order():
    begin_time = datetime.now()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f" {begin_time.strftime("%Y-%m-%d %H:%M:%S")} Debut du traitement  create_order") 
    token = request.headers.get('Authorization')
    if creation_possible(token) != True:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 401 traitement create_order termine")   
        return jsonify({'message': 'Unauthorized'}), 401  
    
    required_keys = ['ClientID', 'DateCommande', 'Statut', 'PrixTotal']
    data = request.get_json()
    if not all(key in data for key in required_keys):
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 400 traitement create_order termine")           
        return jsonify({'message': 'Incomplete data'}), 400
    cursor.execute("""
        INSERT INTO commandes (ClientID, DateCommande, Statut, PrixTotal) 
        VALUES (%s, %s, %s, %s)
        """, (data['ClientID'], data['DateCommande'], data['Statut'], data['PrixTotal']))
    db_connection.commit()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 201 traitement create_order termine")       
    return jsonify({'message': 'order created successfully'}), 201    
 
@app.route('/commande/<int:id>', methods=['PUT'])
def update_order(id):
    begin_time = datetime.now()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f" {begin_time.strftime("%Y-%m-%d %H:%M:%S")} Debut du traitement  update_order")     
    token = request.headers.get('Authorization')
    if update_possible(token) != True:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 401 traitement update_order termine")         
        return jsonify({'message': 'Unauthorized'}), 401 
    
    data = request.get_json()
    if not data:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 400 traitement update_order termine")           
        return jsonify({'message': 'No data provided'}), 400

    cursor.execute("""
        UPDATE commandes
        SET ClientID = %s, DateCommande = %s, Statut = %s, PrixTotal = %s
        WHERE CommandeID = %s
        """, (data.get('ClientID'), data.get('DateCommande'), data.get('Statut'), data.get('PrixTotal'), id))
    
    db_connection.commit()
    if cursor.rowcount > 0:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 200 traitement update_order termine")      
        return jsonify({'message': 'Order updated successfully'}), 200
    else:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 404 traitement update_order termine")              
        return jsonify({'message': 'Order not found'}), 404

@app.route('/commande/<int:id>', methods=['DELETE'])
def delete_order(id):
    begin_time = datetime.now()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f" {begin_time.strftime("%Y-%m-%d %H:%M:%S")} Debut du traitement delete_order")      
    token = request.headers.get('Authorization')
    if delete_possible(token) != True:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 401 traitement delete_order termine")             
        return jsonify({'message': 'Unauthorized'}), 401 

    cursor.execute("SELECT * FROM commandes WHERE CommandeID = %s", (id,))
    order = cursor.fetchone()
    if order is None:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 404 traitement delete_order termine")            
        return jsonify({'message': 'Order not found'}), 404

    cursor.execute("DELETE FROM commandes WHERE CommandeID = %s", (id,))
    db_connection.commit()

    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 200 traitement delete_order termine")    
    return jsonify({'message': 'Order deleted successfully'}), 200

@app.route('/commande/detail', methods=['POST'])
def create_order_detail():
    begin_time = datetime.now()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f" {begin_time.strftime("%Y-%m-%d %H:%M:%S")} Debut du traitement create_order_detail")          
    token = request.headers.get('Authorization')
    if creation_possible(token) != True:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 401 traitement create_order_detail termine")            
        return jsonify({'message': 'Unauthorized'}), 401 

    required_keys = ['CommandeID', 'ProduitID', 'Quantite']
    data = request.get_json()
    if not all(key in data for key in required_keys):
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 400 traitement create_order_detail termine")          
        return jsonify({'message': 'Incomplete data'}), 400
    cursor.execute("""
        INSERT INTO detailscommande (CommandeID, ProduitID, Quantite) 
        VALUES (%s, %s, %s)
        """, (data['CommandeID'], data['ProduitID'], data['Quantite']))
    db_connection.commit()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 201 traitement create_order_detail termine")      
    return jsonify({'message': 'order detail created successfully'}), 201   

@app.route('/commande/detail/<int:id>', methods=['PUT'])
def update_order_detail(id):
    begin_time = datetime.now()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f" {begin_time.strftime("%Y-%m-%d %H:%M:%S")} Debut du traitement update_order_detail")      
    token = request.headers.get('Authorization')
    if update_possible(token) != True:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 401 traitement update_order_detail termine")              
        return jsonify({'message': 'Unauthorized'}), 401     
    data = request.get_json()
    if not data:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 400 traitement update_order_detail termine")                
        return jsonify({'message': 'No data provided'}), 400

    cursor.execute("""
        UPDATE detailscommande
        SET CommandeID = %s, ProduitID = %s, Quantite = %s
        WHERE DetailID = %s
        """, (data.get('CommandeID'), data.get('ProduitID'), data.get('Quantite'), id))
    
    if cursor.rowcount == 0:
        return jsonify({'message': 'Order detail not found'}), 404
    
    db_connection.commit()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 200 traitement update_order_detail termine")            
    return jsonify({'message': 'Order detail updated successfully'}), 200

@app.route('/commande/detail/<int:id>', methods=['DELETE'])
def delete_order_detail(id):
    begin_time = datetime.now()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f" {begin_time.strftime("%Y-%m-%d %H:%M:%S")} Debut du traitement delete_order_detail")      
    token = request.headers.get('Authorization')
    if delete_possible(token) != True:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 401 traitement delete_order_detail termine")           
        return jsonify({'message': 'Unauthorized'}), 401 

    cursor.execute("SELECT * FROM detailscommande WHERE DetailID = %s", (id,))
    order_detail = cursor.fetchone()
    if order_detail is None:
        channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 404 traitement delete_order_detail termine")         
        return jsonify({'message': 'Order detail not found'}), 404

    cursor.execute("DELETE FROM detailscommande WHERE DetailID = %s", (id,))
    db_connection.commit()
    channel.basic_publish(exchange='', routing_key='message_broker_commande', body=f"Temps d'execution {(datetime.now()-begin_time)} - Code 200 traitement delete_order_detail termine") 
    return jsonify({'message': 'Order detail deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
