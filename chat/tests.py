# chat/tests.py
"""
Unit tests for Chat App - DjangoChat project.
"""
from mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from chat.models import ChatMessage
from chat.utils import user_sanitizer, get_last_messages, process_msg


class UtilsTests(TestCase):
    """
    Utilities module - Unit tests
    """
    def setUp(self):
        self.anonymous = AnonymousUser()
        self.user_1 = User.objects.create(username='user_1')
        ChatMessage.objects.create(user=self.user_1, message='Hello1!')
        ChatMessage.objects.create(user=self.user_1, message='Hello2!')
        ChatMessage.objects.create(user=self.user_1, message='Hello3!')
        ChatMessage.objects.create(user=self.user_1, message='Room2', room='room2')

    def test_user_sanitizer_1(self):
        """Test user_sanitizer with instance of AnonymousUser as input"""
        self.assertEqual(user_sanitizer(self.anonymous), 'Bot')

    def test_user_sanitizer_2(self):
        """Test user_sanitizer with instance of User as input"""
        self.assertEqual(user_sanitizer(self.user_1), 'user_1')

    def test_get_last_messages_1(self):
        """Test get_last_messages from room with 3 messages"""
        self.assertEqual(get_last_messages('lobby'), 'Hello1!\nHello2!\nHello3!\n')

    def test_get_last_messages_2(self):
        """Test get_last_messages from empty room"""
        self.assertEqual(get_last_messages('room1'), '')

    def test_get_last_messages_3(self):
        """Test get_last_messages from room with one message"""
        self.assertEqual(get_last_messages('room2'), 'Room2\n')

    def test_process_msg_1(self):
        """Test process_msg  with message starting with '/' calls publish_request function"""
        with patch('chat.utils.publish_request'
                   ) as mock_process_msg:
            process_msg('/stock=AAPL', self.user_1, 'lobby')
            mock_process_msg.assert_called_once()
            mock_process_msg.assert_called_with('{"message": "/stock=AAPL", "room": "lobby"}')

    def test_process_msg_2(self):
        """Test process_msg with regular message stores in database."""
        process_msg('This message!', self.user_1, 'room1')
        self.assertEqual(1, ChatMessage.objects.filter(message='user_1: This message!').count())
