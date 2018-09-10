# encoding: utf-8
freq_point_config = [
    {
        'name': 'freq_point_user0',
        'title': 'User0',
        'tx': 0x606800E8,
        'rx': 0x606800D8,
    },
    {
        'name': 'freq_point_user1',
        'title': 'User1',
        'tx': 0x606800EC,
        'rx': 0x606800DC,
    },
    {
        'name': 'freq_point_user2',
        'title': 'User2',
        'tx': 0x606800F0,
        'rx': 0x606800E0,
    },
    {
        'name': 'freq_point_user3',
        'title': 'User3',
        'tx': 0x606800F4,
        'rx': 0x606800E4,
    },
    {
        'name': 'freq_point_br',
        'title': 'BR',
        'tx': 0x606800D0,
        'rx': None,
    },
    {
        'name': 'freq_point_cs',
        'title': 'CS',
        'tx': 0x606800F8,
        'rx': None,
    },
]

RF_channel_config = [
    {
        'name': 'rf_channel_user0',
        'title': 'User0',
        'tx': (0x60680150, 6),
        'rx': (0x60680150, 7),
    },
    {
        'name': 'rf_channel_user1',
        'title': 'User1',
        'tx': (0x60680158, 6),
        'rx': (0x60680158, 7),
    },
    {
        'name': 'rf_channel_user2',
        'title': 'User2',
        'tx': (0x60680160, 6),
        'rx': (0x60680160, 7),
    },
    {
        'name': 'rf_channel_user3',
        'title': 'User3',
        'tx': (0x60680168, 6),
        'rx': (0x60680168, 7),
    },
    {
        'name': 'rf_channel_br',
        'title': 'BR',
        'tx': (0x60680188, 6),
        'rx': (0x60680188, 7),
    },
    {
        'name': 'rf_channel_cs',
        'title': 'CS',
        'tx': (0x60680178, 6),
        'rx': (0x60680178, 7),
    },
    {
        'name': 'rf_channel_fs',
        'title': 'FS',
        'tx': None,
        'rx': (0x60680180, 7),
    },
]

PA_config = [
    {
        'name': 'pa_setting_user0',
        'title': 'User0',
        'a20': (0x60680157, 0),
        'a21': (0x60680157, 1),
        'a50': (0x60680157, 2),
        'a51': (0x60680157, 3),
    },
    {
        'name': 'pa_setting_user1',
        'title': 'User1',
        'a20': (0x6068015F, 0),
        'a21': (0x6068015F, 1),
        'a50': (0x6068015F, 2),
        'a51': (0x6068015F, 3),
    },
    {
        'name': 'pa_setting_user2',
        'title': 'User2',
        'a20': (0x60680167, 0),
        'a21': (0x60680167, 1),
        'a50': (0x60680167, 2),
        'a51': (0x60680167, 3),
    },
    {
        'name': 'pa_setting_user3',
        'title': 'User3',
        'a20': (0x6068016F, 0),
        'a21': (0x6068016F, 1),
        'a50': (0x6068016F, 2),
        'a51': (0x6068016F, 3),
    },
    {
        'name': 'pa_setting_br',
        'title': 'BR',
        'a20': (0x6068018F, 0),
        'a21': (0x6068018F, 1),
        'a50': (0x6068018F, 2),
        'a51': (0x6068018F, 3),
    },
    {
        'name': 'pa_setting_cs',
        'title': 'CS',
        'a20': (0x6068017F, 0),
        'a21': (0x6068017F, 1),
        'a50': (0x6068017F, 2),
        'a51': (0x6068017F, 3),
    },
]

baseband_power_config = [
    {
        'name': 'baseband_power_user_a0',
        'title': u"所有用户天线0功率:",
        'address': 0x60680020,
    },
    {
        'name': 'baseband_power_user_a1',
        'title': u"所有用户天线1功率:",
        'address': 0x60680021,
    },
    {
        'name': 'baseband_power_br_cs',
        'title': u"BR/CS天线0功率:",
        'address': 0x60680025,
    },
]
# user_interleave_config = [
#     {
#         'name': 'user_interleave_send',
#         'title': u'用户发送',
#         'total_address': {
#             'user0': (0x60680004, 0, 2),
#             'user1': (0x60680008, 0, 2),
#             'user2': (0x6068000C, 0, 2),
#             'user3': (0x60680010, 0, 2),
#         },
#         'mode_address': {
#             'user0': (0x60680015, 0, 2),
#             'user1': (0x60680038, 0, 2),
#             'user2': (0x60680039, 3, 5),
#             'user3': (0x60680039, 0, 2),
#         },
#     },
#     {
#         'name': 'user_interleave_recv',
#         'title': u'用户接收',
#         'total_address': {
#             'user0': (0x60680150, 0, 2),
#             'user1': (0x60680158, 0, 2),
#             'user2': (0x60680160, 0, 2),
#             'user3': (0x60680168, 0, 2),
#         },
#         'mode_address': {
#             'user0': (0x60680151, 3, 5),
#             'user1': (0x60680159, 3, 5),
#             'user2': (0x60680161, 3, 5),
#             'user3': (0x60680169, 3, 5),
#         },
#     },
# ]
user_interleave_config = [
    {
        'name': 'user0_interleave_send',
        'title': 'User0发送',
        'total': (0x60680004, 0, 2),
        'mode': (0x60680015, 0, 2),
    },
    {
        'name': 'user0_interleave_recv',
        'title': 'User0接收',
        'total': (0x60680150, 0, 2),
        'mode': (0x60680151, 3, 5),
    },
    {
        'name': 'user1_interleave_send',
        'title': 'User1发送',
        'total': (0x60680008, 0, 2),
        'mode': (0x60680038, 0, 2),
    },
    {
        'name': 'user1_interleave_recv',
        'title': 'User1接收',
        'total': (0x60680158, 0, 2),
        'mode': (0x60680159, 3, 5),
    },
    {
        'name': 'user2_interleave_send',
        'title': 'User2发送',
        'total': (0x6068000C, 0, 2),
        'mode': (0x60680039, 0, 2),
    },
    {
        'name': 'user2_interleave_recv',
        'title': 'User2接收',
        'total': (0x60680160, 0, 2),
        'mode': (0x60680161, 3, 5),
    },
    {
        'name': 'user3_interleave_send',
        'title': 'User3发送',
        'total': (0x60680010, 0, 2),
        'mode': (0x60680039, 0, 2),
    },

    {
        'name': 'user3_interleave_recv',
        'title': 'User3接收',
        'total': (0x60680168, 0, 2),
        'mode': (0x60680169, 3, 5),
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
        'name': 'br_send',
        'title': u'BR/CS发送',
        'modem': (0x60680017, 4, -1),
        'encode': (0x60680017, 3, -1),
        'repeat': (0x60680016, 4, 6),
    },
    {
        'name': 'br_recv',
        'title': u'BR接收',
        'modem': (0x60680188, 3, 5),
        'encode': (0x6068018A, 4, 7),
        'repeat': (0x60680189, 0, 2),
    },
    {
        'name': 'cs_recv',
        'title': u'CS接收',
        'modem': (0x60680178, 3, 5),
        'encode': (0x6068017A, 4, 7),
        'repeat': (0x60680179, 0, 2),
    },
]

br_cs_bandwidth_config = {
    'name': 'br_cs_bandwidth',
    'BR': {
        'title': u'BR',
        'recv_address': (0x6068018B, 0, 2),
        'send_address': (0x60680017, 0, 2),
    },
    'CS': {
        'title': u'CS',
        'recv_address': (0x6068017B, 0, 2),
        'send_address': (0x60680017, 0, 2),
    },

}

# user_bandwidth_config = {
#     'name': 'user_bandwidth',
#     'title': u'用户',
#     'recv_address': {
#         'user0': (0x60680153, 0, 2),
#         'user1': (0x6068015B, 0, 2),
#         'user2': (0x60680163, 0, 2),
#         'user3': (0x6068016B, 0, 2),
#     },
#     'send_address': {
#         'user0': (0x60680007, 4, 6),
#         'user1': (0x6068000B, 4, 6),
#         'user2': (0x6068000F, 4, 6),
#         'user3': (0x60680013, 4, 6),
#     },
# }
user_bandwidth_config = [
    {
        'name': 'user0_bandwidth',
        'title': u'User0',
        'recv_address': (0x60680153, 0, 2),
        'send_address': (0x60680007, 4, 6),
    },
    {
        'name': 'user1_bandwidth',
        'title': u'User1',
        'recv_address': (0x6068015B, 0, 2),
        'send_address': (0x6068000B, 4, 6),
    },
    {
        'name': 'user2_bandwidth',
        'title': u'User2',
        'recv_address': (0x60680163, 0, 2),
        'send_address': (0x6068000F, 4, 6),
    },
    {
        'name': 'user3_bandwidth',
        'title': u'User3',
        'recv_address': (0x6068016B, 0, 2),
        'send_address': (0x60680013, 4, 6),
    },
]
antenna_mode_config = {
    'name': 'antenna_mode',
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
        'name': 'clear_br',
        'title': ' BR',
        'rx': (0x60680002, 6, -1),
        'tx': (0x60680002, 7, -1),
    },
    {
        'name': 'clear_cs',
        'title': ' CS',
        'rx': (0x60680002, 4, -1),
        'tx': (0x60680002, 5, -1),
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

rssi_config = [
    {
        'title': 'User0',
        'name': 'rssi_user0',
        'address': (
            [0x6068040A, 0x6068040B],
            [0x6068040C, 0x6068040D],
            [0x6068040E, 0x6068040F],
            [0x60680410, 0x60680411],
        ),
    },
    {
        'title': 'User1',
        'name': 'rssi_user1',
        'address': (
            [0x60680418, 0x60680419],
            [0x6068041A, 0x6068041B],
            [0x6068041C, 0x6068041D],
            [0x6068041E, 0x6068041F],
        ),
    },
    {
        'title': 'User2',
        'name': 'rssi_user2',
        'address': (
            [0x60680426, 0x60680427],
            [0x60680428, 0x60680429],
            [0x6068042A, 0x6068042B],
            [0x6068042C, 0x6068042D],
        ),
    },
    {
        'title': 'User3',
        'name': 'rssi_user3',
        'address': (
            [0x60680434, 0x60680435],
            [0x60680436, 0x60680437],
            [0x60680438, 0x60680439],
            [0x6068043A, 0x6068043B],
        ),
    },
]
snr_config = [
    {
        'title': 'User0',
        'name': 'snr_user0',
        'usr': (0x60680470, 0x60680471),
    },
    {
        'title': 'User1',
        'name': 'snr_user1',
        'usr': (0x60680480, 0x60680481),
    },
    {
        'title': 'User2',
        'name': 'snr_user2',
        'usr': (0x60680490, 0x60680491),
    },
    {
        'title': 'User3',
        'name': 'snr_user3',
        'usr': (0x60680498, 0x60680499),
    },

]
bler_config = [
    {
        'title': 'User0',
        'name': 'bler_user0',
        'total': (0x606804CE, 0x606804CF),
        'error': (0x606804CC, 0x606804CD),
    },
    {
        'title': 'User1',
        'name': 'bler_user1 ',
        'total': (0x606804D2, 0x606804D3),
        'error': (0x606804D0, 0x606804D1),
    },
    {
        'title': 'User2',
        'name': 'bler_user2 ',
        'total': (0x606804D6, 0x606804D7),
        'error': (0x606804D4, 0x606804D5),
    },
    {
        'title': 'User3',
        'name': 'bler_user3 ',
        'total': (0x606804DA, 0x606804DB),
        'error': (0x606804D8, 0x606804D9),
    },

]
