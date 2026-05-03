import unittest
from unittest.mock import MagicMock
from services.player_service import PlayerService
from models.entities import PlayerEntity

class TestPlayerService(unittest.TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = PlayerService(self.mock_repo)

    def test_login_fail_user_not_found(self):
        """Test login fails when user is not found in DB."""
        self.mock_repo.get_by_username.return_value = None
        
        result = self.service.login_player("cineva", "parola")
        self.assertIsNone(result)

    def test_save_player_state_calls_repo(self):
        """Test save player state calls repository to save the player."""

        mock_player = MagicMock()
        mock_player.name = "andrei"
        mock_player.balance = 1500.0
        
        mock_entity = PlayerEntity(username="andrei", balance=1000.0)
        self.mock_repo.get_by_username.return_value = mock_entity
        
        self.service.save_player_state(mock_player)
        
        self.assertEqual(mock_entity.balance, 1500.0)
        self.mock_repo.save.assert_called_once_with(mock_entity)