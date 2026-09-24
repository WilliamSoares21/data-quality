"""
Suíte de Testes Unitários de Segurança e Arquitetura.
Valida o comportamento da guarda RBAC, sanitização de Path Traversal, Hashing de Senhas e Repositório.
"""

import unittest
from unittest.mock import MagicMock, patch
import os

from utils.security import sanitize_filename, validate_uploaded_file, get_safe_filepath
from utils.auth import hash_password, verify_password, check_permission
import database.repository as repo

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

if __name__ == "__main__":
    unittest.main()
