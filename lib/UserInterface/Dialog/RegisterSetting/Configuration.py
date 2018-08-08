# encoding: utf-8
freq_point_config = [
    # init_item(name, tx, rx):
    ('User0', 0x606800E8, 0x606800D8),
    ('User1', 0x606800EC, 0x606800DC),
    ('User2', 0x606800F0, 0x606800E0),
    ('User3', 0x606800F4, 0x606800E4),
    ('CS', 0x606800F8, ''),
    ('BR', 0x606800D0, ''),
]

RF_channel_config = [
    # init_item(name, tx, rx):
    ('User0', (0x60680151, 6), (0x60680150, 7)),
    ('User1', (0x60680158, 6), (0x60680158, 7)),
    ('User2', (0x60680160, 6), (0x60680160, 7)),
    ('User3', (0x60680168, 6), (0x60680168, 7)),
    ('CS', (0x60680178, 6), (0x60680178, 7)),
    ('BR', (0x60680188, 6), (0x60680188, 7)),
    ('FS', (None, None), (0x60680180, 7)),
]

PA_config = [
    # def init_item(name, t2_0, t2_1, t5_0, t5_1):
    ('User0', (0x60680157, 0), (0x60680157, 1), (0x60680157, 2), (0x60680157, 3)),
    ('User1', (0x6068015F, 0), (0x6068015F, 1), (0x6068015F, 2), (0x6068015F, 3)),
    ('User2', (0x60680167, 0), (0x60680167, 1), (0x60680167, 2), (0x60680167, 3)),
    ('User3', (0x6068016F, 0), (0x6068016F, 1), (0x6068016F, 2), (0x6068016F, 3)),
    ('CS', (0x6068017F, 0), (None, None), (0x6068017F, 2), (None, None)),
    ('BR', (0x6068018F, 0), (None, None), (0x6068018F, 2), (None, None)),

]

baseband_power_config = [

    # def init_item(name, address, title):
    ('all_user_aerial_0_power', 0x60680020, u"所有用户天线0功率:"),
    ('all_user_aerial_1_power', 0x60680021, u"所有用户天线1功率:"),
    ('br_cs_aerial_0_power', 0x60680025, u"BR/CS天线0功率:"),

]
