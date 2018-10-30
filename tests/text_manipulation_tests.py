# encoding: utf8
from __future__ import unicode_literals

import unittest
from ello.sdk.text_manipulation import apply_some_fixups, ignore_line

class TextManipulationTests(unittest.TestCase):

    def test_text_fixups(self):
        original_text = "aprimoramento no formulários para não repetir a função OPEN na criação";
        expected_text = "Aprimoramento no formulários para não repetir a função OPEN na criação"
        self.assertEqual(expected_text, apply_some_fixups(original_text))
            
        original_text = "Pequena correção no recurso X"
        expected_text = "Correção no recurso X"
        self.assertEqual(expected_text, apply_some_fixups(original_text))
        
        original_text = "Atualizei o form de clientes com novos recursos"
        expected_text = "Atualizei a tela de clientes com novos recursos"
        self.assertEqual(expected_text, apply_some_fixups(original_text))
        
        original_text = "Correção no grid de clientes"
        expected_text = "Correção na grade de clientes"
        self.assertEqual(expected_text, apply_some_fixups(original_text))

        original_text = "Melhoria no processo de emissão de notas"
        expected_text = "Aprimoramento no processo de emissão de notas"
        self.assertEqual(expected_text, apply_some_fixups(original_text))
        
    def test_ignore_line(self):
        self.assertTrue(ignore_line("Revisão no processo de xxx"))
        self.assertFalse(ignore_line("Melhoria no processo de xxx"))
        

if __name__ == "__main__":
    unittest.main()