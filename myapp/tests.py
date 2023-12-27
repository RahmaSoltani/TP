#implementation des tests unitaires
import os
from django.test import TestCase
from .serializers import PDFTxtExtractionSerializer

class PDFTxtExtractionSerializerTest(TestCase):
    def setUp(self):
        self.serializer = PDFTxtExtractionSerializer()
        # Spécifiez le chemin complet du fichier PDF que vous souhaitez utiliser pour le test
        self.pdf_path = os.path.join(os.path.dirname(__file__), 'C:/Users/ThinkPad X280/Desktop/TP/articles/Article_01.pdf')

    def test_extract_text_from_pdf(self):
     # Appelez la méthode d'extraction de texte du serializer
     extracted_text = self.serializer.extract_text_from_pdf(self.pdf_path)

     # Vérifiez si le texte extrait n'est pas vide
     self.assertTrue(extracted_text, "Aucun texte n'a été extrait du PDF.")
