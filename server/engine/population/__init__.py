import random
import uuid
from datetime import datetime
from typing import List

from server.data import Person, PersonStats, Relation
from server.engine import simulation_engine


def cycle(people: List[Person], relations: List[Relation], current_time: datetime):
    if len(people) < 2:
        return

    free_people = list(filter(lambda p: p.is_alive and p.id not in map(lambda r: r.person2, relations) and p.id not in map(lambda r: r.person1, relations) and int(
        float((current_time - p.born).days) / (365.25)) > 18, people))

    if len(free_people) > 1:
        _mating(free_people, relations, current_time)
    if len(relations) > 0:
        _reproduction(people, relations, current_time)
    _health_checkup(people)


def _mating(free_people: List[Person], relations: List[Relation], current_time: datetime):
    for i in range(random.randint(0, len(free_people))):
        if len(free_people) < 2:
            return

        p1 = random.choice(free_people)
        free_people.remove(p1)
        non_incest_matches = \
            list(
                filter(
                    lambda r: not check_relations(r.id, list(filter(
                        lambda r: (r.person1 is p1.id) or (r.person2 is p1.id) or (p1 in r.children),
                        relations
                    ))),
                    free_people
                )
            )
        if len(non_incest_matches) < 1:
            return
        p2 = random.choice(non_incest_matches)
        free_people.remove(p2)

        relations.append(Relation(
            id="R-{}".format(uuid.uuid4().hex),
            person1=p1.id, person2=p2.id,
            children=[], is_active=True,
            start_date=current_time))


def check_relations(rid: str, relations_of_p1: List[Relation]):
    for r in relations_of_p1:
        if rid is r.person1 or rid is r.person2 or rid in r.children:
            return True
    return False


def _reproduction(people: List[Person], relations: List[Relation], current_time: datetime):
    for i in range(random.randint(0, int(len(relations)))):
        relation = relations[random.randint(0, len(relations)) - 1]
        child = _generate_person(current_time)
        people.append(child)
        relation.children.append(child)


def _health_checkup(people: List[Person]):
    for person in people:
        if person.health_issues is None:
            continue
        if person.health_issues.time_left == 0:
            person.health_issues = None
        else:
            person.health_issues.time_left = person.health_issues.time_left - 1


def _generate_person(current_time: datetime) -> Person:
    #identity = requests.get('https://api.namefake.com/').json()
    identity = {
        'name': 'tester test',
        'email_u': 'tester.test',
        'address': 'ezstrasse 76'
    }
    return Person(
        id="P-{}".format(uuid.uuid4().hex),
        firstname=identity['name'].split(' ')[0],
        lastname=identity['name'].split(' ')[1],
        address=identity['address'],
        email="{}@vmail.com".format(identity['email_u']),
        born=current_time,
        is_healthy=True,
        health=None,
        stats=_generate_stats()
    )


def _generate_stats() -> PersonStats:
    return PersonStats(
        strength=random.randint(0, 10),
        perception=random.randint(0, 10),
        endurance=random.randint(0, 10),
        charisma=random.randint(0, 10),
        intelligence=random.randint(0, 10),
        agility=random.randint(0, 10),
        luck=random.randint(0, 10)
    )
