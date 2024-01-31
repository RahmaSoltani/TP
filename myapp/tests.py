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


class InfoExtractorTest(TestCase):
    def test_extract_info(self):
        # Spécifiez le chemin du fichier de test
        test_file_path = 'extracted.txt'  # Remplacez par le chemin de votre fichier

        # Créez une instance de votre sérialiseur avec le chemin du fichier de test
        serializer = InfoExtractor(data={'content': test_file_path})

        # Vérifiez si le sérialiseur est valide avec les données fournies
        self.assertTrue(serializer.is_valid(), f"Serializer errors: {serializer.errors}")

        # Appelez la fonction extract_info sur l'instance du sérialiseur
        result = serializer.extract_info()

        # Vérifiez les résultats attendus dans les champs
        self.assertEqual(result['content'], expected_content_value)
        self.assertEqual(result['title'], expected_title_value)
        self.assertEqual(result['authors'], expected_authors_value)
        self.assertEqual(result['institutions'], expected_institutions_value)
        self.assertEqual(result['abstract'], expected_abstract_value)
        self.assertEqual(result['keywords'], expected_keywords_value)
        self.assertEqual(result['references'], expected_references_value)