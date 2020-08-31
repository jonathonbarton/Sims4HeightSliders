# unpyc3: Decompiled file contains inaccuracies
from protocolbuffers import PersistenceBlobs_pb2
from server_commands.argument_helpers import get_optional_target, OptionalTargetParam, OptionalSimInfoParam
from sims.outfits.outfit_enums import OutfitCategory
from sims.sim_info import SimInfo
import services
import sims4.commands
import itertools
from statistics.commodity import Commodity
from statistics.commodity_tracker import CommodityTracker
from sims4.resources import Types
from statistics.base_statistic import BaseStatistic
import injector
import sims.sim
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from objects.object_enums import ResetReason
from objects import ALL_HIDDEN_REASONS

#First Comment for documentation
@sims4.commands.Command('add_slider', command_type=sims4.commands.CommandType.Live)
def randomize_facial_attributes(modifierstring:str, amount:float, opt_sim:OptionalSimInfoParam=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    if sim_info is None:
        return False
    facial_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
    facial_attributes.MergeFromString(sim_info.facial_attributes)
    modified_facial_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
    slider = PersistenceBlobs_pb2.BlobSimFacialCustomizationData().Modifier()
    slider2 = PersistenceBlobs_pb2.BlobSimFacialCustomizationData().Modifier()
    single = None
    pair = None
    if modifierstring == 'height':
        pair = list([13801231225349348340, 17657724757213773022])
    if modifierstring == 'neck':
        pair = list([13540934658970708314, 16656706900061866254])
    if modifierstring == 'teenheightslider':
        single = 6800132599074582568
    if modifierstring == 'hand':
        single = 17832649487024862641
    if modifierstring == 'bulge':
        single = 1655490812729882184
    if modifierstring == 'ths':
        single = 6800132599074582568
    if modifierstring == 'chs':
        pair = list([1280302701921808756, 15717958195565482356])
    if single is not None and pair is not None:
        output('Duplicate key!')
    if amount >= 0:
        if single is not None:
            slider.key = single
            slider.amount = amount*0.01
            ScumLog.log(str(slider.amount))
            if single == 1655490812729882184:
                get_stat(str(amount), opt_sim, _connection)
        if pair is not None:
            slider.key = pair[0]
            slider2.key = pair[1]
            slider.amount = amount*0.01
    elif pair is not None:
        slider.key = pair[1]
        slider2.key = pair[0]
        slider.amount = amount*-0.01
    for modifier in facial_attributes.face_modifiers:
        if modifier.key != slider2.key:
            modified_facial_attributes.face_modifiers.append(modifier)
    for modifier in facial_attributes.body_modifiers:
        modified_facial_attributes.body_modifiers.append(modifier)
    for sculpt in facial_attributes.sculpts:
        modified_facial_attributes.sculpts.append(sculpt)
    if slider.key is 0:
        output('Key is 0')
        return False
    modified_facial_attributes.face_modifiers.append(slider)
    sim_info.facial_attributes = modified_facial_attributes.SerializeToString()
    output('Applied Sim Attributes!')
    return True


@sims4.commands.Command('print_outfit_parts', command_type=sims4.commands.CommandType.Live)
def print_outfit_parts(opt_sim:OptionalSimInfoParam=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    tgt_client = services.client_manager().get(_connection)
    sim_info = tgt_client.active_sim.sim_info
    outfit = sim_info.get_outfit(OutfitCategory.EVERYDAY, 1)
    for idx in outfit.part_ids:
        output(str(idx))
    return True


@sims4.commands.Command('change_stat', command_type=sims4.commands.CommandType.Live)
def change_stat(inputVal:str=None, opt_sim:OptionalSimInfoParam=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    manager = services.get_instance_manager(Types.STATISTIC)
    bulge_stat_file = manager.get(16640)
    bulge_stat_commodity = sim_info.get_statistic(bulge_stat_file)
    bulge = float(inputVal)
    bulge_stat_commodity.set_value(bulge, add=True)


def setModifierWithSimInfo(modifierstring:str, amount:float, SimInfo):
    sim_info = SimInfo
    if sim_info is None:
        return False
    facial_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
    facial_attributes.MergeFromString(sim_info.facial_attributes)
    modified_facial_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
    slider = PersistenceBlobs_pb2.BlobSimFacialCustomizationData().Modifier()
    slider2 = PersistenceBlobs_pb2.BlobSimFacialCustomizationData().Modifier()
    single = None
    pair = None
    if modifierstring == 'height':
        pair = list([13801231225349348340, 17657724757213773022])
    if modifierstring == 'ths':
        single = 6800132599074582568
    if modifierstring == 'chs':
        pair = list([1280302701921808756, 15717958195565482356])
    if single is not None and pair is not None:
        output('Duplicate key!')
    if modifierstring == 'ths':
        slider.key = single
        tempamount = amount*0.01
        if tempamount < 0:
            tempamount = 0
        slider.amount = tempamount
    if amount >= 0:
        if single is not None:
            slider.key = single
            slider.amount = amount*0.01
        elif pair is not None:
            slider.key = pair[0]
            slider2.key = pair[1]
            slider.amount = amount*0.01
    elif pair is not None:
        slider.key = pair[1]
        slider2.key = pair[0]
        slider.amount = amount*-0.01
    for modifier in facial_attributes.face_modifiers:
        if modifier.key != slider2.key:
            modified_facial_attributes.face_modifiers.append(modifier)
    for modifier in facial_attributes.body_modifiers:
        modified_facial_attributes.body_modifiers.append(modifier)
    for sculpt in facial_attributes.sculpts:
        modified_facial_attributes.sculpts.append(sculpt)
    if slider.key is 0:
        return False
    modified_facial_attributes.face_modifiers.append(slider)
    sim_info.facial_attributes = modified_facial_attributes.SerializeToString()
    return True


def split_stat_name(motive_name):
    return str(motive_name).split('(')[1].split('@')[0]


def split_stat_type(motive_name):
    return str(motive_name).split('(')[0]


def split_value(motive_name):
    return str(motive_name).split('(')[1].split('@')[1].split(')')[0]

