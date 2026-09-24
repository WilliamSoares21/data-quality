"""
Suíte de Testes Unitários de Segurança, Mock Data e Arquitetura em Memória.
Valida o comportamento da guarda RBAC, sanitização de Path Traversal, Hashing Argon2id e Repositório em Memória.
"""

import unittest
from unittest.mock import MagicMock, patch
import os
import streamlit as st

from utils.security import sanitize_filename, validate_uploaded_file, get_safe_filepath
from utils.auth import hash_password, verify_password, check_permission, login
import database.repository as repo
from database.connection import init_demo_data, get_database


class TestSecurityUtils(unittest.TestCase):
    def test_sanitize_filename_prevents_path_traversal(self):
        dangerous_input = "../../../etc/passwd"
        clean = sanitize_filename(dangerous_input)
        self.assertEqual(clean, "passwd")
        self.assertNotIn("..", clean)
        self.assertNotIn("/", clean)

    def test_get_safe_filepath_validates_boundary(self):
        base_dir = os.path.abspath("data")
        filepath = get_safe_filepath(base_dir, "test_file.jpg")
        self.assertTrue(filepath.startswith(base_dir))

    def test_password_hashing_and_verification(self):
        raw_pass = "SenhaSegura123!"
        hashed = hash_password(raw_pass)
        
        self.assertNotEqual(raw_pass, hashed)
        self.assertTrue(hashed.startswith(("$argon2", "$2b$", "$2a$")))
        self.assertTrue(verify_password(raw_pass, hashed))
        self.assertFalse(verify_password("SenhaIncorreta", hashed))

    @patch("streamlit.session_state", {})
    @patch("streamlit.stop")
    @patch("streamlit.error")
    def test_check_permission_unauthenticated(self, mock_error, mock_stop):
        check_permission()
        mock_error.assert_called_once()
        mock_stop.assert_called_once()

    @patch("streamlit.session_state", {"logged_in": True, "role": "user"})
    @patch("streamlit.stop")
    @patch("streamlit.error")
    def test_check_permission_insufficient_role(self, mock_error, mock_stop):
        check_permission(required_role="admin")
        mock_error.assert_called_once()
        mock_stop.assert_called_once()


class TestInMemoryRepository(unittest.TestCase):
    def setUp(self):
        # Cria um session_state limpo para cada teste
        self.session_dict = {}
        self.patcher = patch("streamlit.session_state", self.session_dict)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_init_demo_data_populates_session(self):
        init_demo_data()
        self.assertTrue(self.session_dict.get("demo_initialized"))
        self.assertIn("avaliacoes", self.session_dict)
        self.assertIn("denuncias", self.session_dict)
        self.assertIn("user_photos", self.session_dict)
        self.assertGreater(len(self.session_dict["avaliacoes"]), 0)
        self.assertGreater(len(self.session_dict["denuncias"]), 0)

    def test_get_and_insert_avaliacoes(self):
        df_initial = repo.get_all_avaliacoes()
        initial_count = len(df_initial)
        
        notas = {
            "comunicacao": 10.0, "empatia": 9.0, "capacidade_resolucao": 9.5,
            "conhecimento": 9.0, "trabalho_equipe": 8.5, "discricao": 9.0,
            "honestidade": 10.0, "paciencia": 9.0, "pontualidade": 10.0, "aura": 9.5
        }
        res = repo.insert_avaliacao("Kael", notas)
        self.assertTrue(res)

        df_updated = repo.get_all_avaliacoes()
        self.assertEqual(len(df_updated), initial_count + 1)
        self.assertEqual(df_updated.iloc[-1]["atendente"], "Kael")
        self.assertEqual(df_updated.iloc[-1]["comunicacao"], 10.0)

    def test_denuncias_crud_workflow(self):
        denuncias = repo.get_all_denuncias()
        initial_count = len(denuncias)

        # Inserção
        success = repo.insert_denuncia("user", "Milo", "Conduta inconsistente no atendimento.")
        self.assertTrue(success)

        user_denuncias = repo.get_denuncias_by_user("user")
        self.assertGreaterEqual(len(user_denuncias), 1)
        new_denuncia = user_denuncias[0]
        self.assertEqual(new_denuncia["denunciante"], "user")
        self.assertEqual(new_denuncia["status"], "em_analise")

        # Atualização de status
        denuncia_id = new_denuncia["id"]
        update_res = repo.update_denuncia_status(denuncia_id, "aceita", "Validado pela supervisão.")
        self.assertTrue(update_res)

        all_updated = repo.get_all_denuncias()
        target = next((d for d in all_updated if d["id"] == denuncia_id), None)
        self.assertIsNotNone(target)
        self.assertEqual(target["status"], "aceita")
        self.assertEqual(target["comentario_admin"], "Validado pela supervisão.")

    def test_user_photos_in_memory(self):
        repo.init_demo_state()
        photo = repo.get_user_profile_photo("Kael")
        self.assertIsNotNone(photo)
        self.assertIsInstance(photo, bytes)

        dummy_bytes = b"fake_photo_bytes_123"
        repo.save_user_profile_photo("testuser", dummy_bytes)
        retrieved = repo.get_user_profile_photo("testuser")
        self.assertEqual(retrieved, dummy_bytes)

    def test_reset_demo_data(self):
        repo.init_demo_state()
        # Modifica dados
        repo.insert_denuncia("temp_user", "temp_target", "temp_reason")
        self.assertGreater(len(repo.get_all_denuncias()), len(repo.INITIAL_DENUNCIAS_DATA))
        
        # Reset
        repo.reset_demo_data()
        self.assertEqual(len(repo.get_all_denuncias()), len(repo.INITIAL_DENUNCIAS_DATA))


if __name__ == "__main__":
    unittest.main()
