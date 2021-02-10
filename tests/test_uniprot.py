import pytest
import unittest


class TestUniprot(unittest.TestCase):
    """ Tests
    """

    def setUp(self):
        """Set up
        Loads a model
        """
        self.protein = 'P15993'

    @pytest.mark.webtest
    def test_retreive_uniprot(self):
        """Tests essential reactions
        """
        from dummy.util.uniprot import retreive
        r = retreive(self.protein, format='dict')
        self.assertEqual(len(r.keys()), 3)

    @pytest.mark.xfail
    def test_feature_a(self):
        self.assertEqual(2, 3)
