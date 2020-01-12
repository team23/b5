import unittest

from b5.lib.config import ConfigHandler


class TestConfig(unittest.TestCase):

    def test_load_configs(self):
        handler = ConfigHandler()

        config = handler.load('../', ['stubs/config.yml'])

        self.assertEqual('test-project', config['project']['key'])

    def test_multiple_configs_will_be_loaded(self):
        handler = ConfigHandler()
        config = handler.load('../', [
            'stubs/config.yml',
            'stubs/config2.yml',
        ])

        self.assertEqual('test-project', config['project']['key'])
        self.assertEqual('overwritten-path', config['paths']['web'])

    def test_returns_empty_dict_on_not_existing_config_file(self):
        handler = ConfigHandler()
        config = handler.load_config_file('.', 'not_existing_config.yml')
        self.assertEqual({}, config)

    def test_merges_configs(self):
        a = {
            'a': 1,
            'b': {
                'b1': 2,
                'b2': 3,
            },
        }
        b = {
            'a': 1,
            'b': {
                'b1': 4,
            },
        }

        self.assertEqual(ConfigHandler.merge_config(a, b)['a'], 1)
        self.assertEqual(ConfigHandler.merge_config(a, b)['b']['b2'], 3)
        self.assertEqual(ConfigHandler.merge_config(a, b)['b']['b1'], 4)

    def test_inserts_new_keys(self):
        a = {
            'a': 1,
            'b': {
                'b1': 2,
                'b2': 3,
            },
        }
        b = {
            'a': 1,
            'b': {
                'b1': 4,
                'b3': 5
            },
            'c': 6,
        }

        self.assertEqual(ConfigHandler.merge_config(a, b)['a'], 1)
        self.assertEqual(ConfigHandler.merge_config(a, b)['b']['b2'], 3)
        self.assertEqual(ConfigHandler.merge_config(a, b)['b']['b1'], 4)
        self.assertEqual(ConfigHandler.merge_config(a, b)['b']['b3'], 5)
        self.assertEqual(ConfigHandler.merge_config(a, b)['c'], 6)


if __name__ == '__main__':
    unittest.main()
