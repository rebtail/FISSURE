#!/usr/bin/env python3
import copy
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
from fissure.utils import FISSURE_ROOT, get_fg_library_dir
from decimal import Decimal
from datetime import datetime, date
import json


def openDatabaseConnection():
    """
    Connects to the FISSURE database at the HIPRFISR computer/network.
    """
    # Load environment variables from .env file
    load_dotenv(os.path.join(FISSURE_ROOT,".env"))

    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname = os.getenv('POSTGRES_DB'),
        user = os.getenv('POSTGRES_USER'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST', 'localhost'),
        port = os.getenv('POSTGRES_PORT', '5432')
    )
    return conn


def cacheTableData(source="Dashboard"):
    """
    Loads a copy of frequently used tables for local access and to avoid network queries to the database.
    """
    if source == "Dashboard":
        tables_to_load = [
            "archive_collection", 
            "archive_favorites", 
            "attack_categories",
            "conditioner_flow_graphs",
            "detector_flow_graphs",
            "inspection_flow_graphs",
            "triggers",
            "protocols",
            "attacks",
            "demodulation_flow_graphs",
            "modulation_types",
            "packet_types",
            "soi_data"
        ]
    elif source == "Protocol Discovery":
        tables_to_load = [
            "protocols",
            "demodulation_flow_graphs",
            "modulation_types",
            "packet_types",
            "soi_data"
        ]
    else:
        tables_to_load = [
            "archive_collection", 
            "archive_favorites", 
            "attack_categories",
            "conditioner_flow_graphs",
            "detector_flow_graphs",
            "inspection_flow_graphs",
            "triggers",
            "protocols",
            "attacks",
            "demodulation_flow_graphs",
            "modulation_types",
            "packet_types",
            "soi_data"
        ]

    # Load environment variables from .env file
    load_dotenv(os.path.join(FISSURE_ROOT,".env"))

    try:
        # Connect to PostgreSQL database
        conn = openDatabaseConnection()

        # Read Data
        table_data = {}
        with conn.cursor() as cur:
            for table_name in tables_to_load:
                query = f"SELECT * FROM {table_name};"
                cur.execute(query)
                rows = cur.fetchall()
                table_data[table_name] = [convert_data_types(row) for row in rows]
    
    except psycopg2.Error as e:
        print(f"Database error: {e}")

    finally:
        # Close the connection if it was successfully opened
        if conn is not None:
            conn.close()

    return table_data


def convert_data_types(row):
    """
    FissureZMQNode uses json.dumps() which needs decimal types to be converted to floats and datetimes to strings.
    """
    return [
        float(item) if isinstance(item, Decimal) 
        else item.isoformat() if isinstance(item, (datetime, date))
        else item
        for item in row
    ]


# =============================================================
#                   GET Direct Functions
# =============================================================
# This section contains functions for retrieving values 
# directly from the database accessed from inside the HIPRFISR 
# component.
# =============================================================


def getProtocolsDirect(conn):
    """
    Returns a list of protocol rows directly from the protocols table.
    """
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT protocol_name FROM protocols")
        rows = cur.fetchall()
        cur.close()

        return rows

    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if cur is not None:
            cur.close()


def getProtocolNamesDirect(conn):
    """
    Returns a sorted list of protocol names directly from the protocols table.
    """
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT protocol_name FROM protocols")
        rows = cur.fetchall()
        cur.close()

        # Convert list of tuples into a simple list
        protocol_names = sorted([row[0] for row in rows])

        return protocol_names
    
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if cur is not None:
            cur.close()


def getModulationTypesDirect(conn, protocol):
    """
    Returns the modulation types for a protocol directly from the modulation_types table.
    """
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT modulation_type FROM modulation_types WHERE protocol = %s", (protocol,))
        get_modulation_types = cur.fetchall()
        cur.close()

        # Convert list of tuples into a simple list
        sorted_modulation_types = sorted(item[0] for item in get_modulation_types)

        return sorted_modulation_types
    
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if cur is not None:
            cur.close()


def getPacketTypesDirect(conn, protocol):
    """
    Returns a list of sorted packet types for a protocol from the packet_types table.
    """
    cur = None
    try:
        cur = conn.cursor()
        cur.execute("SELECT packet_name FROM packet_types WHERE protocol = %s", (protocol,))
        get_packet_types = cur.fetchall()
        cur.close()

        # Convert list of tuples into a simple list
        sort_order_packet_types = [(int(row[5]), str(row[2])) for row in get_packet_types]
        sorted_packet_names = [string for _, string in sorted(sort_order_packet_types)]

        return sorted_packet_names
    
    except Exception as e:
        print(f"Error: {e}")
        return []
    finally:
        if cur is not None:
            cur.close()

    


# =============================================================
#                   GET Indirect Functions
# =============================================================
# This section contains functions for retrieving values from 
# the smaller cached FISSURE library/database accessed from
# outside the HIPRFISR component.
# =============================================================

def getConditionerIsolationMethod(library, isolation_category, version):
    """
    Returns a list of filename values for a detector type, hardware type, and version from the detector_flow_graphs table.
    """
    return sorted([str(row[2]) for row in library["conditioner_flow_graphs"] if row[1] == isolation_category and row[7] == version])


def getDetectorFlowGraphsFilename(library, detector_type, hardware, version):
    """
    Returns a list of filename values for a detector type, hardware type, and version from the detector_flow_graphs table.
    """
    return [str(row[3]) for row in library["detector_flow_graphs"] if row[1] == detector_type and row[2] == hardware and row[5] == version]


def getInspectionFlowGraphs(library):
    """
    Returns the inspection_flow_graphs table contents.
    """
    return [row for row in library["inspection_flow_graphs"]]


def getInspectionFlowGraphFilename(library, hardware, version):
    """
    Returns a list of python_file values for a hardware type and version from the inspection_flow_graphs table.
    """
    return [str(row[2]) for row in library["inspection_flow_graphs"] if row[1] == hardware and row[3] == version]


def getProtocolsTable(library):
    """
    Returns the protocols table contents.
    """
    return [row for row in library["protocols"]]


def getProtocols(library):
    """
    Returns a list of protocols from the protocols table.
    """
    return [str(row[1]) for row in library["protocols"]]


def getProtocolDataRates(library, protocol):
    """
    Returns a list of data rates for a protocol from the protocols table.
    """
    data_rates = [row[2] for row in library["protocols"] if row[1] == protocol]

    return data_rates


def getProtocolMedianPacketLengths(library, protocol, statistic):
    """
    Returns a list of median packet lengths for a protocol from the protocols table.
    """
    median_packet_lengths = [row[3] for row in library["protocols"] if row[1] == protocol]

    return median_packet_lengths


def getPacketTypesTable(library):
    """
    Returns the packet_types table contents.
    """
    return [row for row in library["packet_types"]]


def getPacketTypes(library, protocol):
    """
    Returns a list of sorted packet types for a protocol from the packet_types table.
    """
    sort_order_packet_types = [(int(row[5]), str(row[2])) for row in library["packet_types"] if row[1] == protocol]
    sorted_packet_types = [string for _, string in sorted(sort_order_packet_types)]

    return sorted_packet_types


def getArchiveFavorites(library):
    """
    Returns a list of sorted Archive favorites from the archive_favorites table.
    """
    return sorted(library["archive_favorites"], key=lambda x: x[1])


def getArchiveCollection(library):
    """
    Returns a list of Archive collections with no parent IDs (parent folder).
    """
    return [row for row in library["archive_collection"]]


def getArchiveCollectionParent(library):
    """
    Returns a list of Archive collections with no parent IDs (parent folder).
    """
    return sorted([row for row in library["archive_collection"] if row[8] is None], key=lambda x: x[1])


def getArchiveCollectionSubdirectory(library, parent_id):
    """
    Returns a list of Archive collection subdirectories from a parent ID.
    """
    return sorted([row for row in library["archive_collection"] if row[8] == parent_id], key=lambda x: x[1])


def getArchiveCollectionFilepath(library, name, parent1, parent2):
    """
    Returns the filepath (zipped, .tar) of a collection filtered by (unique) name from the archive_collection table).
    """
    # Root Tar File
    if parent1 == None:
        get_filepath = next((row[3] for row in library["archive_collection"] if row[1] == name), None)
        if get_filepath == None:
            return None

    elif parent2 == None:
        if '.sigmf-data' in name:
            # Single Data File with a Single Parent (1MSps_Exampes/avent_scd560_1922_5MHz_1MSps_1.sigmf-data)
            parent1_filepath = next((row[3] for row in library["archive_collection"] if row[1] == parent1), None)
            if parent1_filepath == None:
                return None
            
            get_filepath = parent1_filepath.replace('.tar','') + '/' + name
        else:
            # Child Collection (Avent_SCD560, CW_Morse_Code, etc.)
            parent1_filepath = next((row[3] for row in library["archive_collection"] if row[1] == parent1), None)
            if parent1_filepath == None:
                return None

            get_filepath = parent1_filepath.replace('.tar','') + '/' + name + '.tar'

    else:
        # Single Data File with Two Parents (X3xx_1MSps_All/Avent_SCD560/avent_scd560_1922_5MHz_1MSps_1.sigmf-data)
        if parent1 == None or parent2 == None:
            return None 
        
        parent2_filepath = next((row[3] for row in library["archive_collection"] if row[1] == parent2), None)
        if parent2_filepath == None:
            return None
        
        get_filepath = parent2_filepath.replace('.tar','') + '/' + parent1 + '/' + name
    
    return get_filepath


def getAttackNames(library, protocol, version):
    """
    Returns the attack_name for a protocol and version in the attacks table.
    """
    exclude_list = [
        "Single-Stage",
        "Denial of Service",
        "Jamming",
        "Spoofing",
        "Sniffing/Snooping",
        "Probe Attacks",
        "Installation of Malware",
        "Misuse of Resources",
        "File",
        "Multi-Stage",
        "New Multi-Stage",
        "Fuzzing",
        "Variables",
    ]
    attack_names = [row[2] for row in library["attacks"] if row[1] == protocol and row[2] not in exclude_list and row[8] == version]

    return attack_names


def getAttackType(library, protocol, attack_name, modulation_type, hardware, version):
    """
    Returns the attack_type for an attack in the attacks table.
    """
    attack_name = attack_name.split(' - ')[-1].strip()  # Avoids "X10 - On" in attack tree when entered as "On" in attacks table
    attack_type = next((row[5] for row in library["attacks"] if row[1] == protocol and row[2] == attack_name and row[3] == modulation_type and row[4] == hardware and row[8] == version), None)

    return attack_type


def getAttackFilename(library, protocol, attack_name, modulation_type, hardware, version):
    """
    Returns the filename for an attack in the attacks table.
    """
    attack_name = attack_name.split(' - ')[-1].strip()  # Avoids "X10 - On" in attack tree when entered as "On" in attacks table
    attack_filename = next((row[6] for row in library["attacks"] if row[1] == protocol and row[2] == attack_name and row[3] == modulation_type and row[4] == hardware and row[8] == version), None)

    return attack_filename


def getAttacks(library, protocol, version):
    """
    Returns the rows of attack data for a protocol in the attacks table.
    """
    if protocol == None:
        if version == None:
            attack_rows = [row for row in library["attacks"]]
        else:
            attack_rows = [row for row in library["attacks"] if row[8] == version]
    else:
        if version == None:
            attack_rows = [row for row in library["attacks"] if row[1] == protocol]
        else:
            attack_rows = [row for row in library["attacks"] if row[1] == protocol and row[8] == version]

    return attack_rows


def getAttackCategories(library):
    """
    Returns the rows of attack categories from the attack_categories table.
    """
    attack_categories_rows = [row for row in library["attack_categories"]]

    return attack_categories_rows


def getAttackCategoryNames(library):
    """
    Returns the names of the attack categories from the attack_categories table.
    """
    attack_category_names = [row[1] for row in library["attack_categories"]]

    return attack_category_names


def getSingleStageAttacks(library, version):
    """
    Returns the contents of the attacks table (id, attack_name, and tree_indent).
    """
    return library["attacks"]


def getSingleStageAttackNames(library, version):
    """
    Returns the attack_name of each row in the attacks table.
    """
    return [row[1] + ' - ' + row[2] for row in library["attacks"]]


def getMultiStageAttackNames(library, version):
    """
    Returns the attack_name of each row in the attacks table if the category is "Multi-Stage".
    """
    return [row[2] for row in library["attacks"] if row[7] == "Multi-Stage"]


def getFuzzingAttackNames(library, version):
    """
    Returns the attack_name of each row in the attacks table if the category is "Fuzzing".
    """
    return [row[1] + ' - ' + row[2] for row in library["attacks"] if row[7] == "Fuzzing"]


def getFields(library, protocol, packet_name):
    """
    Returns the sorted field names (no data) for a protocol and packet type from the packet_types table.
    """
    if len(protocol) == 0 or len(packet_name) == 0:
        return []
    
    fields = next(packet_type[4] for packet_type in library["packet_types"]
                  if packet_type[1] == protocol and 
                  packet_type[2] == packet_name)

    sorted_fields_list = sorted(fields, key=lambda x: fields[x]["Sort Order"])

    return sorted_fields_list


def getFieldData(library, protocol, packet_name, field_name):
    """
    Returns the field dictionary for a protocol, packet_name, and field_name from the packet_types table.
    """
    fields = next(packet_type[4] for packet_type in library["packet_types"]
                  if packet_type[1] == protocol and 
                  packet_type[2] == packet_name)
    
    field_dictionary = fields[field_name]

    return field_dictionary


def getDemodulationFlowGraphs(library):
    """
    Returns the demdulation_flow_graph table contents.
    """
    return [row for row in library["demodulation_flow_graphs"]]


def getDemodulationFlowGraphFilenames(library, protocol=None, modulation=None, hardware=None, version=None):
    """
    Returns the demdulation flow graph filename for a protocol, modulation, hardware type, and version combination.
    """
    # Start with all flow graphs
    demod_flowgraphs = library["demodulation_flow_graphs"]
    # Filter based on provided arguments
    if protocol:
        demod_flowgraphs = [row for row in demod_flowgraphs if row[1] == protocol]
    if modulation:
        demod_flowgraphs = [row for row in demod_flowgraphs if row[2] == modulation]
    if hardware:
        demod_flowgraphs = [row for row in demod_flowgraphs if row[3] == hardware]
    if version:
        demod_flowgraphs = [row for row in demod_flowgraphs if row[6] == version]

    return [row[4] for row in demod_flowgraphs]


def getDemodulationFlowGraphsModulation(library, protocol=None, version=None):
    """
    Returns the modulation types for a protocol's demodulation flow graphs in the demodulation_flow_graphs table.
    """
    get_modulation_types = []
    if protocol:
        get_modulation_types = [row[2] for row in library["demodulation_flow_graphs"] if row[1] == protocol and row[6] == version]
    else:
        get_modulation_types = [row[2] for row in library["demodulation_flow_graphs"] if row[6] == version]

    return get_modulation_types


def getDemodulationFlowGraphsSnifferType(library, filename, version):
    """
    Returns the sniffer types for a protocol's demodulation flow graph filename in the demodulation_flow_graphs table.
    """
    get_sniffer_types = []
    if filename:
        get_sniffer_types = [row[5] for row in library["demodulation_flow_graphs"] if row[4] == filename and row[6] == version]
    else:
        get_sniffer_types = [row[5] for row in library["demodulation_flow_graphs"] if row[6] == version]

    return get_sniffer_types


def getDemodulationFlowGraphsHardware(library, protocol=None, modulation=None, version=None):
    """
    Returns the demodulation flow graph hardware types for a protocol, modulation type, and version in the demodulation_flow_graphs table.
    """
    # Start with all flow graphs
    hardware_list = library["demodulation_flow_graphs"]
    
    # Filter based on provided arguments
    if protocol:
        hardware_list = [row[3] for row in hardware_list if row[1] == protocol]
    if modulation:
        hardware_list = [row[3] for row in hardware_list if row[2] == modulation]
    if version:
        hardware_list = [row[3] for row in hardware_list if row[6] == version]

    return hardware_list


def getDissector(library, protocol, packet_name):
    """
    Returns the dissector filename and port of a dissector for a packet type with a matching protocol and packet_name.
    """
    dissectors = [row[3] for row in library["packet_types"] if row[1] == protocol and row[2] == packet_name]
    
    if dissectors:
        return dissectors[0]  # Return the first matching result
    else:
        return None  # Or handle the case when nothing is found


def getNextDissectorPort(library):
    """
    Returns an unassigned dissector UDP port.
    """
    all_dissector_ports = [
        int(row[3]["Port"]) for row in library["packet_types"] 
        if row[3].get("Port") not in [None, 'None']  # Filter out both None and 'None'
    ]

    if all_dissector_ports:  # Ensure the list is not empty
        max_value = max(all_dissector_ports)
        return max_value + 1
    else:
        # Handle the case when there are no valid ports
        return 1  # Return 1 or any default starting port number


def getFieldProperties(library, protocol, packet_name, field):
    """
    Returns a field value from the fields dictionary in the packet_types table.
    """
    field_properties = [row[4][field] for row in library["packet_types"] if row[1] == protocol and row[2] == packet_name and field in row[4]]
    
    return field_properties


def getDefaults(library, protocol, packet_name):
    """
    Returns default values for fields in the fields dictionary sorted by field sort order in the packet_types table.
    """
    sorted_fields = getFields(protocol, packet_name)
    
    default_field_data = []
    for field in default_field_data:
        default_field_data.append(row[4][field]["Default Value"] for row in library["packet_types"] if row[1] == protocol and row[2] == packet_name and field in row[4])

    return default_field_data


def getModulationTypes(library):
    """
    Returns the modulation_types table contents.
    """
    return [row for row in library["modulation_types"]]


def getModulations(library, protocol):
    """
    Returns the modulation types for a protocol from the modulation_types table.
    """
    modulations = [row[2] for row in library["modulation_types"] if row[1] == protocol]

    return modulations


def getSOI_Names(library, protocol):
    """
    Returns a list of all soi_name values for a protocol from the soi_data table.
    """
    all_soi_names = [row[2] for row in library["soi_data"] if row[1] == protocol]

    return all_soi_names


def getSOIs(library, protocol=None):
    """
    Returns a list of all the SOIs for a protocol from the soi_data table.
    """
    if protocol == None:
        protocol_sois = [row for row in library["soi_data"]]
    else:
        protocol_sois = [row for row in library["soi_data"] if row[1] == protocol]

    return protocol_sois


def getTriggersTable(library):
    """
    Returns the trigger table contents.
    """
    return [row for row in library["triggers"]]


def getTriggerCategories(library, version):
    """
    Returns a sorted unique list of trigger categories from the triggers table.
    """
    return sorted(list(set([row[1] for row in library["triggers"] if row[6] == version])))


def getTriggerNames(library, category, version):
    """
    Returns a sorted unique list of trigger names filtered by category from the triggers table.
    """
    return sorted(list(set([row[2] for row in library["triggers"] if row[1] == category and row[6] == version])))


def getTriggerFilename(library, category, trigger_name, version):
    """
    Returns the trigger filename filtered by category and trigger_name from the triggers table.
    """
    return next((row[4] for row in library["triggers"] if row[1] == category and row[2] == trigger_name and row[6] == version), None)


def getTriggerFileType(library, category, trigger_name, version):
    """
    Returns the trigger file_type filtered by category and trigger_name from the triggers table.
    """
    return next((row[5] for row in library["triggers"] if row[1] == category and row[2] == trigger_name and row[6] == version), None)


def getTriggerDefaultSettings(library, category, trigger_name, version):
    """
    Returns the trigger file_type filtered by category and trigger_name from the triggers table.
    """
    return next((row[3] for row in library["triggers"] if row[1] == category and row[2] == trigger_name and row[6] == version), None)


def getConditionerFlowGraphsTable(library):
    """
    Returns all rows in the conditioner_flow_graphs table.
    """
    return [row for row in library["conditioner_flow_graphs"]]


def getDetectorFlowGraphsTable(library):
    """
    Returns all rows in the detector_flow_graphs table.
    """
    return [row for row in library["detector_flow_graphs"]]


# =============================================================
#                        ADD Functions
# =============================================================
# This section contains functions for adding values to the 
# FISSURE library/database.
# =============================================================

def addArchiveCollection(name, file_list, filepath, files, format, size, notes, parent_id):
    """
    Adds a new archive_collection table to the FISSURE PostgreSQL library.
    """
    # Load environment variables from .env file
    load_dotenv(os.path.join(FISSURE_ROOT,".env"))

    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname = os.getenv('POSTGRES_DB'),
        user = os.getenv('POSTGRES_USER'),
        password = os.getenv('POSTGRES_PASSWORD'),
        host = os.getenv('POSTGRES_HOST', 'localhost'),
        port = os.getenv('POSTGRES_PORT', '5432')
    )
    cur = conn.cursor()

    # SQL Insert command
    insert_query = """
        INSERT INTO archive_collection (name, file_list, filepath, files, format, size, notes, parent_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

    # Data to be inserted
    get_data = (name, file_list, filepath, files, format, size, notes, parent_id)
    # data = [
    #     ('X3xx_10MSps_All', None, '/X3xx/10MSps.tar', 75, 'Complex Float 32', 1.8, 
    #     'A collection of signals from miscellaneous devices recorded by Assured Information Security.', 
    #     None),
    #     ('Avent_SCD560', 
    #     ['avent_scd560_1922_5MHz_10MSps_1.sigmf-data', 
    #     'avent_scd560_1922_5MHz_10MSps_2.sigmf-data', 
    #     'avent_scd560_1922_5MHz_10MSps_3.sigmf-data', 
    #     'avent_scd560_1922_5MHz_10MSps_4.sigmf-data', 
    #     'avent_scd560_1922_5MHz_10MSps_5.sigmf-data'], 
    #     None, 5, 'Complex Float 32', 0.1796, '', 1)
    # ]

    # Execute the query
    cur.execute(insert_query, get_data)

    # Commit the transaction
    conn.commit()

    # Close communication
    cur.close()
    conn.close()


def addArchiveFavorite(file_name, date, format, modulation, notes, protocol, sample_rate, samples, size, tuned_frequency):
    """
    Adds a new entry to the archive_favorites table in the FISSURE PostgreSQL library.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=os.getenv('POSTGRES_PORT', '5432')
    )
    cur = conn.cursor()

    # SQL Insert command for the archive_favorites table
    insert_query = """
        INSERT INTO archive_favorites (file_name, date, format, modulation, notes, protocol, sample_rate, samples, size, tuned_frequency)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Data to be inserted
    get_data = (file_name, date, format, modulation, notes, protocol, sample_rate, samples, size, tuned_frequency)

    # Execute the query
    cur.execute(insert_query, get_data)

    # Commit the transaction
    conn.commit()

    # Close communication
    cur.close()
    conn.close()


def addProtocol(conn, protocol, data_rates, median_packet_lengths):
    """
    Adds a new protocol to the protocols table.
    """
    cur = None
    try:
        cur = conn.cursor()

        # Check if the second column already has the value
        check_query = sql.SQL("SELECT 1 FROM protocols WHERE protocol_name = %s")
        cur.execute(check_query, (protocol,))
        result = cur.fetchone()

        # If no matching value in column2, insert the new row
        if result is None:
            insert_query = sql.SQL(
                "INSERT INTO {} (protocol_name, data_rates, median_packet_lengths) VALUES (%s, %s, %s)"
            ).format(sql.Identifier("protocols"))
            
            cur.execute(insert_query, (protocol, None, None))
            conn.commit()
            print("Row inserted successfully.")
        else:
            print("Row with protocol_name value '{}' already exists.".format(protocol))

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback in case of error
    finally:
        if cur is not None:
            cur.close()


def addModulationType(conn, protocol, modulation):
    """
    Adds a new modulation type to the modulation_types table.
    """
    cur = None
    try:
        cur = conn.cursor()

        # Check if the columns already have the values
        check_query = sql.SQL("SELECT 1 FROM modulation_types WHERE protocol = %s AND modulation_type = %s")
        cur.execute(check_query, (protocol, modulation))
        result = cur.fetchone()

        # If no matching value, insert the new row
        if result is None:
            insert_query = sql.SQL(
                "INSERT INTO {} (protocol, modulation_type) VALUES (%s, %s)"
            ).format(sql.Identifier("modulation_types"))
            
            cur.execute(insert_query, (protocol, modulation))
            conn.commit()
            print("Row inserted successfully.")
        else:
            print(f"Row with modulation_type '{modulation}' for protocol '{protocol}' already exists.")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback in case of error
    finally:
        if cur is not None:
            cur.close()


def addPacketType(conn, protocol, packet_name, dissector, fields, sort_order):
    """
    Adds a new packet type to the packet_types table.
    """
    cur = None
    try:
        cur = conn.cursor()

        # Check if the columns already has the values
        check_query = sql.SQL("SELECT 1 FROM packet_types WHERE protocol = %s AND packet_name = %s")
        cur.execute(check_query, (protocol, packet_name))
        result = cur.fetchone()

        # If no matching value, insert the new row
        if result is None:
            # Convert dictionaries to JSON strings
            dissector_json = json.dumps(dissector)
            fields_json = json.dumps(fields)

            insert_query = sql.SQL(
                "INSERT INTO packet_types (protocol, packet_name, dissector, fields, sort_order) VALUES (%s, %s, %s, %s, %s)"
            )
            
            cur.execute(insert_query, (protocol, packet_name, dissector_json, fields_json, sort_order))
            conn.commit()
            print("Row inserted successfully.")
        else:
            print(f"Row with packet name '{packet_name}' for protocol '{protocol}' already exists.")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback in case of error
    finally:
        if cur is not None:
            cur.close()


def addSOI(conn, protocol, soi_name, center_frequency, start_frequency, end_frequency, bandwidth, continuous, modulation, notes):
    """
    Adds a signal of interest (SOI) to the soi_data table.
    """
    cur = None
    try:
        cur = conn.cursor()

        # Check if the columns already has the values
        check_query = sql.SQL("SELECT 1 FROM soi_data WHERE protocol = %s AND soi_name = %s")
        cur.execute(check_query, (protocol, soi_name))
        result = cur.fetchone()

        # If no matching value, insert the new row
        if result is None:
            insert_query = sql.SQL(
                """
                INSERT INTO soi_data (
                    protocol,
                    soi_name,
                    center_frequency,
                    start_frequency,
                    end_frequency,
                    bandwidth,
                    continuous,
                    modulation,
                    notes
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            )
            
            cur.execute(insert_query, (protocol, soi_name, center_frequency, start_frequency, end_frequency, bandwidth, continuous, modulation, notes))
            conn.commit()
            print("Row inserted successfully.")
        else:
            print(f"Row with SOI name '{soi_name}' for protocol '{protocol}' already exists.")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback in case of error
    finally:
        if cur is not None:
            cur.close()


def addDemodulationFlowGraph(conn, protocol, modulation_type, hardware, filename, output_type):
    """
    Adds a demodulation flow graph to the demodulation_flow_graphs table.
    """
    cur = None
    try:
        cur = conn.cursor()

        # Check if the columns already has the values
        check_query = sql.SQL("SELECT 1 FROM demodulation_flow_graphs WHERE protocol = %s AND filename = %s")
        cur.execute(check_query, (protocol, filename))
        result = cur.fetchone()

        # If no matching value, insert the new row
        if result is None:
            insert_query = sql.SQL(
                """
                INSERT INTO demodulation_flow_graphs (
                    protocol,
                    modulation_type,
                    hardware,
                    filename,
                    output_type
                ) VALUES (%s, %s, %s, %s, %s)
                """
            )
            
            cur.execute(insert_query, (protocol, modulation_type, hardware, filename, output_type))
            conn.commit()
            print("Row inserted successfully.")
        else:
            print(f"Row with filename '{filename}' for protocol '{protocol}' already exists.")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback in case of error
    finally:
        if cur is not None:
            cur.close()


def addAttack(conn, protocol, attack_name, modulation_type, hardware, attack_type, filename, category_name):
    """
    Adds a new attack to the attacks table.
    """
    cur = None
    try:
        cur = conn.cursor()

        # Check if the columns already has the values
        check_query = sql.SQL("SELECT 1 FROM attacks WHERE protocol = %s AND filename = %s")
        cur.execute(check_query, (protocol, filename))
        result = cur.fetchone()

        # If no matching value, insert the new row
        if result is None:
            insert_query = sql.SQL(
                """
                INSERT INTO attacks (
                    protocol,
                    attack_name,
                    modulation_type,
                    hardware,
                    attack_type,
                    filename,
                    category_name
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
            )
            
            cur.execute(insert_query, (protocol, attack_name, modulation_type, hardware, attack_type, filename, category_name))
            conn.commit()
            print("Row inserted successfully.")
        else:
            print(f"Row with filename '{filename}' for protocol '{protocol}' already exists.")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback in case of error
    finally:
        if cur is not None:
            cur.close()


def addDissector(conn, protocol, packet_name, dissector_filename, dissector_port):
    """
    Replaces the dissector filename and port for a packet type in the packet_types table. 
    There should only be one dissector per packet type.
    """
    cur = None
    try:
        cur = conn.cursor()

        new_value = json.dumps({"Port": int(dissector_port), "Filename": str(dissector_filename)})

        # Construct the SQL query
        update_query = """
        UPDATE packet_types
        SET dissector = %s
        WHERE protocol = %s AND packet_name = %s;
        """

        # Execute the query with the appropriate parameters
        cur.execute(update_query, (
            new_value,
            protocol,
            packet_name
        ))
        conn.commit()

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback in case of error
    finally:
        if cur is not None:
            cur.close()


# def newProtocol(protocolname="", attacks={}, demodflowgraph="", modtype="", pkttypes=newPacket()):
#     """Adds an empty protocol to a library."""

#     new_protocol_dict = {protocolname: {"Null Placeholder": None}}

#     return new_protocol_dict

# =============================================================
#                        REMOVE Functions
# =============================================================
# This section contains functions for removing values from the
# FISSURE library/database.
# =============================================================

def removeFromTable(conn, table_name, row_id, delete_files, os_version):
    """
    Removes a row from a table in the database.
    """
    cur = None
    try:
        cur = conn.cursor()

        # Use parameterized query to prevent SQL injection
        query = f"DELETE FROM {table_name} WHERE id = %s;"
        cur.execute(query, (row_id,))
        conn.commit()
        print(f"Row with ID {row_id} deleted from {table_name}.")

        # Remove Files
        if delete_files == True:
            if table_name == "demodulation_flow_graphs":
                # Use parameterized query to prevent SQL injection
                query = f"SELECT filename FROM {table_name} WHERE id = %s;"
                cur.execute(query, (row_id,))
                result = cur.fetchone()
                
                # If the row exists, fetch the filename, delete the file
                if result:
                    get_filename = result[0]
                    get_filepath = os.path.join(get_fg_library_dir(os_version), "PD Flow Graphs", get_filename)
                    os.system('rm "' + get_filepath + '"' )

            elif table_name == "inspection_flow_graphs":
                # Use parameterized query to prevent SQL injection
                query = f"SELECT python_file FROM {table_name} WHERE id = %s;"
                cur.execute(query, (row_id,))
                result = cur.fetchone()
                
                # If the row exists, fetch the filename, delete the file
                if result:
                    get_filename = result[0]
                    get_filepath = os.path.join(get_fg_library_dir(os_version), "Inspection Flow Graphs", get_filename)
                    os.system('rm "' + get_filepath + '"' )
                    os.system('rm "' + get_filepath.replace(".py",".grc") + '"' )

            elif table_name == "soi_data":
                pass  # Delete IQ files

            elif table_name == "triggers":
                # Use parameterized query to prevent SQL injection
                query = f"SELECT filename FROM {table_name} WHERE id = %s;"
                cur.execute(query, (row_id,))
                result = cur.fetchone()
                
                # If the row exists, fetch the filename, delete the file
                if result:
                    get_filename = result[0]
                    get_filepath = os.path.join(get_fg_library_dir(os_version), "Triggers", get_filename)
                    os.system('rm "' + get_filepath + '"' )

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()  # Rollback in case of error
    finally:
        if cur is not None:
            cur.close()



# =============================================================
#                        OTHER Functions
# =============================================================
# This section contains other supporting functions for 
# interacting with the library. .
# =============================================================

def newField(fieldname="", defaultvalue="", length=0, sortorder=1, iscrc="False", crcrange=""):
    """
    Constructs a field dictionary for fields in stored in a packet type.
    """
    if not fieldname:
        fieldname = "New Field"
    if not length:
        length = len(defaultvalue)

    if iscrc == "True":
        iscrc = True
    else:
        iscrc = False

    if crcrange == "":
        new_field_subdict = {
            fieldname: {
                "Default Value": defaultvalue,
                "Length": int(length),
                "Sort Order": int(sortorder),
                "Is CRC": bool(iscrc),
            }
        }
    else:
        new_field_subdict = {
            fieldname: {
                "Default Value": defaultvalue,
                "Length": int(length),
                "Sort Order": int(sortorder),
                "Is CRC": bool(iscrc),
                "CRC Range": str(crcrange),
            }
        }
    return new_field_subdict



####################################################################################################
# These were copied over, check these two functions.
def SOI_AutoSelect(list1, SOI_priorities, SOI_filters):
    """
    Sort the SOI_list using specified criteria and choose the best SOI to examine.
    "priority" is a list specifying which list elements in the SOI_list will be sorted by.
    priority = (2, 0, 1) will produce a list that is sorted by element2, then element0, and then element1
    "must_contain" is a list containing elements that narrows the SOI list further by checking for matches after
    the SOI list is sorted by priority
    """

    # print('Unsorted list: {}' .format(list1))

    # Sort the list by element priority
    for x in reversed(range(0, len(SOI_priorities))):
        if SOI_filters[x] == "Highest":
            list1 = sorted(list1, key=lambda list1: float(list1[SOI_priorities[x]]), reverse=True)

        elif SOI_filters[x] == "Lowest":
            list1 = sorted(list1, key=lambda list1: float(list1[SOI_priorities[x]]), reverse=False)

        elif SOI_filters[x] == "Nearest to":
            # Take Absolute Value of Value Differences and then Sort
            new_list_matching = []
            abs_value_list = []

            # Absolute Value
            for soi in range(0, len(list1)):
                abs_value_list.append(abs(float(SOI_parameters[x]) - float(list1[soi][SOI_priorities[x]])))

            # Sort from Absolute Value
            sorted_index = sorted(range(len(abs_value_list)), key=lambda x: abs_value_list[x])
            for index in range(0, len(sorted_index)):
                new_list_matching.append(list1[sorted_index[index]])
            list1 = new_list_matching

        elif SOI_filters[x] == "Greater than":
            # Keep Things that Fit Criteria
            new_list_matching = []
            for soi in range(0, len(list1)):
                if float(list1[soi][SOI_priorities[x]]) > float(SOI_parameters[x]):
                    new_list_matching.append(list1[soi])
            list1 = new_list_matching

        elif SOI_filters[x] == "Less than":
            # Keep Things that Fit Criteria
            new_list_matching = []
            for soi in range(0, len(list1)):
                if float(list1[soi][SOI_priorities[x]]) < float(SOI_parameters[x]):
                    new_list_matching.append(list1[soi])
            list1 = new_list_matching

        elif SOI_filters[x] == "Containing":
            # Keep Things that Fit Criteria
            new_list_matching = []
            for soi in range(0, len(list1)):
                if list1[soi][0] in SOI_parameters[x]:
                    new_list_matching.append(list1[soi])
            list1 = new_list_matching

    # print('Sorted list: {}' .format(list1))

    # Check if the list is empty
    if len(list1) > 0:
        soi = list1[0]
    else:
        print("No SOI Matches the Criteria")
        soi = []

    print("Selected SOI: {}".format(soi))

    return soi


def SOI_LibraryCheck(soi):
    """Look up the SOI to recommend a best-fit flow graph from the library"""

    # There needs to be some kind of look up to limit the possibilities
    # What parameters will be used to search the library? Modulation, Spreading, Frequency, Bandwidth?
    #  How will the search library be managed?

    # (
    #   Modulation_Type, Modulation_Sub_Parameters, Same_Modulation_Type_Index
    # ) : (
    #   Flow_Graph_Name, [Default_Variables], [Default_Values], [Potential_Attacks]
    # )

    # Find Flow Graphs with Same Modulation Type
    same_modulation_list_names = [
        v[0] for k, v in SOI_library.items() if k[0] == soi[0]
    ]  # Look Through Each Key in the Search Dictionary
    if not same_modulation_list_names:
        same_modulation_list_names = [v[0] for v in SOI_library.values()]

    return same_modulation_list_names


###################################


if __name__ == "__main__":
    pass
