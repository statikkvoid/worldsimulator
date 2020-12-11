import time
import threading
from datetime import datetime, timedelta

from server.engine import event, population

_current_time = datetime.now()

_people = []
_relations = []

TICK_LENGTH = 365


def start():
    for i in range(2):
        _people.append(population._generate_person(_current_time))
    t = threading.Thread(target=_cycle)
    t.start()


def _cycle():
    global _current_time
    event.add('storm')
    while True:

        # get DB data

        # do stuff
        population.cycle(_people, _relations, _current_time)
        event.cycle(_people, _relations)

        # Add one tick (1 day at the moment)
        _current_time = _current_time + timedelta(days=TICK_LENGTH)

        active_relations = list(filter(lambda r: r.is_active, _relations))
        people_alive = list(filter(lambda p: p.is_alive, _people))

        if len(people_alive) < 1:
            print("---------------------------------------------------------------------")
            print("\033[1mCONGRATULATIONS! YOUR POPULATION FUCKING DIED\033[1m")
            print("---------------------------------------------------------------------")
            break

        if event.has_events():
            event.print_events()

        print("Population Count: {}".format(len(_people)))
        print("Date: {}".format(_current_time))

        if len(people_alive) > 0:
            print("\033[1mPopulation: {}\033[0m".format(
                '({} dead)'.format(
                    len(_people) - len(people_alive)) if len(_people) - len(people_alive) > 1 else ''))
            for i in people_alive:
                print("  Person: {}, Age: {} days (~{} years), Affected By: {}, Health: {}".format(
                    i.id, (_current_time - i.born).days, round((_current_time - i.born).days / 365), i.affected_by, i.health_issues))

        if len(active_relations) > 0:
            print("\033[1mRelations: {}\033[0m".format(
                '({} inactive)'.format(
                    len(_relations) - len(active_relations)) if len(_relations) - len(active_relations) > 0 else ''))
            for i in active_relations:
                print("  Relation: {} is between {} and {}".format(i.id, i.person1, i.person2))

        print("---------------------------------------------------------------------")

        # persist DB data
        time.sleep(1)


def get_population():
    return _people


def get_relations():
    return _relations


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


def get_time():
    return _current_time