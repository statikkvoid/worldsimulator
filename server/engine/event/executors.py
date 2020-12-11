import random
from typing import List

from server.data import Event, Person, PersonHealth, Relation


def event_execute_catastrophe(event: Event, people_affected: List[Person], relations: List[Relation]):
    injury_description = event.event['injury']['description']
    injury_chance = event.event['injury']['chance']
    injury_duration = event.event['injury']['duration']
    injury_death_chance = event.event['injury']['death_chance']

    people_injured_amount = int(round((float(injury_chance) / 100) * len(people_affected)))
    if people_injured_amount < 1:
        return

    people_injured = random.sample(people_affected, people_injured_amount)

    for person in people_injured:
        person.health_issues = PersonHealth(injury=injury_description, time_left=injury_duration)

    people_to_die_amount = int(round((float(injury_death_chance) / 100) * people_injured_amount))
    if people_to_die_amount < 1:
        return

    people_to_die = random.sample(people_injured, people_to_die_amount)

    for person in people_to_die:
        person.is_alive = False
        for r in filter(lambda r: r.person1 == person.id or r.person2 == person.id, relations):
            r.is_active = False



