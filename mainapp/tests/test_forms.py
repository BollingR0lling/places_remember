from django.test import TestCase
from django.forms.widgets import TextInput, Textarea
from ..forms import MemoryModelForm


class MemoryModelFormTestCase(TestCase):

    def test_place_is_wrong(self):
        form_data = {
            'location': 'Место, которого не существует',
            'title': 'Какой то заголовок',
            'description': 'Какое то описание'
        }
        form = MemoryModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_null_title(self):
        form_data = {
            'location': 'США, Нью-Йорк',
            'title': '',
            'description': 'Какое то описание'
        }
        form = MemoryModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_null_description(self):
        form_data = {
            'location': 'США, Нью-Йорк',
            'title': 'Какой то заголовок',
            'description': ''
        }
        form = MemoryModelForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_help_from_field(self):
        form = MemoryModelForm()
        self.assertEqual(
            form.fields['location'].widget.attrs['placeholder'],
            'Место воспоминания'
        )
        self.assertEqual(
            form.fields['title'].widget.attrs['placeholder'],
            'Придумайте для него название'
        )
        self.assertEqual(
            form.fields['description'].widget.attrs['placeholder'],
            'Опишите его'
        )

    def test_widget_type_check(self):
        form = MemoryModelForm()
        self.assertEqual(type(form.fields['location'].widget), TextInput)
        self.assertEqual(type(form.fields['description'].widget), Textarea)
