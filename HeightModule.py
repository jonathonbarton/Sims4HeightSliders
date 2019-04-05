# Python bytecode 3.3 (3230)
# Embedded file name: HeightModule.py
# Compiled at: 2016-02-17 11:41:31
# Size of source mod 2**32: 6798 bytes
import AddSimSlider, services, injector, traits.trait_tracker, random, sims.sim_info, sims4.commands
from server_commands.argument_helpers import get_optional_target, OptionalTargetParam, OptionalSimInfoParam
from sims.sim_info_types import Age
from sims4.resources import Types
from sims.sim_info import SimInfo
import zone, alarms, clock, date_and_time

def randomizeHeightIfDefault(sim_info):
    trait = services.trait_manager().get(15258887174838921384L)
    hastrait = sim_info.trait_tracker.has_trait(trait)
    if hastrait is False:
        if trait is None:
            return
        sim_info.add_trait(trait)
        howTall = random.randrange(0, 13)
        if howTall <= 5:
            HEIGHT = 'AVERAGE'
        if howTall > 5 and howTall < 8:
            HEIGHT = 'TALL'
        if howTall >= 8 and howTall < 11:
            HEIGHT = 'SHORT'
        if howTall == 11:
            HEIGHT = 'VERYSHORT'
        if howTall == 12:
            HEIGHT = 'VERYTALL'
        manager = services.get_instance_manager(Types.STATISTIC)
        stat_file = manager.get(18157023230166068511L)
        stat_commodity = sim_info.get_statistic(stat_file)
        if HEIGHT == 'AVERAGE':
            randHeight = random.randrange(-35, 35)
        else:
            if HEIGHT == 'SHORT':
                randHeight = random.randrange(-60, -35)
            else:
                if HEIGHT == 'TALL':
                    randHeight = random.randrange(35, 60)
                else:
                    if HEIGHT == 'VERYTALL':
                        randHeight = random.randrange(60, 100)
                    else:
                        if HEIGHT == 'VERYSHORT':
                            randHeight = random.randrange(-100, -60)
                        stat_commodity.set_value(randHeight, add=True)
                        AddSimSlider.setModifierWithSimInfo('height', randHeight, sim_info)
    return


@sims4.commands.Command('sa', command_type=sims4.commands.CommandType.Live)
def randomize_facial_attributes(amount: None, opt_sim: OptionalSimInfoParam=None, _connection=None):
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    sim_info._age_progress.set_value(amount + sim_info.age_progress)
    sim_info.send_age_progress()


@sims4.commands.Command('rhall', command_type=sims4.commands.CommandType.Live)
def SimGrowthCommand():
    trait = services.trait_manager().get(15258887174838921384L)
    if trait != None:
        SimGrowth(None)
    return


@sims4.commands.Command('rhone', command_type=sims4.commands.CommandType.Live)
def SimGrowthCommand(opt_sim: OptionalSimInfoParam=None, _connection=None):
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    trait = services.trait_manager().get(15258887174838921384L)
    if trait != None:
        SimGrowthOneSim(sim_info)
    return


def SimGrowth(_):
    ageSpeed = services.get_age_service().aging_speed
    pop = 0
    if not services.get_age_service()._unplayed_aging_enabled:
        ageSpeed = None
    for sim_info in services.sim_info_manager().get_all():
        pop = pop + 1
        sim_age = sim_info._days_until_ready_to_age()
        SimAge = sim_info.age
        randomizeHeightIfDefault(sim_info)
        manager = services.get_instance_manager(Types.STATISTIC)
        stat_file = manager.get(18157023230166068511L)
        stat_commodity = sim_info.get_statistic(stat_file)
        simHeightStat = stat_commodity.get_value()
        if SimAge == Age.CHILD:
            childHeightSlider = 15.36 * sim_age + simHeightStat - 100
            teenHeightSlider = 0
            height = None
        else:
            if SimAge == Age.TEEN:
                teenHeightSlider = 7.68 * sim_age
                childHeightSlider = 0
                height = None
            else:
                if SimAge == Age.YOUNGADULT or SimAge == Age.ADULT or SimAge == Age.ELDER:
                    height = None
                    teenHeightSlider = 0
                    childHeightSlider = 0
        if height is not None:
            AddSimSlider.setModifierWithSimInfo('height', height, sim_info)
        if childHeightSlider is not None:
            AddSimSlider.setModifierWithSimInfo('chs', childHeightSlider, sim_info)
        if teenHeightSlider is not None:
            AddSimSlider.setModifierWithSimInfo('ths', teenHeightSlider, sim_info)
            continue

    return


def SimGrowthOneSim(sim_info=None):
    ageSpeed = services.get_age_service().aging_speed
    pop = 0
    if not services.get_age_service()._unplayed_aging_enabled:
        ageSpeed = None
    if sim_info is not None:
        pop = pop + 1
        ScumLog.log('1')
        sim_age = sim_info._days_until_ready_to_age()
        SimAge = sim_info.age
        randomizeHeightIfDefault(sim_info)
        manager = services.get_instance_manager(Types.STATISTIC)
        stat_file = manager.get(18157023230166068511L)
        stat_commodity = sim_info.get_statistic(stat_file)
        simHeightStat = stat_commodity.get_value()
        if SimAge == Age.CHILD:
            childHeightSlider = 15.36 * sim_age + simHeightStat - 100
            teenHeightSlider = 0
        else:
            if SimAge == Age.TEEN:
                teenHeightSlider = 7.68 * sim_age
                childHeightSlider = 0
            else:
                if SimAge == Age.YOUNGADULT or SimAge == Age.ADULT or SimAge == Age.ELDER:
                    teenHeightSlider = 0
                    childHeightSlider = 0
        if childHeightSlider is not None:
            AddSimSlider.setModifierWithSimInfo('chs', childHeightSlider, sim_info)
        if teenHeightSlider is not None:
            AddSimSlider.setModifierWithSimInfo('ths', teenHeightSlider, sim_info)
    return


height_alarm = None

def height_alarm_set():
    global height_alarm
    if height_alarm is not None:
        alarms.cancel_alarm(height_alarm)
        height_alarm = None
    time_service = services.time_service()
    time = date_and_time.create_date_and_time(hours=1)
    span2 = time_service.sim_now.time_till_next_day_time(time)
    span = clock.interval_in_sim_days(1)
    height_alarm = alarms.add_alarm(height_alarm_set, span2, SimGrowth, repeating=True, repeating_time_span=span, use_sleep_time=True)
    return


@injector.inject_to(zone.Zone, 'on_hit_their_marks')
def height_on_their_marks(original, self):
    original(self)
    trait = services.trait_manager().get(15258887174838921384L)
    if trait != None:
        height_alarm_set()
    return
