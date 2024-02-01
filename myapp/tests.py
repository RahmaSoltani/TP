#implementation des tests unitaires
import os
from django.test import TestCase
from .serializers import PDFTxtExtractionSerializer
from .serializers import InfoExtractor

   #Premier test pour les fichier pdf téléchargés


class PDFTxtExtractionSerializerTest(TestCase):
    def setUp(self):
        self.serializer = PDFTxtExtractionSerializer()
        self.pdf_path = os.path.join(os.path.dirname(__file__), 'C:/Users/ThinkPad X280/Desktop/TP/articles/Article_01.pdf')

    def test_extract_text_from_pdf(self):
     extracted_text = self.serializer.extract_text_from_pdf(self.pdf_path)

     self.assertTrue(extracted_text, "Aucun texte n'a été extrait du PDF.")

class InfoExtractorTest(TestCase):
   class InfoExtractorTest(TestCase):
    def setUp(self):
        self.info_extractor = InfoExtractor()
        self.test_file_path = os.path.join(os.path.dirname(__file__), 'C:/Users/ThinkPad X280/Desktop/TP/extracted_text.txt')

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_extract_info_fields(self):
        with open(self.test_file_path, 'w', encoding='utf-8') as test_file:
            test_file.write("Your test content here.")

        info_extractor = InfoExtractor()
        info_extractor._validated_data = {'content': self.test_file_path}

        result = info_extractor.extract_info()

        self.assertIn('title', result, "Title should be present in the result")
        self.assertIn('authors', result, "Authors should be present in the result")
        self.assertIn('institutions', result, "Institutions should be present in the result")
        self.assertIn('abstract', result, "Abstract should be present in the result")
        self.assertIn('keywords', result, "Keywords should be present in the result")
        self.assertIn('references', result, "References should be present in the result")

