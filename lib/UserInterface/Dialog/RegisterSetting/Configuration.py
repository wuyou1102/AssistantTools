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

user_interleave_config = [
    # def __init__(self, item):
    {
        'name': 'user_interleave_send',
        'title': u'用户发送',
        'total_address': {
            'user0': (0x60680004, 0, 2),
            'user1': (0x60680008, 0, 2),
            'user2': (0x6068000C, 0, 2),
            'user3': (0x60680010, 0, 2),
        },
        'mode_address': {
            'user0': (0x60680015, 0, 2),
            'user1': (0x60680038, 0, 2),
            'user2': (0x60680039, 3, 5),
            'user3': (0x60680039, 0, 2),
        },
    },
    {
        'name': 'user_interleave_recv',
        'title': u'用户接收',
        'total_address': {
            'user0': (0x60680150, 0, 2),
            'user1': (0x60680158, 0, 2),
            'user2': (0x60680160, 0, 2),
            'user3': (0x60680168, 0, 2),
        },
        'mode_address': {
            'user0': (0x60680151, 3, 5),
            'user1': (0x60680159, 3, 5),
            'user2': (0x60680161, 3, 5),
            'user3': (0x60680169, 3, 5),
        },
    },
]
br_interleave_config = [
    {
        'name': 'br_interleave_send',
        'title': u'BR发送',
        'total_address': (0x60680017, 5, 7)
    },
    {
        'name': 'br_interleave_recv',
        'title': u'BR接收',
        'total_address': (0x60680188, 0, 2)
    },
]

MCS_config = [
    {
        'name': 'user0_send',
        'title': u'User0发送',
        'modem': (0x60680004, 3, 5),
        'encode': (0x60680005, 0, 2),
        'repeat': (0x60680005, 3, 5),
    },
    {
        'name': 'user1_send',
        'title': u'User1发送',
        'modem': (0x60680008, 3, 5),
        'encode': (0x60680009, 0, 2),
        'repeat': (0x60680009, 3, 5),
    },
    {
        'name': 'user2_send',
        'title': u'User2发送',
        'modem': (0x6068000C, 3, 5),
        'encode': (0x6068000D, 0, 2),
        'repeat': (0x6068000D, 3, 5),
    },
    {
        'name': 'user3_send',
        'title': u'User3发送',
        'modem': (0x60680010, 3, 5),
        'encode': (0x60680011, 0, 2),
        'repeat': (0x60680011, 3, 5),
    },
    {
        'name': 'cs_recv',
        'title': u'CS接收',
        'modem': (0x60680178, 3, 5),
        'encode': (0x6068017A, 4, 7),
        'repeat': (0x60680179, 0, 2),
    },
    {
        'name': 'br_recv',
        'title': u'BR接收',
        'modem': (0x60680188, 3, 5),
        'encode': (0x6068018A, 4, 7),
        'repeat': (0x60680189, 0, 2),
    },
    {
        'name': 'br_send',
        'title': u'BR发送',
        'modem': (0x60680017, 4, -1),
        'encode': (0x60680017, 3, -1),
        'repeat': (0x60680016, 4, 6),
    },
]

br_cs_bandwidth_config = {
    'name': 'br_cs_bandwidth',
    'BR': {
        'title': u'BR',
        'recv_address': (0x6068018B, 0, 2),
        'send_address': (0x6068017B, 0, 2),
    },
    'CS': {
        'title': u'CS',
        'recv_address': (0x6068017B, 0, 2),
        'send_address': (0x6068017B, 0, 2),
    }
}

user_bandwidth_config = {
    'name': 'user_bandwidth',
    'title': u'用户',
    'recv_address': {
        'user0': (0x60680153, 0, 2),
        'user1': (0x6068015E, 0, 2),
        'user2': (0x60680163, 0, 2),
        'user3': (0x6068016B, 0, 2),
    },
    'send_address': {
        'user0': (0x60680007, 0, 2),
        'user1': (0x6068000B, 0, 2),
        'user2': (0x6068000F, 0, 2),
        'user3': (0x60680013, 0, 2),
    },
}
antenna_mode_config = {
    'name': 'antenna_mod',
    'send': {
        'title': u'发送端天线配置：',
        'address': (0x60680014, 3, -1),
    },
    'recv': {
        'title': u'接收端天线配置：',
        'address': (0x6068020A, 4, 5),
    },
}

slot_mimo_mode_config = {
    'name': 'slot_mimo_mode',
    'user0': {
        'title': u'用户0 接收方式：',
        'address': (0x60680152, 0, 2),
    },
    'user1': {
        'title': u'用户1 接收方式：',
        'address': (0x6068015A, 0, 2),
    },
    'user2': {
        'title': u'用户2 接收方式：',
        'address': (0x60680162, 0, 2),
    },
    'user3': {
        'title': u'用户3 接收方式：',
        'address': (0x6068016A, 0, 2),
    },

}
lock_config = [
    {
        'name': 'usr0_lock',
        'title': 'User0',
        'fch': ('FCH', (0x606800B3, 7, -1)),
        'slot': ('SLOT', (0x606800B3, 6, -1)),
    },
    {
        'name': 'usr1_lock',
        'title': 'User1',
        'fch': ('FCH', (0x606800B3, 5, -1)),
        'slot': ('SLOT', (0x606800B3, 4, -1)),
    },
    {
        'name': 'usr2_lock',
        'title': 'User2',
        'fch': ('FCH', (0x606800B3, 3, -1)),
        'slot': ('SLOT', (0x606800B3, 2, -1)),
    },
    {
        'name': 'usr3_lock',
        'title': 'User3',
        'fch': ('FCH', (0x606800B3, 1, -1)),
        'slot': ('SLOT', (0x606800B3, 0, -1)),
    },
    {
        'name': 'br_csma_lock',
        'title': 'BR/CSMA',
        'fch': ('BR', (0x606800B2, 7, -1)),
        'slot': ('CSMA', (0x606800B2, 6, -1)),
    },
]
clear_config = [
    {
        'name': 'clear_user0',
        'title': 'User0',
        'rx': (0x60680003, 3, -1),
        'tx': (0x60680003, 7, -1),
    },
    {
        'name': 'clear_user1',
        'title': 'User1',
        'rx': (0x60680003, 2, -1),
        'tx': (0x60680003, 6, -1),
    },
    {
        'name': 'clear_user2',
        'title': 'User2',
        'rx': (0x60680003, 1, -1),
        'tx': (0x60680003, 5, -1),
    },
    {
        'name': 'clear_user3',
        'title': 'User3',
        'rx': (0x60680003, 0, -1),
        'tx': (0x60680003, 4, -1),
    },
    {
        'name': 'clear_cs',
        'title': 'CS',
        'rx': (0x60680002, 4, -1),
        'tx': (0x60680002, 5, -1),
    },
    {
        'name': 'clear_br',
        'title': 'BR',
        'rx': (0x60680002, 6, -1),
        'tx': (0x60680002, 7, -1),
    },
]
reset_config = [
    {
        'name': 'reset_baseband_trx',
        'title': u'复位整个基带',
        'address': (0x60680000, 0, -1),
    },
    {
        'name': 'reset_baseband_rx',
        'title': u'复位整个基带RX',
        'address': (0x60680000, 1, -1),
    },
    {
        'name': 'reset_baseband_tx',
        'title': u'复位整个基带TX',
        'address': (0x60680000, 2, -1),
    },
]
