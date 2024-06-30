import unittest
from app.services.deal_finder import find_deals


class TestDealFinder(unittest.TestCase):
    def test_deal_finder(self):
        find_deals(200, 'JBL')


if __name__ == '__main__':
    unittest.main()
