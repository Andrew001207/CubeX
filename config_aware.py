import configparser
#TODO logger shebang usw...
class ConfigAware():
    '''Subclass from this to get access to the config'''
    def __init__(self):
        # Read configfile
        config = configparser.ConfigParser()

        config_path = 'cert/config.ini'

        # create a parser
        config.read(config_path)

        # read config file
        try:
            self.conf_db = dict(config['postgresql'])
            self.conf_bot_token = config['bot']['token']
            self.conf_aws = dict(config['AwsConnector'])
        except KeyError:
            raise Exception('A nessecary section was not found in the {0} file'.format(config_path))
