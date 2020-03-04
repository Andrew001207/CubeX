import logging
import configparser
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigAware():
    '''Subclass from this to get access to the config'''
    def __init__(self):
        # Read configfile
        config = configparser.ConfigParser()

        config_path = 'cert/config.ini'

        # create a parser
        config.read(config_path)

        try:
            self.conf_db = dict(config['postgresql'])
            self.conf_bot_token = config['bot']['token']
            self.conf_aws = dict(config['AwsConnector'])
        except KeyError:
            raise Exception('A nessecary section was not found in the {0} file'.format(config_path))

        logger.debug('Read config')
