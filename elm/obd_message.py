# List of known ECUs:
ECU_ADDR_FUNC_68 = "7DF"  # Functional address of protocol number: 6,8
ECU_ADDR_FUNC_45 = "C7 33 F1"  # Functional address of protocol number: 4,5
ECU_ADDR_FUNC_A = "EA FF F9"  # Functional address of protocol number: A
ECU_ADDR_H = "7E2"  # HVECU address (Hybrid contol module)
ECU_R_ADDR_H = "7EA"  # Responses sent by HVECU (Hybrid contol module) 7E2/7EA
ECU_ADDR_E = "7E0"  # Engine ECU address
ECU_R_ADDR_E = "7E8"  # Responses sent by Engine ECU - ECM (engine control module) 7E0/7E8
ECU_ADDR_T = "7E1"  # Transmission ECU address (transmission control module)
ECU_R_ADDR_T = "7E9"  # Responses sent by Transmission ECU - TCM (transmission control module) 7E1/7E9
ECU_ADDR_I = "7C0"  # ICE ECU address
ECU_R_ADDR_I = "7C8"  # Responses sent by ICE ECU address 7C0/7C8
ECU_ADDR_B = "7E3"  # Traction Battery ECU address
ECU_R_ADDR_B = "7EB"  # Responses sent by Traction Battery ECU - 7E3/7EB
ECU_ADDR_P = "7C4"  # Air Conditioning
ECU_R_ADDR_P = "7CC"  # Responses sent by Air Conditioning ECU - 7C4/7CC
ECU_ADDR_S = "7B0"  # Skid Control address ECU
ECU_R_ADDR_S = "7B8"  # Responses sent by 7B0 Skid Control ECU 7B0/7B8

ELM_R_OK = "OK\r"
ELM_MAX_RESP = '[0123456]?$'

ELM327_PROTO_STR = ['Automatic',
                    'SAE 1850 PWM (41.6k baud)',
                    'SAE 1850 VPW (10.4k baud)',
                    'ISO 9141-2 (5 baud init)',
                    'ISO 14230-4 KWP (5 baud init)',
                    'ISO 14230-4 KWP (fast init)',
                    'ISO 15765-4 CAN (11 bit ID, 500k baud)',
                    'ISO 15765-4 CAN (29 bit ID, 500k baud)',
                    'ISO 15765-4 CAN (11 bit ID, 250k baud)',
                    'ISO 15765-4 CAN (29 bit ID, 250k baud)',
                    'SAE 1939 CAN (29 bit ID, 250k baud)'
                    ]

# PID Dictionary
ObdMessage = {
    # AT Commands
    'AT' : {
        'AT_DESCR': {
            'Request': '^AT@1' + ELM_MAX_RESP,
            'Descr': 'Device description',
            'Response': "OBDII to RS232 Interpreter\r"
        },
        'AT_ID': {
            'Request': '^AT@2' + ELM_MAX_RESP,
            'Descr': 'Device identifier',
            'Response': "?\r"
        },
        'AT_CAF': {
            'Request': '^ATCAF[01]$',
            'Descr': 'AT CAF',
            'Exec': 'self.counters["cmd_caf"] = (cmd[4] == "1")',
            'Log': '"set CAF ON/OFF : %s", self.counters["cmd_caf"]',
            'Response': ELM_R_OK
        },
        'AT_DESCRIBE_PROTO': {
            'Request': '^ATDP' + ELM_MAX_RESP,
            'Descr': 'set DESCRIBE_PROTO',
            'Exec': 'time.sleep(0.1)',
            'ResponseHeader': \
            lambda self, cmd, pid, val: \
                ELM327_PROTO_STR[int(self.counters["cmd_proto"])] if 'cmd_proto' in self.counters \
                    else "ISO 15765-4 CAN (11 bit ID, 500k baud)",
            'Response': "\r"
        },
        'AT_DESCRIBE_PROTO_N': {
            'Request': '^ATDPN$',
            'Descr': 'set DESCRIBE_PROTO_N',
            'Exec': 'time.sleep(0.1)',
            'ResponseHeader': \
            lambda self, cmd, pid, val: \
                self.counters["cmd_proto"] if 'cmd_proto' in self.counters else "6",
            'Response': "\r"
        },
        'AT_ECHO': {
            'Request': '^ATE[01]$',
            'Descr': 'AT ECHO',
            'Exec': 'self.counters["cmd_echo"] = (cmd[3] == "1")',
            'Log': '"set ECHO ON/OFF : %s", self.counters["cmd_echo"]',
            'Response': ELM_R_OK
        },
        'AT_HEADERS': {
            'Request': '^ATH[01]$',
            'Descr': 'AT HEADERS',
            'Exec': 'self.counters["cmd_headers"] = (cmd[3] == "1")',
            'Log': '"set HEADERS ON/OFF : %s", self.counters["cmd_headers"]',
            'Response': ELM_R_OK
        },
        'AT_I': {
            'Request': '^ATI$',
            'Descr': 'ELM327 version string',
            'Response': "ELM327 v1.5\r"
        },
        'AT_IGN': {
            'Request': '^ATIGN' + ELM_MAX_RESP,
            'Descr': 'IgnMon input level',
            'Response': ("ON\r", "OFF\r")
        },
        'AT_LINEFEEDS': {
            'Request': '^ATL[01]$',
            'Descr': 'AT LINEFEEDS',
            'Exec': 'self.counters["cmd_linefeeds"] = (cmd[3] == "1")',
            'Log': '"set LINEFEEDS ON/OFF : %s", self.counters["cmd_linefeeds"]',
            'Response': ELM_R_OK
        },
        'AT_R_VOLT': {
            'Request': '^ATRV$',
            'Descr': 'AT read volt',
            'Log':
            '"Volt = {:.1f}".format(0.1 * abs(9 - (self.counters[pid] + 9) % 18) + 13)',
            'ResponseHeader': \
            lambda self, cmd, pid, val: \
                "{:.1f}".format(0.1 * abs(9 - (self.counters[pid] + 9) % 18) + 13),
            'Response': "V\r"
        },
        'AT_SPACES': {
            'Request': '^ATS[01]$',
            'Descr': 'Spaces off or on',
            'Exec': 'self.counters["cmd_spaces"] = (cmd[3] == "1")',
            'Response': ELM_R_OK
        },
        'AT_SET_HEADER': {
            'Request': '^ATSH',
            'Descr': 'AT SET HEADER',
            'Exec': 'self.counters["cmd_header"] = cmd[4:]',
            'Log': '"set HEADER %s", self.counters["cmd_header"]',
            'Response': ELM_R_OK
        },
        'AT_PROTO': {
            'Request': '^ATSP[0-9A-C]$',
            'Descr': 'AT PROTO',
            'Exec': 'self.counters["cmd_proto"] = cmd[4]',
            'Log': '"set PROTO %s", self.counters["cmd_proto"]',
            'Response': ELM_R_OK
        },
        'AT_TRY_PROTO': {
            'Request': '^ATTP[0-9A-C]+$',
            'Descr': 'AT TRY PROTO',
            'Exec': 'self.counters["cmd_proto"] = cmd[4:]',
            'Log': '"Try protocol %s", self.counters["cmd_proto"]',
            'Response': ELM_R_OK
        },
        'AT_WARM_START': {
            'Request': '^ATWS$',
            'Descr': 'AT WARM START',
            'Log': '"Sleep 0.1 seconds"',
            'Exec': 'self.reset(0.1)',
            'Response': "\r\rELM327 v1.5\r"
        },
        'AT_RESET': {
            'Request': '^ATZ$',
            'Descr': 'AT RESET',
            'Log': '"Sleep 0.5 seconds"',
            'Exec': 'self.reset(0.5)',
            'Response': "\r\rELM327 v1.5\r"
        },
        'AT_SET_TIMEOUT': {
            'Request': '^ATST[0-9A-F][0-9A-F]$',
            'Descr': 'AT SET TIMEOUT',
            'Exec': 'self.counters["cmd_timeout"] = int(cmd[4:], 16)',
            'Log': '"Set timeout %s", cmd[4:]',
            'Response': ELM_R_OK
        },
        'AT_M': {
            'Request': '^ATM[01]$',
            'Descr': 'Memory off or on',
            'Response': ELM_R_OK
        },
    },
    # OBD Commands
    'engineoff' : {
        'ELM_PIDS_A': {
            'Request': '^0100$',
            'Descr': 'PIDS_A',
            'ResponseHeader': \
            lambda self, cmd, pid, val: \
                'SEARCHING...\0 time.sleep(4.5) \0\rUNABLE TO CONNECT\r' \
                if self.counters[pid] == 1 else 'NO DATA\r',
            'Response': '',
            'Priority': 5
        },
        'ELM_MIDS_A': {
            'Request': '^0600$',
            'Descr': 'MIDS_A',
            'ResponseHeader': \
            lambda self, cmd, pid, val: \
                'SEARCHING...\0 time.sleep(4.5) \0\rUNABLE TO CONNECT\r' \
                if self.counters[pid] == 1 else 'NO DATA\r',
            'Response': '',
            'Priority': 5
        },
        'AT_DESCRIBE_PROTO_N': {
            'Request': '^ATDPN$',
            'Descr': 'set DESCRIBE_PROTO_N',
            'Exec': 'time.sleep(0.5)',
            'Response': "A0\r"
        },
        'NO_DATA': {
            'Request': '^[0-9][0-9][0-9A-F]+$',
            'Descr': 'NO_DATA',
            'Response': 'NO DATA\r',
            'Priority': 6
        },
    },
    'default' : {
        'STATUS': {
            'Request': '^0101' + ELM_MAX_RESP,
            'Descr': 'Status since DTCs cleared',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 06 41 01 00 07 55 00 \r'
        },
        # 'STATUS': {
        #     'Request': '^0101' + ELM_MAX_RESP,
        #     'Descr': 'Status since DTCs cleared',
        #     'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
        #     'Response': 'NO DATA\r'
        # },
        # 'STATUS': {
        #     'Request': '^0101' + ELM_MAX_RESP,
        #     'Descr': 'Status since DTCs cleared',
        #     'Response':
        #     ECU_R_ADDR_E + ' 06 41 01 00 07 55 FF \r' +
        #     ECU_R_ADDR_H + ' 06 41 01 00 07 55 FF \r'
        # },
        'FUEL_STATUS': {
            'Request': '^0103' + ELM_MAX_RESP,
            'Descr': 'Fuel System Status',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 03 00 00 \r'
        },
        'ENGINE_LOAD': {
            'Request': '^0104' + ELM_MAX_RESP,
            'Descr': 'Calculated Engine Load',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 04 00 \r'
        },
        'COOLANT_TEMP': {
            'Request': '^0105' + ELM_MAX_RESP,
            'Descr': 'Engine Coolant Temperature',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 05 41 05 7B \r'
        },
        'INTAKE_PRESSURE': {
            'Request': '^010B' + ELM_MAX_RESP,
            'Descr': 'Intake Manifold Pressure',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 0B 73 \r'
        },
        'RPM': {
            'Request': '^010C' + ELM_MAX_RESP,
            'Descr': 'Engine RPM',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': '',
            'ResponseFooter': \
            lambda self, cmd, pid, val: \
                ECU_R_ADDR_E + ' 04 41 0C ' \
                + self.Sequence(pid, base=2400, max=200, factor=80, n_bytes=2) \
                + ' \r' + ECU_R_ADDR_H + ' 04 41 0C ' \
                + self.Sequence(pid, base=2400, max=200, factor=80, n_bytes=2) \
                + ' \r'
        },
        'SPEED': {
            'Request': '^010D' + ELM_MAX_RESP,
            'Descr': 'Vehicle Speed',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': '',
            'ResponseFooter': \
            lambda self, cmd, pid, val: \
                ECU_R_ADDR_E + ' 03 41 0D ' \
                + self.Sequence(pid, base=0, max=30, factor=4, n_bytes=1) \
                + ' \r' + ECU_R_ADDR_H + ' 03 41 0D ' \
                + self.Sequence(pid, base=0, max=30, factor=4, n_bytes=1) \
                + ' \r'
        },
        'INTAKE_TEMP': {
            'Request': '^010F' + ELM_MAX_RESP,
            'Descr': 'Intake Air Temp',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 0F 44 \r'
        },
        'MAF': {
            'Request': '^0110' + ELM_MAX_RESP,
            'Descr': 'Air Flow Rate (MAF)',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 10 05 1F \r'
        },
        'THROTTLE_POS': {
            'Request': '^0111' + ELM_MAX_RESP,
            'Descr': 'Throttle Position',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 11 FF \r'
        },
        'OBD_COMPLIANCE': {
            'Request': '^011C' + ELM_MAX_RESP,
            'Descr': 'OBD Standards Compliance',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response':
            ECU_R_ADDR_H + ' 03 41 1C 06 \r' +
            ECU_R_ADDR_E + ' 03 41 1C 29 \r'
        },
        # 'OBD_COMPLIANCE': {
        #     'Request': '^011C' + ELM_MAX_RESP,
        #     'Descr': 'OBD Standards Compliance',
        #     'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
        #     'Response': 'NO DATA\r'
        # },
        'RUN_TIME': {
            'Request': '^011F' + ELM_MAX_RESP,
            'Descr': 'Engine Run Time',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 1F 00 8C \r'
        },
        'DISTANCE_W_MIL': {
            'Request': '^0121' + ELM_MAX_RESP,
            'Descr': 'Distance Traveled with MIL on',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 21 00 00 \r'
        },
        'FUEL_RAIL_PRESSURE_DIRECT': {
            'Request': '^0123' + ELM_MAX_RESP,
            'Descr': 'Fuel Rail Pressure (direct inject)',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 23 1A 0E \r'
        },
        'COMMANDED_EGR': {
            'Request': '^012C' + ELM_MAX_RESP,
            'Descr': 'Commanded EGR',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 2C 0D \r'
        },
        'EGR_ERROR': {
            'Request': '^012D' + ELM_MAX_RESP,
            'Descr': 'EGR Error',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 2D 80 \r'
        },
        'WARM-UP_SINCE_DTC_CLEAR': {
            'Request': '^0130' + ELM_MAX_RESP,
            'Descr': 'Number of warm-ups since DTC cleared',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 30 C8 \r'
        },
        'DISTANCE_SINCE_DTC_CLEAR': {
            'Request': '^0131' + ELM_MAX_RESP,
            'Descr': 'Distance traveled since codes cleared',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 31 C8 1F \r'
        },
        'BAROMETRIC_PRESSURE': {
            'Request': '^0133' + ELM_MAX_RESP,
            'Descr': 'Barometric Pressure',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 33 65 \r'
        },
        'CATALYST_TEMP_B1S1': {
            'Request': '^013C' + ELM_MAX_RESP,
            'Descr': 'Catalyst Temperature: Bank 1 - Sensor 1',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 3C 04 44 \r'
        },
        'CONTROL_MODULE_VOLTAGE': {
            'Request': '^0142' + ELM_MAX_RESP,
            'Descr': 'Control module voltage',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 42 39 D6 \r'
        },
        'LAMBDA': {
            'Request': '^0144' + ELM_MAX_RESP,
            'Descr': 'Fuel/Air Commanded Equivalence Ratio',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 44 43 43 \r'
        },
        'AMBIANT_AIR_TEMP': {
            'Request': '^0146' + ELM_MAX_RESP,
            'Descr': 'Ambient air temperature',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 46 43 \r'
        },
        'ACCELERATOR_POS_D': {
            'Request': '^0149' + ELM_MAX_RESP,
            'Descr': 'Accelerator pedal position D',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 49 00 \r'
        },
        'ACCELERATOR_POS_E': {
            'Request': '^014A' + ELM_MAX_RESP,
            'Descr': 'Accelerator pedal position E',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 4A 45 \r'
        },
        'THROTTLE_ACTUATOR': {
            'Request': '^014C' + ELM_MAX_RESP,
            'Descr': 'Commanded throttle actuator',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 4C 00 \r'
        },
        'RUN_TIME_MIL': {
            'Request': '^014D' + ELM_MAX_RESP,
            'Descr': 'Time run with MIL on',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 4D 00 00 \r'
        },
        'TIME_SINCE_DTC_CLEARED': {
            'Request': '^014E' + ELM_MAX_RESP,
            'Descr': 'Time since trouble codes cleared',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 4E 4C 69 \r'
        },
        'FUEL_TYPE': {
            'Request': '^0151' + ELM_MAX_RESP,
            'Descr': 'Fuel Type',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 03 41 51 01 \r'
        },
        'FUEL_INJECT_TIMING': {
            'Request': '^015D' + ELM_MAX_RESP,
            'Descr': 'Fuel injection timing',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 41 5D 66 00 \r'
        },
        # Supported PIDs for protocols
        'ELM_PIDS_A': {
            'Request': '^0100' + ELM_MAX_RESP,
            'Descr': 'PIDS_A',
            # 'ResponseHeader': \
            # lambda self, cmd, pid, val: \
                # 'SEARCHING...\0 time.sleep(3) \0\r' if self.counters[pid] == 1 else "",
            'Response':
            ECU_R_ADDR_H + ' 06 41 00 98 3A 80 13 \r' +
            ECU_R_ADDR_E + ' 06 41 00 BE 3F A8 13 \r'
        },
        'ELM_PIDS_B': {
            'Request': '^0120' + ELM_MAX_RESP,
            'Descr': 'PIDS_B',
            'Response':
            ECU_R_ADDR_H + ' 06 41 20 80 01 A0 00 \r' +
            ECU_R_ADDR_E + ' 06 41 20 90 15 B0 15 \r'
        },
        # 'ELM_PIDS_B': {
        #     'Request': '^0120' + ELM_MAX_RESP,
        #     'Descr': 'PIDS_B',
        #     'Response':
        #     ECU_R_ADDR_H + ' 06 41 20 80 01 80 01 \r' +
        #     ECU_R_ADDR_E + ' 06 41 20 A0 19 90 15 \r'
        # },
        'ELM_PIDS_C': {
            'Request': '^0140' + ELM_MAX_RESP,
            'Descr': 'PIDS_C',
            'Response':
            ECU_R_ADDR_E + ' 06 41 40 7A 1C 80 00 \r'
        },
        # 'ELM_PIDS_C': {
        #     'Request': '^0140' + ELM_MAX_RESP,
        #     'Descr': 'PIDS_C',
        #     'Response':
        #     ECU_R_ADDR_H + ' 06 41 40 C0 00 00 01 \r' +
        #     ECU_R_ADDR_E + ' 06 41 40 CC D0 00 09 \r'
        # },
        # 'ELM_PIDS_D': {
        #     'Request': '^0160' + ELM_MAX_RESP,
        #     'Descr': 'PIDS_D',
        #     'Response':
        #     ECU_R_ADDR_E + ' 06 41 60 02 09 02 40 \r'
        # },
        'CONFIRMED_DTC': {
            'Request': '^03' + ELM_MAX_RESP,
            'Descr': 'Confirmed DTC',
            'Response':
            ECU_R_ADDR_H + ' 02 43 00 \r' +
            ECU_R_ADDR_E + ' 02 43 00 \r'
        },
        'PENDING_DTC': {
            'Request': '^07' + ELM_MAX_RESP,
            'Descr': 'Pending DTC',
            'Response':
            ECU_R_ADDR_H + ' 02 47 00 \r' +
            ECU_R_ADDR_E + ' 02 47 00 \r'
        },
        # 'PENDING_DTC': {
        #     'Request': '^07' + ELM_MAX_RESP,
        #     'Descr': 'Pending DTC',
        #     'Response':
        #     ECU_R_ADDR_H + ' 02 47 02 00 10 00 20 \r' +
        #     ECU_R_ADDR_E + ' 02 47 00 \r'
        # },
        'PERMANENT_DTC': {
            'Request': '^0A' + ELM_MAX_RESP,
            'Descr': 'Permanent DTC',
            'Response':
            ECU_R_ADDR_H + ' 02 4A 00 \r' +
            ECU_R_ADDR_E + ' 02 4A 00 \r'
        },
        'ELM_MIDS_A': {
            'Request': '^0600' + ELM_MAX_RESP,
            'Descr': 'MIDS_A',
            'Response': ECU_R_ADDR_E + ' 06 46 00 C0 00 00 01 \r'
        },
        'ELM_MIDS_B': {
            'Request': '^0620' + ELM_MAX_RESP,
            'Descr': 'MIDS_B',
            'Response': ECU_R_ADDR_E + ' 06 46 20 80 00 80 01 \r'
        },
        'ELM_MIDS_C': {
            'Request': '^0640' + ELM_MAX_RESP,
            'Descr': 'MIDS_C',
            'Response': ECU_R_ADDR_E + ' 06 46 40 00 00 00 01 \r'
        },
        'ELM_MIDS_D': {
            'Request': '^0660' + ELM_MAX_RESP,
            'Descr': 'MIDS_D',
            'Response': ECU_R_ADDR_E + ' 06 46 60 00 00 00 01 \r'
        },
        'ELM_MIDS_E': {
            'Request': '^0680' + ELM_MAX_RESP,
            'Descr': 'MIDS_E',
            'Response': ECU_R_ADDR_E + ' 06 46 80 00 00 00 01 \r'
        },
        'ELM_MIDS_F': {
            'Request': '^06A0' + ELM_MAX_RESP,
            'Descr': 'MIDS_F',
            'Response': ECU_R_ADDR_E + ' 06 46 A0 F8 00 00 00 \r'
        },
        'ELM_PIDS_9A': {
            'Request': '^0900' + ELM_MAX_RESP,
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Descr': 'PIDS_9A',
            'Response':
            ECU_R_ADDR_H + ' 06 49 00 14 00 00 00 \r' +
            ECU_R_ADDR_E + ' 06 49 00 FF DF 00 00 \r'
        },
        'VIN_MESSAGE_COUNT': {
            'Request': '^0901' + ELM_MAX_RESP,
            'Descr': 'VIN Message Count',
            'Response': ECU_R_ADDR_E + ' 03 49 01 05 \r'
        },
        'VIN': { # Check this also: https://stackoverflow.com/a/26752855/10598800, https://www.autocheck.com/vehiclehistory/autocheck/en/vinbasics
            'Request': '^0902' + ELM_MAX_RESP,
            'Descr': 'Get Vehicle Identification Number',
            'Response': [
                        ECU_R_ADDR_E + ' 10 14 49 02 01 57 50 30 \r' +
                        ECU_R_ADDR_E + ' 21 5A 5A 5A 39 39 5A 54 \r' +
                        ECU_R_ADDR_E + ' 22 53 33 39 30 30 30 36 \r', # https://www.autodna.com/vin/WP0ZZZ99ZTS390000, https://it.vin-info.com/libro-denuncia/WP0ZZZ99ZTS390000
                        ECU_R_ADDR_E + ' 10 14 49 02 01 4D 41 54 \r' + # https://community.carloop.io/t/how-to-request-vin/153/11
                        ECU_R_ADDR_E + ' 21 34 30 33 30 39 36 42 \r' +
                        ECU_R_ADDR_E + ' 22 4E 4C 30 30 30 30 38 \r'
                        ]
        },
        # 'VIN': { # Check this also: https://stackoverflow.com/a/26752855/10598800, https://www.autocheck.com/vehiclehistory/autocheck/en/vinbasics
        #     'Request': '^0902' + ELM_MAX_RESP,
        #     'Descr': 'Get Vehicle Identification Number',
        #     'Response':
        #     ECU_R_ADDR_E + ' 03 7F 09 78 \r' +
        #     ECU_R_ADDR_E + ' 10 14 49 02 01 57 50 30 \r' +
        #     ECU_R_ADDR_E + ' 21 5A 5A 5A 39 39 5A 54 \r' +
        #     ECU_R_ADDR_E + ' 22 53 33 39 30 30 30 36 \r'
        # },
        'CALIBRATION_ID_MESSAGE_COUNT': {
            'Request': '^0903' + ELM_MAX_RESP,
            'Descr': 'Calibration ID message count for PID 04',
            'Response':
            ECU_R_ADDR_H + ' 03 49 03 04 \r' +
            ECU_R_ADDR_E + ' 03 49 03 08 \r'
        },
        'CALIBRATION_ID': {
            'Request': '^0904' + ELM_MAX_RESP,
            'Descr': 'Get Calibration ID',
            'Response':
            ECU_R_ADDR_H + ' 10 13 49 04 01 4A 4D 41 \r' +
            ECU_R_ADDR_H + ' 21 2A 34 33 31 32 39 39 \r' +
            ECU_R_ADDR_H + ' 22 31 31 30 30 30 30 \r' +
            ECU_R_ADDR_E + ' 10 23 49 04 02 4C 4B 32 \r' +
            ECU_R_ADDR_E + ' 21 31 2D 31 34 43 32 30 \r' +
            ECU_R_ADDR_E + ' 22 34 2D 44 42 00 00 4B \r' +
            ECU_R_ADDR_E + ' 23 56 36 41 2D 31 34 47 \r' +
            ECU_R_ADDR_E + ' 24 32 35 30 2D 43 43 00 \r' +
            ECU_R_ADDR_E + ' 25 00 \r'
        },
        # 'CALIBRATION_ID': {
        #     'Request': '^0904' + ELM_MAX_RESP,
        #     'Descr': 'Get Calibration ID',
        #     'Response':
        #     ECU_R_ADDR_H + ' 10 13 49 04 01 4A 4D 41 \r' +
        #     ECU_R_ADDR_H + ' 21 2A 34 33 31 32 39 39 \r' +
        #     ECU_R_ADDR_H + ' 22 31 31 30 30 30 30 \r' +
        #     ECU_R_ADDR_E + ' 10 13 49 04 02 4C 4B 32 \r' +
        #     ECU_R_ADDR_E + ' 21 31 2D 31 34 43 32 30 \r' +
        #     ECU_R_ADDR_E + ' 22 34 2D 44 42 00 00 \r'
        # },
        # 'CALIBRATION_ID': {
        #     'Request': '^0904' + ELM_MAX_RESP,
        #     'Descr': 'Get Calibration ID',
        #     'Response':
        #     ECU_R_ADDR_H + ' 10 13 49 04 01 00 00 00 \r' +
        #     ECU_R_ADDR_H + ' 21 00 00 00 00 00 00 00 \r' +
        #     ECU_R_ADDR_H + ' 22 00 00 00 00 00 00 AA \r' +
        #     ECU_R_ADDR_E + ' 10 13 49 04 01 20 20 20 \r' +
        #     ECU_R_ADDR_E + ' 21 20 20 20 20 20 20 20 \r' +
        #     ECU_R_ADDR_E + ' 22 20 20 20 20 20 20 AA \r'
        # },
        'CVN_MESSAGE_COUNT': {
            'Request': '^0905' + ELM_MAX_RESP,
            'Descr': 'Calibration Verification Numbers message count for PID 06',
            'Response':
            ECU_R_ADDR_H + ' 03 49 05 01 \r' +
            ECU_R_ADDR_E + ' 03 49 05 02 \r'
        },
        'CVN': {
            'Request': '^0906' + ELM_MAX_RESP,
            'Descr': 'Get Calibration Verification Numbers',
            'Response':
            ECU_R_ADDR_H + ' 07 49 06 01 98 12 34 76 \r' +
            ECU_R_ADDR_E + ' 10 0B 49 06 02 42 32 42 \r' +
            ECU_R_ADDR_E + ' 21 41 33 45 36 46 \r'
        },
        # 'CVN': {
        #     'Request': '^0906' + ELM_MAX_RESP,
        #     'Descr': 'Get Calibration Verification Numbers',
        #     'Response':
        #     ECU_R_ADDR_H + ' 07 49 06 01 98 12 34 76 \r' +
        #     ECU_R_ADDR_E + ' 07 49 06 01 33 45 36 46 \r'
        # },
        # 'CVN': {
        #     'Request': '^0906' + ELM_MAX_RESP,
        #     'Descr': 'Get Calibration Verification Numbers',
        #     'Response':
        #     ECU_R_ADDR_E + ' 03 7F 09 78 \r\r>\0 time.sleep(5) \0' +
        #     ECU_R_ADDR_H + ' 07 49 06 01 98 12 34 76 \r' +
        #     ECU_R_ADDR_E + ' 10 0B 49 06 02 42 32 42 \r' +
        #     ECU_R_ADDR_E + ' 21 41 33 45 36 46 \r'
        # },
        # 'CVN': {
        #     'Request': '^0906' + ELM_MAX_RESP,
        #     'Descr': 'Get Calibration Verification Numbers',
        #     'Response':
        #     ECU_R_ADDR_E + ' 03 7F 09 78 \r'
        # },
        # 'CVN': {
        #     'Request': '^0906' + ELM_MAX_RESP,
        #     'Descr': 'Get Calibration Verification Numbers',
        #     'Response':
        #     ECU_R_ADDR_E + ' 03 7F 09 78 \r\r>\0 time.sleep(1) \0\r' +
        #     ECU_R_ADDR_E + ' 02 7E 00 \r'
        # },
        'IPT_MESSAGE_COUNT': {
            'Request': '^0907' + ELM_MAX_RESP,
            'Descr': 'Number of messages to report In-use Performance Tracking for PID 08',
            'Response': ECU_R_ADDR_E + ' 03 49 07 08 \r'
        },
        'IPT_SPARK_IGNITION': {
            'Request': '^0908' + ELM_MAX_RESP,
            'Descr': 'Get In-use Performance Tracking for spark ignition vehicles',
            'Response':
            ECU_R_ADDR_E + ' 10 23 49 08 10 04 00 0D \r' +
            ECU_R_ADDR_E + ' 21 09 03 38 03 B1 02 C7 \r' +
            ECU_R_ADDR_E + ' 22 03 B1 02 E1 03 9C 02 \r' +
            ECU_R_ADDR_E + ' 23 D4 03 41 03 E5 03 F2 \r' +
            ECU_R_ADDR_E + ' 24 03 A9 03 CD 00 44 00 \r' +
            ECU_R_ADDR_E + ' 25 61 \r'
        },
        'ECUNAME_MESSAGE_COUNT': {
            'Request': '^0909' + ELM_MAX_RESP,
            'Descr': 'Number of messages to report the ECU’s/module’s acronym and text name for PID 0A',
            'Response': ECU_R_ADDR_E + ' 03 49 09 05 \r'
        },
        'ECU_NAME': {
            'Request': '^090A' + ELM_MAX_RESP,
            'Descr': 'Get ECU’s/module’s acronym and text name',
            'Response':
            ECU_R_ADDR_H + ' 10 17 49 0A 01 48 56 41 \r' +
            ECU_R_ADDR_H + ' 21 43 2D 48 56 41 43 43 \r' +
            ECU_R_ADDR_H + ' 22 74 72 6C 00 00 00 00 \r' +
            ECU_R_ADDR_H + ' 23 00 00 00 \r' +
            ECU_R_ADDR_E + ' 10 17 49 0A 01 45 43 4D \r' +
            ECU_R_ADDR_E + ' 21 00 2D 45 6E 67 69 6E \r' +
            ECU_R_ADDR_E + ' 22 65 20 43 6F 6E 74 72 \r' +
            ECU_R_ADDR_E + ' 23 6F 6C 00 \r'
        },
        'IPT_COMPRESSION_IGNITION': {
            'Request': '^090B' + ELM_MAX_RESP,
            'Descr': 'Get In-use Performance Tracking for compression ignition vehicles',
            'Response':
            ECU_R_ADDR_E + ' 10 23 49 08 10 04 00 0D \r' +
            ECU_R_ADDR_E + ' 21 09 03 38 03 B1 02 C7 \r' +
            ECU_R_ADDR_E + ' 22 03 B1 02 E1 03 9C 02 \r' +
            ECU_R_ADDR_E + ' 23 D4 03 41 03 E5 03 F2 \r' +
            ECU_R_ADDR_E + ' 24 03 A9 03 CD 00 44 00 \r' +
            ECU_R_ADDR_E + ' 25 61 \r'
        },
        'ESN_MESSAGE_COUNT': {
            'Request': '^090C' + ELM_MAX_RESP,
            'Descr': 'Number of messages to report Engine Serial Number (ESN)',
            'Response': ECU_R_ADDR_E + ' 03 49 0C 05 \r'
        },
        'ESN': {
            'Request': '^090D' + ELM_MAX_RESP,
            'Descr': 'Get Engine Serial Number',
            'Response':
            ECU_R_ADDR_E + ' 10 14 49 0D 01 00 00 00 \r' +
            ECU_R_ADDR_E + ' 21 00 42 52 41 4E 44 20 \r' +
            ECU_R_ADDR_E + ' 22 33 32 31 37 34 38 36 \r'
        },
        'EROTAN_MESSAGE_COUNT': {
            'Request': '^090E' + ELM_MAX_RESP,
            'Descr': 'Number of messages to report Exhaust Regulation Or Type Approval Number (EROTAN)',
            'Response': ECU_R_ADDR_E + ' 03 49 0E 05 \r'
        },
        'EROTAN': {
            'Request': '^090F' + ELM_MAX_RESP,
            'Descr': 'Get Exhaust Regulation Or Type Approval Number',
            'Response':
            ECU_R_ADDR_E + ' 10 14 49 0D 01 00 00 00 \r' +
            ECU_R_ADDR_E + ' 21 00 44 4F 43 2D 43 52 \r' +
            ECU_R_ADDR_E + ' 22 2D 39 33 34 35 36 37 \r'
        }
    },
    'ISO14230': {
        'ELM_PIDS_A': {
            'Request': '^0100' + ELM_MAX_RESP,
            'Descr': 'Support PID 01~20',
            'Response': '86 F1 11 41 00 BE 3E B8 11 8E \r'
        },
        'ELM_PIDS_B': {
            'Request': '^0120' + ELM_MAX_RESP,
            'Descr': 'Support PID 21~40',
            'Response': '86 F1 11 41 20 BE 3E B8 11 AE \r'
        },
        'ELM_PIDS_C': {
            'Request': '^0140' + ELM_MAX_RESP,
            'Descr': 'Support PID 41~60',
            'Response': '86 F1 11 41 40 00 00 00 00 09 \r'
        },
        'STATUS': {
            'Request': '^0101' + ELM_MAX_RESP,
            'Descr': 'Status since DTCs cleared',
            'Response': '86 F1 11 41 01 00 07 61 21 53 \r'
        },
        'OBD_COMPLIANCE': {
            'Request': '^011C' + ELM_MAX_RESP,
            'Descr': 'OBD Standards Compliance',
            'Response': '83 F1 11 41 1C 06 E8 \r'
        },
        'DISTANCE_W_MIL': {
            'Request': '^0121' + ELM_MAX_RESP,
            'Descr': 'Distance Traveled with MIL on',
            'Response': '84 F1 11 41 21 00 00 E8 \r'
        },
        'ODO': {
            'Request': '^01A6' + ELM_MAX_RESP,
            'Descr': 'Vehicle Odometer Reading',
            'Response': '83 F1 11 7F 01 12 17 \r'
        },
        'CONFIRMED_DTC': {
            'Request': '^03' + ELM_MAX_RESP,
            'Descr': 'Confirmed DTC',
            'Response': '87 F1 11 43 00 00 00 00 00 00 CC \r'
        },
        'PENDING_DTC': {
            'Request': '^07' + ELM_MAX_RESP,
            'Descr': 'Pending DTC',
            'Response': '87 F1 11 47 00 00 00 00 00 00 D0 \r'
        },
        'PERMANENT_DTC': {
            'Request': '^0A' + ELM_MAX_RESP,
            'Descr': 'Permanent DTC',
            'Response': '83 F1 11 7F 0A 11 1F \r'
        },
        'ELM_PIDS_9A': {
            'Request': '^0900' + ELM_MAX_RESP,
            'Descr': 'Support ITID 01~20',
            'Response': '87 F1 11 49 00 01 FF 00 00 00 D2 \r'
        },
        'VIN': {
            'Request': '^0902' + ELM_MAX_RESP,
            'Descr': 'Get Vehicle Identification Number',
            'Response':
            '87 F1 11 49 02 01 00 00 00 4C 21 \r' +
            '87 F1 11 49 02 02 4A 58 42 4D 07 \r' +
            '87 F1 11 49 02 03 46 48 43 33 DB \r' +
            '87 F1 11 49 02 04 4B 54 31 30 D8 \r' +
            '87 F1 11 49 02 05 34 33 37 31 A8 \r'
        },
        'CALIBRATION_ID': {
            'Request': '^0904' + ELM_MAX_RESP,
            'Descr': 'Get Calibration ID',
            'Response':
            '87 F1 11 49 04 01 32 38 35 37 AD \r' +
            '87 F1 11 49 04 02 37 33 38 39 B3 \r' +
            '87 F1 11 49 04 03 00 00 00 00 D9 \r' +
            '87 F1 11 49 04 04 00 00 00 00 DA \r'
        },
        'CVN': {
            'Request': '^0906' + ELM_MAX_RESP,
            'Descr': 'Get Calibration Verification Numbers',
            'Response': '87 F1 11 49 06 01 70 AA 70 AA 0D \r'
        },
        'ECU_NAME': {
            'Request': '^090A' + ELM_MAX_RESP,
            'Descr': 'Get ECU name',
            'Response': '83 F1 11 7F 09 12 1F \r'
        }
    },
    'ISO27145': {
        'ELM_PIDS_A': {
            'Request': '^22F400' + ELM_MAX_RESP,
            'Descr': 'Support PID 01~20',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 07 62 F4 00 BE 3F A8 13 \r'
        },
        'ELM_PIDS_B': {
            'Request': '^22F420' + ELM_MAX_RESP,
            'Descr': 'Support PID 21~40',
            'Response': ECU_R_ADDR_E + ' 07 62 F4 20 90 15 B0 15 \r'
        },
        'ELM_PIDS_C': {
            'Request': '^22F440' + ELM_MAX_RESP,
            'Descr': 'Support PID 41~60',
            'Response': ECU_R_ADDR_E + ' 07 62 F4 40 7A 1C 80 00 \r'
        },
        'F401': {
            'Request': '^22F401' + ELM_MAX_RESP,
            'Descr': 'Status since DTCs cleared',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 07 62 F4 01 00 0F AA 00 \r'
        },
        'F41C': {
            'Request': '^22F41C' + ELM_MAX_RESP,
            'Descr': 'OBD Standards Compliance',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 22 F4 1C 06 \r'
        },
        'F421': {
            'Request': '^22F421' + ELM_MAX_RESP,
            'Descr': 'Distance Traveled with MIL on',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 05 62 F4 21 00 00 \r'
        },
        'F800': {
            'Request': '^22F800' + ELM_MAX_RESP,
            'Descr': 'Support ITID 01~20',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 07 62 F8 00 54 69 80 00 \r'
        },
        'F802': {
            'Request': '^22F802' + ELM_MAX_RESP,
            'Descr': 'Get Vehicle Identification Number',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response':
            ECU_R_ADDR_E + ' 10 14 62 F8 02 4C 4A 58 \r' +
            ECU_R_ADDR_E + ' 21 43 4C 44 44 42 35 4B \r' +
            ECU_R_ADDR_E + ' 22 54 56 31 36 33 34 37 \r'
        },
        'F804': {
            'Request': '^22F804' + ELM_MAX_RESP,
            'Descr': 'Get Calibration ID',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response':
            ECU_R_ADDR_E + ' 10 23 62 F8 04 4C 4B 32 \r' +
            ECU_R_ADDR_E + ' 21 31 2D 31 34 43 32 30 \r' +
            ECU_R_ADDR_E + ' 22 34 2D 44 44 00 00 4B \r' +
            ECU_R_ADDR_E + ' 23 56 36 41 2D 31 34 47 \r' +
            ECU_R_ADDR_E + ' 24 32 35 30 2D 43 45 00 \r' +
            ECU_R_ADDR_E + ' 25 00 00 00 00 00 00 00 \r'
        },
        # 'F804': {
        #     'Request': '^22F804' + ELM_MAX_RESP,
        #     'Descr': 'Get Calibration ID',
        #     'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
        #     'Response':
        #     ECU_R_ADDR_E + ' 10 13 62 F8 04 4C 4B 32 \r' +
        #     ECU_R_ADDR_E + ' 21 31 2D 31 34 43 32 30 \r' +
        #     ECU_R_ADDR_E + ' 22 34 2D 44 44 00 00 \r'
        # },
        'F806': {
            'Request': '^22F806' + ELM_MAX_RESP,
            'Descr': 'Get CVN',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response':
            ECU_R_ADDR_E + ' 10 0B 62 F8 06 DC 41 EC \r' +
            ECU_R_ADDR_E + ' 21 C0 92 9E D9 D2 00 00 \r'
        },
        # 'F806': {
        #     'Request': '^22F806' + ELM_MAX_RESP,
        #     'Descr': 'Get CVN',
        #     'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
        #     'Response':
        #     ECU_R_ADDR_E + ' 07 62 F8 06 DC 41 EC C0 \r'
        # },
        'F80A': {
            'Request': '^22F80A' + ELM_MAX_RESP,
            'Descr': 'Get ECU’s/module’s acronym and text name',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response':
            ECU_R_ADDR_E + ' 10 17 62 F8 0A 45 43 4D \r' +
            ECU_R_ADDR_E + ' 21 00 2D 45 6E 67 69 6E \r' +
            ECU_R_ADDR_E + ' 22 65 43 6F 6E 74 72 6F \r' +
            ECU_R_ADDR_E + ' 23 6C 00 00 00 00 00 00 \r'
        },
        'F80B': {
            'Request': '^22F80B' + ELM_MAX_RESP,
            'Descr': 'Get In-use Performance Tracking for compression ignition vehicles',
            'Response':
            ECU_R_ADDR_E + ' 10 23 49 08 10 04 00 0D \r' +
            ECU_R_ADDR_E + ' 21 09 03 38 03 B1 02 C7 \r' +
            ECU_R_ADDR_E + ' 22 03 B1 02 E1 03 9C 02 \r' +
            ECU_R_ADDR_E + ' 23 D4 03 41 03 E5 03 F2 \r' +
            ECU_R_ADDR_E + ' 24 03 A9 03 CD 00 44 00 \r' +
            ECU_R_ADDR_E + ' 25 61 \r'
        },
        'F80D': {
            'Request': '^22F80D' + ELM_MAX_RESP,
            'Descr': 'Get Engine Serial Number',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response':
            ECU_R_ADDR_E + ' 10 14 62 F8 0D 3F 3F 3F \r' +
            ECU_R_ADDR_E + ' 21 3F 3F 3F 3F 3F 3F 3F \r' +
            ECU_R_ADDR_E + ' 22 3F 3F 3F 3F 3F 3F 3F \r'
        },
        'F810': {
            'Request': '^22F810' + ELM_MAX_RESP,
            'Descr': 'Get Protocol Identification',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response': ECU_R_ADDR_E + ' 04 62 F8 10 01 \r'
        },
        'F811': {
            'Request': '^22F811' + ELM_MAX_RESP,
            'Descr': 'Get WWH-OBD GTR Number',
            'Header': [ECU_ADDR_FUNC_68, ECU_ADDR_E],
            'Response':
            ECU_R_ADDR_E + ' 10 0E 62 F8 11 47 54 52 \r' +
            ECU_R_ADDR_E + ' 21 5F 30 30 35 2E 30 30 \r' +
            ECU_R_ADDR_E + ' 22 30 \r'
        },
        'CONFIRMED_DTC': {
            'Request': '^194233081E' + ELM_MAX_RESP,
            'Descr': 'Confirmed DTC',
            'Response': ECU_R_ADDR_E + ' 06 59 42 33 08 1E 04 \r'
        },
        # 'CONFIRMED_DTC': {
        #     'Request': '^194233081E' + ELM_MAX_RESP,
        #     'Descr': 'Confirmed DTC',
        #     'Response':
        #     ECU_R_ADDR_E + ' 10 0B 59 42 33 08 1E 04 \r' +
        #     ECU_R_ADDR_E + ' 21 08 25 22 1F 0C 20 02 \r' +
        #     ECU_R_ADDR_E + ' 22 35 12 2E \r'
        # },
        'PENDING_DTC': {
            'Request': '^194233041E' + ELM_MAX_RESP,
            'Descr': 'Pending DTC',
            'Response':
            ECU_R_ADDR_E + ' 06 59 42 33 04 1E 04 \r'
        },
        # 'PENDING_DTC': {
        #     'Request': '^194233041E' + ELM_MAX_RESP,
        #     'Descr': 'Pending DTC',
        #     'Response':
        #     ECU_R_ADDR_E + ' 10 0B 59 42 33 04 1E 04 \r' +
        #     ECU_R_ADDR_E + ' 21 08 25 22 1F 0C 20 02 \r' +
        #     ECU_R_ADDR_E + ' 22 35 12 2E \r'
        # },
        # 'PERMANENT_DTC': {
        #     'Request': '^195533' + ELM_MAX_RESP,
        #     'Descr': 'Permanent DTC',
        #     'Response':
        #     ECU_R_ADDR_E + ' 05 59 55 33 5C 04 \r'
        # },
    },
    'J1939': {
        'ELM_PIDS_A': {
            'Request': '^00FECE' + ELM_MAX_RESP,
            'Descr': 'DM5',
            'Response': '6 0FECE 00 00 01 29 06 00 08 00 08 \r'
        },
        'VIN': {
            'Request': '^00FEEC' + ELM_MAX_RESP,
            'Descr': 'Get Vehicle Identification Number',
            'Response':
            '012 \r' +
            '6 0EBFF 00 01 4C 45 46 59 45 44 4B \r' +
            '6 0EBFF 00 02 35 32 4B 48 4E 38 32 \r' +
            '6 0EBFF 00 03 31 33 30 2A FF FF FF \r'
        },
        # 'VIN': {
        #     'Request': '^00FEEC' + ELM_MAX_RESP,
        #     'Descr': 'Get Vehicle Identification Number',
        #     'Response':
        #     '6 0E8FF 00 01 FF FF FF FF EC FE 00 \r'
        # },
        'DM19': {
            'Request': '^00D300' + ELM_MAX_RESP,
            'Descr': 'Get Calibration Information',
            'Response':
            '028 \r\0 time.sleep(0.6) \0' +
            '7 0EBFF 00 01 FF 12 75 15 4B 43 31 \r' +
            '7 0EBFF 00 02 30 30 31 36 2E 30 30 \r' +
            '7 0EBFF 00 03 00 00 00 00 00 00 8C \r' +
            '7 0EBFF 00 04 4B F9 C9 4E 4F 78 2D \r' +
            '7 0EBFF 00 05 53 41 45 31 34 61 20 \r' +
            '7 0EBFF 00 06 41 54 4F 31 00 FF FF \r'
        },
    }
}
