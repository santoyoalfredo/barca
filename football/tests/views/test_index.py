from django.test import TestCase
from django.urls import reverse_lazy

class IndexViewTests(TestCase):
	#
	# The index view should return the base.html template
	# for rendering
	#
	def test_base(self):
		response = self.client.get(reverse_lazy('index'))
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(template_name='base.html', count=1)
	#
	# The index view should return the index.html template
	# for rendering
	#
	def test_index(self):
		response = self.client.get(reverse_lazy('index'))
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(template_name='index.html', count=1)
