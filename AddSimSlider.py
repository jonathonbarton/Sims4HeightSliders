# Python bytecode 3.3 (3230)
# Embedded file name: AddSimSlider.py
# Compiled at: 2017-06-01 20:31:28
# Size of source mod 2**32: 12084 bytes
from protocolbuffers import PersistenceBlobs_pb2
from server_commands.argument_helpers import get_optional_target, OptionalTargetParam, OptionalSimInfoParam
from sims.outfits.outfit_enums import OutfitCategory
from sims.sim_info import SimInfo
import services, sims4.commands, itertools
from statistics.commodity import Commodity
from statistics.commodity_tracker import CommodityTracker
from sims4.resources import Types
from statistics.base_statistic import BaseStatistic
import injector, sims.sim
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from objects.object_enums import ResetReason
from objects import ALL_HIDDEN_REASONS

@sims4.commands.Command('add_slider', command_type=sims4.commands.CommandType.Live)
def randomize_facial_attributes(modifierstring: None, amount: None, opt_sim: OptionalSimInfoParam=None, _connection=None):
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
        pair = list([13801231225349348340L, 17657724757213773022L])
    if modifierstring == 'neck':
        pair = list([13540934658970708314L, 16656706900061866254L])
    if modifierstring == 'teenheightslider':
        single = 6800132599074582568L
    if modifierstring == 'hand':
        single = 17832649487024862641L
    if modifierstring == 'bulge':
        single = 1655490812729882184L
    if modifierstring == 'ths':
        single = 6800132599074582568L
    if modifierstring == 'chs':
        pair = list([1280302701921808756L, 15717958195565482356L])
    if single is not None:
        if pair is not None:
            output('Duplicate key!')
    if amount >= 0:
        if single is not None:
            slider.key = single
            slider.amount = amount * 0.01
            if single == 1655490812729882184L:
                get_stat(str(amount), opt_sim, _connection)
        if pair is not None:
            slider.key = pair[0]
            slider2.key = pair[1]
            slider.amount = amount * 0.01
    else:
        if amount < 0:
            if pair is not None:
                slider.key = pair[1]
                slider2.key = pair[0]
                slider.amount = amount * -0.01
        for modifier in facial_attributes.face_modifiers:
            if modifier.key != slider2.key:
                modified_facial_attributes.face_modifiers.append(modifier)
                continue

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
def print_outfit_parts(opt_sim: OptionalSimInfoParam=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    tgt_client = services.client_manager().get(_connection)
    sim_info = tgt_client.active_sim.sim_info
    outfit = sim_info.get_outfit(OutfitCategory.EVERYDAY, 1)
    for idx in outfit.part_ids:
        output(str(idx))

    return True


@sims4.commands.Command('change_stat', command_type=sims4.commands.CommandType.Live)
def change_stat(inputVal: str=None, opt_sim: OptionalSimInfoParam=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    manager = services.get_instance_manager(Types.STATISTIC)
    bulge_stat_file = manager.get(16640)
    bulge_stat_commodity = sim_info.get_statistic(bulge_stat_file)
    bulge = float(inputVal)
    bulge_stat_commodity.set_value(bulge, add=True)
    output('Set bulge stat')
    return True


@injector.inject_to(sims.sim.Sim, 'on_outfit_changed')
def log_outfit_change(original, self, sim_info, category_and_index):
    outfit_data = sim_info.get_outfit(*category_and_index)
    original(self, sim_info, category_and_index)
    bool = False
    manager = services.get_instance_manager(Types.STATISTIC)
    bulge_stat_file = manager.get(16025366513249183958L)
    if bulge_stat_file != None:
        bulge_stat_commodity = sim_info.get_statistic(bulge_stat_file)
        bulge_showing_parts = [
         69624, 69625, 69626, 69627, 69628, 69629, 69630, 69631, 69632, 68004, 68005, 68006, 68007, 68008, 68009, 68010, 68011, 68012, 67988, 67989, 67990, 67991, 67992, 67993, 67994, 67995, 67996, 67997, 67998, 67999, 68000, 68001, 68002, 68003, 92345, 92346, 92347, 92348, 92349, 92350, 92351, 92352, 92353, 92354, 92355, 92356, 92357, 92358, 92359, 92360, 92361, 92362, 92363, 92364, 92365, 92366, 92367, 92368, 92369, 92370, 92371, 92372, 92373, 92374, 92375, 92376, 92377, 92378, 92379, 92380, 94592, 94593, 94594, 94595, 94596, 94597, 94598, 94599, 94600, 94601, 24539, 24740, 24741, 24742, 83929, 83930, 83931, 83932]
        for part in outfit_data.part_ids:
            for bulge_cas_part in bulge_showing_parts:
                if part == bulge_cas_part:
                    bool = True

        if bool is True:
            set_bulginess('bulge', bulge_stat_commodity, sim_info)
        else:
            set_bulginess('bulge', 'Commodity(Theo_SliderMod_BulgeSlider@0.0)', sim_info)
    return


def set_bulginess(modifierstring: str,
                  amount2: str, sim_info):
    amount = float(split_value(amount2))
    if sim_info is None:
        return False
    else:
        facial_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
        facial_attributes.MergeFromString(sim_info.facial_attributes)
        modified_facial_attributes = PersistenceBlobs_pb2.BlobSimFacialCustomizationData()
        slider = PersistenceBlobs_pb2.BlobSimFacialCustomizationData().Modifier()
        slider2 = PersistenceBlobs_pb2.BlobSimFacialCustomizationData().Modifier()
        single = None
        pair = None
        if modifierstring == 'bulge':
            single = 1655490812729882184L
        if amount >= 0:
            if single is not None:
                slider.key = single
                slider.amount = amount * 0.01
            if pair is not None:
                slider.key = pair[0]
                slider2.key = pair[1]
                slider.amount = amount * 0.01
        for modifier in facial_attributes.face_modifiers:
            modified_facial_attributes.face_modifiers.append(modifier)

        for modifier in facial_attributes.body_modifiers:
            modified_facial_attributes.body_modifiers.append(modifier)

        for sculpt in facial_attributes.sculpts:
            modified_facial_attributes.sculpts.append(sculpt)

        if slider.key is 0:
            return False
        modified_facial_attributes.face_modifiers.append(slider)
        sim_info.facial_attributes = modified_facial_attributes.SerializeToString()
        return


def setModifierWithSimInfo(modifierstring: str,
                           amount: float, SimInfo):
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
        pair = list([13801231225349348340L, 17657724757213773022L])
    if modifierstring == 'ths':
        single = 6800132599074582568L
    if modifierstring == 'chs':
        pair = list([1280302701921808756L, 15717958195565482356L])
    if single is not None:
        if pair is not None:
            output('Duplicate key!')
    if modifierstring == 'ths':
        slider.key = single
        tempamount = amount * 0.01
        if tempamount < 0:
            tempamount = 0
        slider.amount = tempamount
    if amount >= 0:
        if single is not None:
            slider.key = single
            slider.amount = amount * 0.01
        if pair is not None:
            slider.key = pair[0]
            slider2.key = pair[1]
            slider.amount = amount * 0.01
    else:
        if amount < 0:
            if pair is not None:
                slider.key = pair[1]
                slider2.key = pair[0]
                slider.amount = amount * -0.01
        for modifier in facial_attributes.face_modifiers:
            if modifier.key != slider2.key:
                modified_facial_attributes.face_modifiers.append(modifier)
                continue

        for modifier in facial_attributes.body_modifiers:
            modified_facial_attributes.body_modifiers.append(modifier)

        for sculpt in facial_attributes.sculpts:
            modified_facial_attributes.sculpts.append(sculpt)

        if slider.key is 0:
            return False
        modified_facial_attributes.face_modifiers.append(slider)
        sim_info.facial_attributes = modified_facial_attributes.SerializeToString()
        return True


def get_stat(inputVal: str=None,
             opt_sim: OptionalSimInfoParam=None, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    sim_info = get_optional_target(opt_sim, target_type=OptionalSimInfoParam, _connection=_connection)
    manager = services.get_instance_manager(Types.STATISTIC)
    bulge_stat_file = manager.get(16025366513249183958L)
    bulge_stat_commodity = sim_info.get_statistic(bulge_stat_file)
    bulge = float(inputVal)
    bulge_stat_commodity.set_value(bulge, add=True)
    output('Set bulge stat')
    return True


def split_stat_name(motive_name):
    return str(motive_name).split('(')[1].split('@')[0]


def split_stat_type(motive_name):
    return str(motive_name).split('(')[0]


def split_value(motive_name):
    return str(motive_name).split('(')[1].split('@')[1].split(')')[0]
