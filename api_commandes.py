from db_connector import connect_to_database, close_connection
from flask import Flask, request, jsonify
from roles import  read_possible,update_possible,creation_possible,delete_possible

db_connection = connect_to_database()
cursor = db_connection.cursor()
app = Flask(__name__)

#TODO  ajouter les permission les méthodes PUT DELETE et POST

@app.route('/commande', methods=['GET'])
def get_all_orders_with_products_and_clients():
    cursor.execute("""SELECT cmd.CommandeID, cmd.DateCommande, cmd.Statut, cmd.PrixTotal, cl.Nom AS NomClient,
    cl.Prenom AS PrenomClient, pr.Nom AS NomProduit, pr.Description AS DescriptionProduit, pr.PrixUnitaire AS PrixUnitaireProduit, 
    pr.Stock AS StockProduit, pr.Fournisseur AS FournisseurProduit, dc.Quantite FROM commandes cmd JOIN clients cl 
    ON cmd.ClientID = cl.ClientID JOIN detailsCommande dc ON cmd.CommandeID = dc.CommandeID 
    JOIN produits pr ON dc.ProduitID = pr.ProduitID;""")
    commande = cursor.fetchall()
    return jsonify({'commande': commande})

@app.route('/commande/<int:commande_id>', methods=['GET'])
def get__order_with_product_and_client(commande_id):
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

if __name__ == '__main__':
    app.run(debug=True)
