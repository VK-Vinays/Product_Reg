import unittest
import os
from flask import Flask
from app import app, db, User, Product, convert_date
import yaml
import subprocess

def read_yaml_data(key):
    local_path = os.path.dirname(os.path.abspath(__file__)) + '/config.yaml'
    if os.path.exists(local_path):
        with open(local_path, 'r') as yaml_data:
            data = yaml.safe_load(yaml_data)
            return data[key]

class TestProductApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.yaml_data = read_yaml_data('UNIT_TEST_CONFIG')
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = cls.yaml_data['SQLALCHEMY_DATABASE_URI']
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.rollback()
        #db.drop_all()
        cls.app_context.pop()

    def test_user_registration(self):
        response = self.app.post('/register', data=dict(
            name=self.yaml_data.get('TEST_USER',{}).get('name'),
            email=self.yaml_data.get('TEST_USER',{}).get('email'),
            password=self.yaml_data.get('TEST_USER',{}).get('password')
        ), follow_redirects=True)
        self.assertIn(b'User already exists, Try to register with different name', response.data)

    def test_login(self):
        response = self.app.post('/login', data=dict(
            name=self.yaml_data.get('TEST_USER', {}).get('name'),
            password=self.yaml_data.get('TEST_USER', {}).get('password')
        ), follow_redirects=True)
        self.assertIn(b'Login successfull', response.data)
    
    def test_prod_reg(self):
        response = self.app.post('/product_reg', data=dict(
            product_name=self.yaml_data.get('TEST_PRODUCT', {}).get('product_name'),
            prod_discription=self.yaml_data.get('TEST_PRODUCT', {}).get('prod_discription'),
            manfacture_info=self.yaml_data.get('TEST_PRODUCT', {}).get('manfacture_info'),
            serial_number=self.yaml_data.get('TEST_PRODUCT', {}).get('serial_number'),
            manfacture_date=self.yaml_data.get('TEST_PRODUCT', {}).get('manfacture_date'),
            warranty_info=self.yaml_data.get('TEST_PRODUCT', {}).get('warranty_info'),
            prod_category=self.yaml_data.get('TEST_PRODUCT', {}).get('prod_category'),
        ), follow_redirects=True)
        #self.assertIn(b'Prodcut registered Successfully', response.data)
        self.assertIn(b'Product already registered with Serial Number 12345', response.data)
        
if __name__ == '__main__':
    #unittest.main()
    result = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestProductApp))
    if result.wasSuccessful():
        subprocess.Popen(['python3', 'app.py'])
    else:
        raise RuntimeError("Unit tests failed. Check the test results.")