import unittest
from app.models import Comments

class CommentModelTest(unittest.TestCase):
    def setUp(self):
         self.new_comment = Comments(comment = "comments")

    def test_init(self):
        self.assertEqual(self.new_comment.comment,"comments") 