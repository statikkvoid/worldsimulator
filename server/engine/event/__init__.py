import math
import uuid
import random

from typing import List

import server.engine.util as engine_utils

import server.engine.event.evaluators as evaluators
import server.engine.event.executors as executors

from server.data import Event, Person, Relation
from server.engine import simulation_engine

_event_queue: List[Event] = []


def cycle(people: List[Person], relations: List[Relation]):
    for event in _event_queue:
        if event.days_left is None:
            event.days_left = int(event.event['general']['duration'])
        elif event.days_left <= simulation_engine.TICK_LENGTH:
            _event_queue.remove(event)
            for p in people:
                if event.id in p.affected_by:
                    p.affected_by.remove(event.id)
            continue
        else:
            event.days_left = event.days_left - simulation_engine.TICK_LENGTH

        affected = event.event['general']['affected']

        people_possible_affected = list(filter(lambda p: event.id not in p.affected_by, people))

        people_affected_amount = int(math.floor((float(affected) / 100) * len(people_possible_affected)))
        if people_affected_amount < 1:
            continue

        if len(people_possible_affected) < 1:
            continue

        people_affected = random.sample(people_possible_affected, people_affected_amount)

        for person in people_affected:
            person.affected_by.append(event.id)

        _event_executors[event.event['general']['type']](event, people_affected, relations)


def has_events():
    return len(_event_queue) > 0


def print_events():
    print("\033[1mEvents: ({})\033[0m".format(len(_event_queue)))
    for i in _event_queue:
        print("  Event: {} ({}) has {} days left".format(i.id, i.event['general']['name'], i.days_left))


def add(event_id: str):
    event = engine_utils.read_event(event_id)
    engine_utils.assert_section(event, 'general')

    _event_evaluators[event['general']['type']](event)

    _event_queue.append(Event(id=uuid.uuid4().hex, name=event['general']['name'], event=event, weeks_left=None))


def get_events():
    return dict(_event_queue)


_event_evaluators = {
    "catastrophe": evaluators.event_evaluate_catastrophe,
}

_event_executors = {
    "catastrophe": executors.event_execute_catastrophe,
}