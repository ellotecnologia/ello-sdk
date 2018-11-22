# encoding: utf8
from __future__ import unicode_literals

import unittest
from ello.sdk.text_manipulation import (
    apply_some_fixups, 
    ignore_line,
    preprocess_commit_messages
)

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
        
        original_text = "nova correção na atualização do saldo do colaborador"
        expected_text = "Correção na atualização do saldo do colaborador"
        self.assertEqual(expected_text, apply_some_fixups(original_text))
        
    def test_ignore_line(self):
        self.assertFalse(ignore_line("Melhoria no processo de xxx"))

        self.assertTrue(ignore_line("Revisão no processo de xxx"), 'Deve ignorar a palavra revisão')
        self.assertTrue(ignore_line("Criado frame de Farmácia Popular no cadastro do produto"), 'Deve ignorar a palavra frame')
        self.assertTrue(ignore_line("Atualização nos metadados do projeto"))
        self.assertTrue(ignore_line("Atualização no metadado do projeto"))
        self.assertTrue(ignore_line("Removido dataset não mais utilizado"))
        self.assertTrue(ignore_line("Removido ClientDataset não mais utilizado"))
        self.assertTrue(ignore_line("Movi componentes relacionados ao princípio ativo para um frame isolado"))
        self.assertTrue(ignore_line('Revert "Correção na gravação da data do lote (#9312)"'))
        self.assertTrue(ignore_line("Limpeza das units"))
        self.assertTrue(ignore_line("Correção para adicionar script no arquivo de resources"))
        self.assertTrue(ignore_line("Renomeada variável xxx"))
        self.assertTrue(ignore_line("Renomeado variável xxx"))
        self.assertTrue(ignore_line("Renomeei variável xxx"))
    
    def test_message_removal(self):
        messages = [
            '- Mensagem commit 01 (#9312) <Bruno>', 
            '- Mensagem commit 02 <Clayton>', 
            '- Esta mensagem não pode ir* <Clayton>', 
            '- Mensagem commit 04 <Clayton>', 
            '- Esta também não* <Clayton>', 
            '- Outro teste <Clayton>'
        ]
        expected_messages = [
            '- Outro teste <Clayton>'
        ]
        messages = preprocess_commit_messages(messages)
        self.assertEqual(expected_messages, messages)
        

if __name__ == "__main__":
    unittest.main()