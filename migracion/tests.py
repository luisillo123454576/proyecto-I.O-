from django.test import TestCase, Client
from django.urls import reverse
import os
import json

class MigracionTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dashboard_view(self):
        response = self.client.get(reverse('migracion:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'OPTIQUEUE')
        self.assertContains(response, 'x* = 15')
        self.assertContains(response, '801.07')

    def test_vista_codigo(self):
        response = self.client.get(reverse('migracion:vista_codigo'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'pulp.LpVariable')
        self.assertContains(response, 'simpy.Environment')

    def test_documentacion_views(self):
        r1 = self.client.get(reverse('migracion:vista_documentacion'))
        self.assertEqual(r1.status_code, 200)
        
        r2 = self.client.get(reverse('migracion:vista_documentacion_doc', args=['02']))
        self.assertEqual(r2.status_code, 200)
        self.assertContains(r2, 'Shark Tank')

        r3 = self.client.get(reverse('migracion:vista_documentacion_doc', args=['03']))
        self.assertEqual(r3.status_code, 200)
        self.assertContains(r3, 'Preguntas')

    def test_api_optimizar(self):
        response = self.client.get(reverse('migracion:api_optimizar'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['x_optimo'], 15)
        self.assertAlmostEqual(data['y_optimo'], 801.07, places=1)

    def test_api_recalcular(self):
        response = self.client.get(reverse('migracion:api_recalcular') + '?c=15')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['c'], 15)
        self.assertTrue(data['cumple_restriccion'])

    def test_api_simular(self):
        response = self.client.get(reverse('migracion:api_simular') + '?ventanillas=15&duracion=1.0')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertGreater(data['total_atendidos'], 50)
