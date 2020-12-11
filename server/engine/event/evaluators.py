import server.engine.util as engine_utils


def event_evaluate_catastrophe(event: object):
    engine_utils.assert_section(event, 'injury')
