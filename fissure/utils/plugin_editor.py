#!/usr/bin/python3
"""Plugin Editor Functionality
"""
import os
import csv
from typing import List
from fissure.utils import PLUGIN_DIR
from fissure.utils.plugin import TABLES_FUNCTIONS
import fissure.utils.library
import json
import shutil

TABLE_FIELDS = {
    'protocols': [("index", int, None), ("protocol_name", str), ("data_rates", float, None), ("median_packet_lengths", float, None)]
}


def plugin_exists(name: str, directory: os.PathLike = PLUGIN_DIR):
    """Check if Plugin Exists

    Check if plugin and its expected file structure exists.

    Parameters
    ----------
    name : str
        Plugin name
    directory : os.PathLike, optional
        Directory for plugins, by default PLUGIN_DIR

    Returns
    -------
    bool
        Plugin exists
    """
    basepath = os.path.join(directory, name)
    if os.path.isdir(basepath):
        if os.path.isdir(os.path.join(basepath, 'tables')):
            for entry in TABLES_FUNCTIONS:
                if not os.path.isfile(os.path.join(basepath, 'tables', entry[0])):
                    return False
        else:
            return False
        if not os.path.isdir(os.path.join(basepath, 'install_files')):
            return False
        return True
    else:
        return False


def create_plugin(name: str, directory: os.PathLike = PLUGIN_DIR):
    """Create Plugin Directory and File Structure

    Parameters
    ----------
    name : str
        Plugin name
    directory : os.PathLike, optional
        Directory for plugins, by default PLUGIN_DIR
    """
    print('\nDIRECTORY: ' + str(directory))
    print('NAME: ' + str(name))
    print('TABLES DIR: ' + os.path.join(directory, name, 'tables') + '\n')
    # Create plugin directory structure
    os.makedirs(os.path.join(directory, name), 0o777, True)
    os.makedirs(os.path.join(directory, name, 'tables'), 0o777, True)
    os.makedirs(os.path.join(directory, name, 'install_files'), 0o777, True)

    # Create empty tables
    for entry in TABLES_FUNCTIONS:
        if not os.path.isfile(os.path.join(directory, name, 'tables', entry[0])):
            # table file does not exist; create
            with open(os.path.join(directory, name, 'tables', entry[0]), 'w') as f:
                f.write('')


# def read_protocol_csv(file: os.PathLike):
#     entries = {}
#     with open(file, 'r') as f:
#         reader = csv.reader(f, dialect='unix', quotechar="'")
#         for row in reader:
#             # Add protocol to entries
#             entries[row[1]] = {
#                 "data_rates": None if len(row[2]) == 0 else float(row[2]),
#                 "median_packet_lengths": None if len(row[3]) == 0 else float(row[3])
#             }
#     return entries


# def read_modulation_types_csv(file: os.PathLike):
#     protocols = {}
#     with open(file, 'r') as f:
#         reader = csv.reader(f, dialect='unix', quotechar="'")
#         for row in reader:
#             print(row)
#             # add mod_type to protocol
#             if row[1] in protocols.keys():
#                 # protocol already exists
#                 protocols[row[1]].append(row[2])
#             else:
#                 protocols[row[1]] = [row[2]]
#     return protocols


# def read_packet_types(file: os.PathLike):
#     pkt_types = {}
#     with open(file, 'r') as f:
#         reader = csv.reader(f, dialect='unix', quotechar="'")
#         for row in reader:
#             # add pkt_type to protocol
#             if row[1] in pkt_types.keys():
#                 # protocol already exists
#                 pkt_types[row[1]].append(row[2:])
#             else:
#                 pkt_types[row[1]] = [row[2:]]
#     return pkt_types


# def write_protocol_csv(file: os.PathLike, protocol_name: str, data_rates: float=None, median_packet_lengths: float=None):
#     with open(file, 'a') as f:
#         writer = csv.writer(f, dialect='unix', quotechar="'")
#         writer.writerow([None, protocol_name, data_rates, median_packet_lengths])


class PluginEditor(object):
    def __init__(self, name: str, directory: os.PathLike = PLUGIN_DIR):
        # Create or ensure plugin file structure aligns to expectations
        create_plugin(name, directory)

        # Create class variables
        self.basepath = os.path.join(PLUGIN_DIR, name)
        self.name = name

        # Import plugin data
        self.__importData__()


    def __importData__(self):
        """
        Packages the table data from CSV files in the 'tables' folder into a dictionary.
        Returns the packaged data in JSON format.
        """
        tables_path = os.path.join(self.basepath, "tables")
        table_data = {}

        for file_name in os.listdir(tables_path):
            if file_name.endswith(".csv"):
                table_name = os.path.splitext(file_name)[0]
                
                # Initialize list to store rows for this table
                table_data[table_name] = []

                csv_file_path = os.path.join(tables_path, file_name)
                with open(csv_file_path, "r", newline="") as csv_file:
                    reader = csv.reader(csv_file)
                    for row in reader:
                        table_data[table_name].append(row)

        self.table_data = json.dumps(table_data)  # Convert the data to JSON format


        # Read protocols file
        # self.protocols = read_protocol_csv(os.path.join(self.basepath, 'tables', 'protocols.csv'))

        # # Initialize remainder of protocols structure
        # for protocol in self.protocols:
        #     self.protocols[protocol]['mod_types'] = []

        # # Read mod types file and merge into protocols
        # mod_types = read_modulation_types_csv(os.path.join(self.basepath, 'tables', 'modulation_types.csv'))
        # for protocol in mod_types.keys():
        #     if protocol in self.protocols:
        #         self.protocols[protocol]['mod_types'] = mod_types[protocol]
        #     else:
        #         raise RuntimeError('`modulation_types.csv` contains protocol ' + str(protocol) + ' but ' + str(protocol) + ' is not in `protocols.csv`')

        # # Read packet types file and merge into protocols
        # pkt_types = read_packet_types(os.path.join(self.basepath, 'tables', 'packet_types.csv'))
        # for protocol in pkt_types.keys():
        #     if protocol in self.protocols:
        #         self.protocols[protocol]['pkt_types'] = pkt_types[protocol]
        #     else:
        #         raise RuntimeError('`packet_types.csv` contains protocol ' + str(protocol) + ' but ' + str(protocol) + ' is not in `protocols.csv`')

        # print('PROTOCOLS: ' + str(self.protocols))


    def applyChanges(self, table_data_json: dict):
        """
        Overwrites the csv files with table data from the Plugin Editor tab.
        """
        # Convert the JSON back to a dictionary
        table_data = json.loads(table_data_json)
        
        # Find the 'tables' folder
        tables_path = None
        for root, dirs, _ in os.walk(self.basepath):
            if "tables" in dirs:
                tables_path = os.path.join(root, "tables")
                break

        if not tables_path:
            # print("No 'tables' folder found.")
            return

        # Iterate over the table data
        for table_name, data in table_data.items():
            # headers = data["headers"]
            rows = data["rows"]

            # Construct the CSV file path for the current table
            csv_file_path = os.path.join(tables_path, f"{table_name}.csv")
            
            # Write the data to the CSV file
            with open(csv_file_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                # writer.writerow(headers)  # Write the headers first
                writer.writerows(rows)  # Write the rows
            
            # Optionally, notify the user for each table
            print(f"Table '{table_name}' has been updated in CSV.")

        # QtWidgets.QMessageBox.information(None, "Success", "CSV files have been updated!")


    def deletePlugin(self, plugin_name: str, delete_from_library: bool, os_version: str):
        """
        Overwrites the csv files with table data from the Plugin Editor tab.
        """
        if not os.path.isdir(self.basepath):
            print(f"Plugin folder '{plugin_name}' does not exist.")
            # QMessageBox.critical(None, "Error", f"Plugin folder '{plugin_name}' does not exist.")
            return

        # Remove from library/database
        if delete_from_library:
            try:
                # Find the 'tables' folder
                tables_path = None
                for root, dirs, _ in os.walk(self.basepath):
                    if "tables" in dirs:
                        tables_path = os.path.join(root, "tables")
                        break

                if not tables_path:
                    print("No 'tables' folder found.")
                    return
                
                # Maintain a Connection to the Database
                conn = fissure.utils.library.openDatabaseConnection()
        
                # Iterate through all CSV files in the folder
                for file_name in os.listdir(tables_path):
                    if file_name.endswith(".csv"):
                        table_name = os.path.splitext(file_name)[0]
                        csv_file_path = os.path.join(tables_path, file_name)

                        print(f"Processing table: {table_name} from file: {csv_file_path}")

                        try:
                            with open(csv_file_path, "r", newline="") as csv_file:
                                reader = csv.reader(csv_file)
                                for row in reader:
                                    # Call the appropriate deletion function for the current table
                                    self.deleteTableRow(conn, table_name, row, os_version)
                        except Exception as e:
                            print(f"Error processing file '{csv_file_path}': {e}")
                            
                print(f"Deleted associated library files and database entries for plugin: {plugin_name}")
            except:
                print(f"An error occurred while deleting the plugin: {e} from the library/database. Plugin folder not deleted.")
                return
            finally:
                conn.close()

        # Delete the plugin folder
        try:
            shutil.rmtree(self.basepath)
            print(f"Deleted plugin folder: {self.basepath}")
        except Exception as e:
            print(f"An error occurred while deleting the plugin folder: {e}")


    def deleteTableRow(self, conn, table_name: str, row: list, os_version: str):
        """
        Handles a single row for a specific table by calling the appropriate deletion function.

        Parameters:
        ----------
        table_name : str
            Name of the table being processed.
        row : list
            Row data from the CSV file.
        """
        # Get Row ID if Exact Match
        row_id = fissure.utils.library.findMatchingRow(conn, table_name, row)  # Fix this
        delete_files = True
        print(row_id)
    
        # Remove from Database/Library
        if row_id:
            if table_name == "archive_collection":
                pass
                # fissure.utils.library.removeFromTable(conn, table_name, row_id, delete_files, os_version)
            elif table_name == "archive_favorites":
                pass
            elif table_name == "attack_categories":
                pass
            elif table_name == "attacks":
                pass
                # fissure.utils.library.removeFromTable(conn, table_name, row_id, delete_files, os_version)
            elif table_name == "conditioner_flow_graphs":
                pass
            elif table_name == "demodulation_flow_graphs":
                pass
            elif table_name == "detector_flow_graphs":
                pass
            elif table_name == "inspection_flow_graphs":
                pass
            elif table_name == "modulation_types":
                pass
            elif table_name == "packet_types":
                pass
            elif table_name == "protocols":
                pass
            elif table_name == "soi_data":
                pass
            elif table_name == "triggers":
                pass
            else:
                print(f"No deletion logic defined for table '{table_name}'. Skipping row: {row}")

    ##########################################################################
    # def get_protocols(self):
    #     return list(self.protocols.keys())


    # def add_protocol(self, protocol_name: str, data_rates: float=None, median_packet_lengths: float=None):
    #     if not protocol_name in self.protocols.keys():
    #         # Protocol not in table
    #         with open(os.path.join(self.basepath, 'tables', 'protocols.csv'), 'a', newline='') as f:
    #             writer = csv.writer(f, dialect='unix', quotechar="'", quoting=csv.QUOTE_NONE)
    #             writer.writerow([None, protocol_name, data_rates, median_packet_lengths])
            
    #         # Update class dictionary
    #         self.protocols[protocol_name] = {
    #             "data_rates": data_rates,
    #             "median_packet_lengths": median_packet_lengths,
    #             "mod_types": [],
    #             "pkt_types": []
    #         }
    

    # def edit_protocol(self, protocol_name: str, data_rates: float, median_packet_lengths: float):
    #     if protocol_name in self.protocols.keys():
    #         # Protocol is in the set; perform edit
    #         # Read lines
    #         with open(os.path.join(self.basepath, 'tables', 'protocols.csv'), 'r') as f:
    #             reader = csv.reader(f, dialect='unix', quotechar="'")
    #             lines = list(reader)

    #         # Find line to edit
    #         for (i, line) in enumerate(lines):
    #             if line[1] == protocol_name:
    #                 lines[i][2] = '' if data_rates is None else str(data_rates)
    #                 lines[i][3] = '' if median_packet_lengths is None else str(median_packet_lengths)
    #                 print(line)
    #                 break
                    
    #         # Write lines back to file
    #         with open(os.path.join(self.basepath, 'tables', 'protocols.csv'), 'w', newline='') as f:
    #                 writer = csv.writer(f, dialect='unix', quotechar="'", quoting=csv.QUOTE_NONE)
    #                 writer.writerows(lines)

    #         # Update class dictionary
    #         self.protocols[protocol_name]["data_rates"] = data_rates
    #         self.protocols[protocol_name]["median_packet_lengths"] = median_packet_lengths

    #     else:
    #         self.add_protocol(protocol_name, data_rates, median_packet_lengths)


    # def get_protocol_parameters(self, protocol_name: str):
    #     return self.protocols.get(protocol_name)


    # def add_mod_type(self, protocol_name: str, mod_type: str):
    #     if len(mod_type) > 0:
    #         self.add_protocol(protocol_name) # ensure protocol exists in plugin

    #         if not mod_type in self.protocols.get(protocol_name).get('mod_types'):
    #             self.protocols[protocol_name]['mod_types'].append(mod_type)

    #             # protocol not in table
    #             with open(os.path.join(self.basepath, 'tables', 'modulation_types.csv'), 'a', newline='') as f:
    #                 writer = csv.writer(f, dialect='unix', quotechar="'", quoting=csv.QUOTE_NONE)
    #                 writer.writerow([None, protocol_name, mod_type])


    # def remove_mod_types(self, protocol_name: str, mod_types: List[str]):
    #     for mod_type in mod_types:
    #         # read lines
    #         with open(os.path.join(self.basepath, 'tables', 'modulation_types.csv'), 'r') as f:
    #             reader = csv.reader(f, dialect='unix', quotechar="'")
    #             lines = list(reader)

    #         print(lines)

    #         # find and remove line
    #         #line_idx = None
    #         for (i, line) in enumerate(lines):
    #             if line[2] == mod_type:
    #                 #print(i)
    #                 #print(line)
    #                 #line_idx = i
    #                 lines = lines[:i] + lines[i+1:]
    #                 break

    #         # write lines back to file
    #         with open(os.path.join(self.basepath, 'tables', 'modulation_types.csv'), 'w', newline='') as f:
    #                 writer = csv.writer(f, dialect='unix', quotechar="'", quoting=csv.QUOTE_NONE)
    #                 writer.writerows(lines)

    #         # remove from protocol dict
    #         self.protocols[protocol_name]['mod_types'].remove(mod_type)


    # def edit_pkt_types(self, protocol_name: str, pkt_types: List[List[str]]):
    #     # Rewrite packet types table with pkt_types
    #     self.protocols[protocol_name]['pkt_types'] = pkt_types
    #     with open(os.path.join(self.basepath, 'tables', 'packet_types.csv'), 'w', newline='') as f:
    #         writer = csv.writer(f, dialect='unix', quotechar="'", quoting=csv.QUOTE_MINIMAL)
    #         for pkt_type in pkt_types:
    #             line = [None, protocol_name] + pkt_type
    #             #print(['', protocol_name] + pkt_type)
    #             print('\nLINE: ' + str(line) + '\n')
    #             for entry in line:
    #                 print(entry)
    #             writer.writerow(line)


if __name__ == '__main__':
    pass
    # print(plugin_exists('test_plugin'))
    # print(plugin_exists('test'))
    # #create_plugin('test')
    # editor = PluginEditor('uitest')
    # '''editor.add_protocol('test2')
    # editor.add_protocol('test3', 42, 712.2)
    # editor.edit_protocol('test2', 75.1)
    # editor.edit_protocol('test3', None, 712.2)'''
    # #editor.edit_pkt_types('uitest2', [['', 'uitest2', 'uitest Plugin Packet!', '{"Port": null, "Filename": null}', '{"bb": {"Is CRC": true, "Length": 8, "CRC Range": "1-1", "Sort Order": 2, "Default Value": "00000000"}, "aaa": {"Is CRC": false, "Length": 8, "Sort Order": 1, "Default Value": "11111111"}}', " '1'"]])
    # editor.edit_pkt_types('uitest2', [['uitest Plugin Packet!', '{"Port": null, "Filename": null}', '{"bb": {"Is CRC": True, "Length": 8, "CRC Range": "1-1", "Sort Order": 2, "Default Value": "00000000"}, "aaa": {"Is CRC": False, "Length": 8, "Sort Order": 1, "Default Value": "11111111"}}', '1']])