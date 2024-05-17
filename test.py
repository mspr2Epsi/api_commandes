import unittest
from unittest.mock import  patch
from api_commandes import app




class TestCommande(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    # Tests unitaires
    def tests_unitaires(self):
        self.test_get_all_orders_with_valid_token()
        self.test_get_all_orders_with_invalid_token()
        self.test_get_order_with_product_and_client_with_valid_token()
        self.test_get_order_with_product_and_client_with_invalid_token()
        self.test_create_order_with_incomplete_data()
        self.test_update_order_with_no_data_provided()
        self.test_delete_nonexistent_order()

    # Tests d'intégration
    def test_integration(self):
        self.test_create_order_with_valid_token()
        self.test_create_order_with_invalid_token()
        self.test_update_order_with_valid_token()
        self.test_update_order_with_invalid_token()
        self.test_delete_order_with_valid_token()
        self.test_delete_order_with_invalid_token()

    # Tests fonctionnels
    def test_fonctionnel(self):
        self.test_get_all_orders_with_valid_token()
        self.test_get_order_with_product_and_client_with_valid_token()
        self.test_create_order_with_valid_token()
        self.test_update_order_with_valid_token()
        self.test_delete_order_with_valid_token()

    # Tests de régression
    def test_regression(self):
        self.test_get_all_orders_with_valid_token()
        self.test_get_order_with_product_and_client_with_valid_token()
        self.test_delete_nonexistent_order()

    # Tests de performance
    def test_performance(self):
        # Placeholder for performance tests
        pass

    # Tests de sécurité
    def test_securite(self):
        self.test_get_all_orders_with_invalid_token()
        self.test_get_order_with_product_and_client_with_invalid_token()
        self.test_create_order_with_invalid_token()
        self.test_update_order_with_invalid_token()
        self.test_delete_order_with_invalid_token()

    def test_get_all_orders_with_valid_token(self):
        with unittest.mock.patch('api_commandes.read_possible', return_value=True):
            response = self.app.get('/commande', headers={'Authorization': 'valid_token'})
            self.assertEqual(response.status_code, 200)

    def test_get_all_orders_with_invalid_token(self):
        with unittest.mock.patch('api_commandes.read_possible', return_value=False):
            response = self.app.get('/commande', headers={'Authorization': 'invalid_token'})
            self.assertEqual(response.status_code, 401)


    def test_get_order_with_product_and_client_with_valid_token(self):
        commande_id = 1  
        with patch('api_commandes.read_possible', return_value=True):
            response = self.app.get(f'/commande/{commande_id}', headers={'Authorization': 'valid_token'})
            self.assertEqual(response.status_code, 200)

    def test_get_order_with_product_and_client_with_invalid_token(self):
        commande_id = 1  
        with patch('api_commandes.read_possible', return_value=False):
            response = self.app.get(f'/commande/{commande_id}', headers={'Authorization': 'invalid_token'})
            self.assertEqual(response.status_code, 401)


    def test_create_order_with_valid_token(self):
        valid_data = {
            'ClientID': 1,
            'DateCommande': '2024-05-17',
            'Statut': 'Pending',
            'PrixTotal': 100.0
        }
        with patch('api_commandes.creation_possible', return_value=True):
            response = self.app.post('/commande', json=valid_data, headers={'Authorization': 'valid_token'})
            self.assertEqual(response.status_code, 201)

    def test_create_order_with_invalid_token(self):
        valid_data = {
            'ClientID': 1,
            'DateCommande': '2024-05-17',
            'Statut': 'Pending',
            'PrixTotal': 100.0
        }
        with patch('api_commandes.creation_possible', return_value=False):
            response = self.app.post('/commande', json=valid_data, headers={'Authorization': 'invalid_token'})
            self.assertEqual(response.status_code, 401)

    def test_create_order_with_incomplete_data(self):
        incomplete_data = {
            'ClientID': 1,
            'DateCommande': '2024-05-17',
            'Statut': 'Pending'
        }
        with patch('api_commandes.creation_possible', return_value=True):
            response = self.app.post('/commande', json=incomplete_data, headers={'Authorization': 'valid_token'})
            self.assertEqual(response.status_code, 400)

    def test_update_order_with_valid_token(self):
        order_id = 4
        valid_data = {
            'ClientID': 1,
            'DateCommande': '2024-05-17',
            'Statut': 'Shipped',
            'PrixTotal': 150.0
        }
        with patch('api_commandes.update_possible', return_value=True):
            response = self.app.put(f'/commande/{order_id}', json=valid_data, headers={'Authorization': 'valid_token'})
            self.assertEqual(response.status_code, 200)

    def test_update_order_with_invalid_token(self):
        # Assuming valid data is provided
        order_id = 1
        valid_data = {
            'ClientID': 1,
            'DateCommande': '2024-05-17',
            'Statut': 'Shipped',
            'PrixTotal': 150.0
        }
        with patch('api_commandes.update_possible', return_value=False):
            response = self.app.put(f'/commande/{order_id}', json=valid_data, headers={'Authorization': 'invalid_token'})
            self.assertEqual(response.status_code, 401)

    def test_update_order_with_no_data_provided(self):
        # Assuming no data is provided
        order_id = 1
        invalid_data = {
        
        }        
        with patch('api_commandes.update_possible', return_value=True):
            response = self.app.put(f'/commande/{order_id}', json=invalid_data, headers={'Authorization': 'valid_token'})
            self.assertEqual(response.status_code, 400)



    def test_delete_order_with_valid_token(self):
        # Assuming an existing order ID and a valid token
        order_id = 1
        with patch('api_commandes.delete_possible', return_value=True):
            response = self.app.delete(f'/commande/{order_id}', headers={'Authorization': 'valid_token'})
            self.assertEqual(response.status_code, 200)

    def test_delete_order_with_invalid_token(self):
        # Assuming an existing order ID and an invalid token
        order_id = 1
        with patch('api_commandes.delete_possible', return_value=False):
            response = self.app.delete(f'/commande/{order_id}', headers={'Authorization': 'invalid_token'})
            self.assertEqual(response.status_code, 401)

    def test_delete_nonexistent_order(self):
        # Assuming a non-existent order ID and a valid token
        order_id = 999  # Assuming a non-existent order ID
        with patch('api_commandes.delete_possible', return_value=True):
            response = self.app.delete(f'/commande/{order_id}', headers={'Authorization': 'valid_token'})
            self.assertEqual(response.status_code, 404)

# if __name__ == '__main__':
#     unittest.main()