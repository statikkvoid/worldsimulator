import configparser

from server.engine import SimulationEngineError


def read_event(event_id: str):
    config = configparser.ConfigParser()
    config.read('events/{}.evt'.format(event_id))
    return config


def assert_section(event: object, section: str):
    if section not in event:
        raise SimulationEngineError("No '{}' section in event config file".format(section))