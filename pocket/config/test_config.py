import unittest
from pocket.config.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.test_file1 = './test_data/config1.yaml'
        self.test_file2 = './test_data/config2.yaml'

    def test_config(self):
        # good config file
        c = Config(self.test_file1)
        self.assertTrue('name' in c.args)
        self.assertTrue('image' in c.args)

        # bad config file
        self.assertRaises(ValueError, lambda: Config(self.test_file2))


if __name__ == '__main__':
    unittest.main()
