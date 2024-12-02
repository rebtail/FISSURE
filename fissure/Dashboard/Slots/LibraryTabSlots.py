from PyQt5 import QtCore, QtWidgets, QtGui
import os
import fissure.utils
import qasync
import yaml
import shutil


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryGalleryNextClicked(dashboard: QtCore.QObject):
    """
    Selects the next picture in the gallery listbox.
    """
    # Increment the Row
    get_index = dashboard.ui.listWidget_library_gallery.currentRow() + 1
    if get_index >= dashboard.ui.listWidget_library_gallery.count():
        dashboard.ui.listWidget_library_gallery.setCurrentRow(0)
    else:
        dashboard.ui.listWidget_library_gallery.setCurrentRow(get_index)


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryGalleryPreviousClicked(dashboard: QtCore.QObject):
    """
    Selects the previous picture in the gallery listbox.
    """
    # Decrement the Row
    get_index = dashboard.ui.listWidget_library_gallery.currentRow() - 1
    if get_index < 0:
        dashboard.ui.listWidget_library_gallery.setCurrentRow(dashboard.ui.listWidget_library_gallery.count()-1)
    else:
        dashboard.ui.listWidget_library_gallery.setCurrentRow(get_index)


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryGalleryOpenClicked(dashboard: QtCore.QObject):
    """
    Opens the selected gallery image in an image viewer.
    """
    # Get the File
    get_image_name = str(dashboard.ui.listWidget_library_gallery.currentItem().text())
    image_filepath = os.path.join(fissure.utils.GALLERY_DIR, get_image_name)

    # Opens the File with EOG
    osCommandString = "eog " + image_filepath
    os.system(osCommandString+ " &")


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryGalleryProtocolChanged(dashboard: QtCore.QObject):
    """ 
    Updates the gallery listbox with images files for the selected protocol.
    """
    # Update the Listbox
    dashboard.ui.listWidget_library_gallery.clear()
    get_protocol = str(dashboard.ui.comboBox_library_gallery_protocol.currentText())
    get_protocol = get_protocol.replace(" ","_")
    protocol_len = len(get_protocol)
    for fname in sorted(os.listdir(fissure.utils.GALLERY_DIR)):
        if get_protocol in fname[0:protocol_len]:
            dashboard.ui.listWidget_library_gallery.addItem(fname)


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryGalleryImageChanged(dashboard: QtCore.QObject):
    """ 
    Displays the selected image in the gallery.
    """
    try:
        # Display Image
        get_image_name = str(dashboard.ui.listWidget_library_gallery.currentItem().text())
        get_image = QtGui.QPixmap(os.path.join(fissure.utils.GALLERY_DIR, get_image_name))
        get_width = get_image.width()
        get_height = get_image.height()
        label_width = 860
        label_height = 630

        # Resize Image, Keep Aspect Ratio
        w_ratio = float(get_width)/float(label_width)
        h_ratio = float(get_height)/float(label_height)
        if w_ratio > h_ratio:
            get_image = get_image.scaled(int(get_width/w_ratio),int(get_height/w_ratio))
        else:
            get_image = get_image.scaled(int(get_width/h_ratio),int(get_height/h_ratio))

        dashboard.ui.label_library_gallery.setFixedSize(get_image.width(),get_image.height())
        dashboard.ui.label_library_gallery.setPixmap(get_image)

    except:
        pass


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibrarySearchBinaryClicked(dashboard: QtCore.QObject):
    """ 
    Converts the PD Search Field Values edit box to binary.
    """
    try:
        # Convert to Binary
        get_data = str(dashboard.ui.textEdit_library_search_field_value.toPlainText())
        get_data = get_data.replace(' ','')
        bin_str = bin(int(get_data, 16))[2:].zfill(int(len(get_data)*4))
        dashboard.ui.textEdit_library_search_field_value.setPlainText(bin_str)
    except:
        pass


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibrarySearchHexClicked(dashboard: QtCore.QObject):
    """ 
    Converts the PD Search Field Values edit box to hex.
    """
    try:
        # Convert to Hex
        get_data = str(dashboard.ui.textEdit_library_search_field_value.toPlainText())
        get_data = get_data.replace(' ','')
        hex_str = '%0*X' % ((len(get_data) + 3) // 4, int(get_data, 2))
        dashboard.ui.textEdit_library_search_field_value.setPlainText(hex_str)
    except:
        pass


@QtCore.pyqtSlot(QtCore.QObject)
def _slotPD_AddToLibraryProtocolChanged(dashboard: QtCore.QObject):
    """ 
    Selects a protocol for the new packet type to be assigned to in the library.
    """
    # Clear Demodulation Flow Graph Modulation Combo Box
    dashboard.ui.comboBox_library_pd_modulation_types.clear()

    # Enable/Disable New Protocol Name
    get_protocol = str(dashboard.ui.comboBox_library_pd_protocol.currentText())
    if get_protocol != "":
        if get_protocol == "-- New Protocol --":
            dashboard.ui.label1_library_add.setText("Add New Protocol to Library")
            dashboard.ui.stackedWidget2_library_pd.setCurrentIndex(0)
            dashboard.ui.label2_library_pd_data_type.setVisible(False)
            dashboard.ui.comboBox_library_pd_data_type.setVisible(False)
        else:
            dashboard.ui.label2_library_pd_data_type.setVisible(True)
            dashboard.ui.comboBox_library_pd_data_type.setVisible(True)
            _slotLibraryAddDataTypeChanged(dashboard)


@QtCore.pyqtSlot(QtCore.QObject)
def _slotAttackImportAttackTypeChanged(dashboard: QtCore.QObject):
    """ 
    This changes the items in the attack tree parent combobox to reflect single-stage or multi-stage categories.
    """
    # Add New Items
    dashboard.ui.comboBox_library_attacks_subcategory.clear()
    if dashboard.ui.comboBox_library_attacks_attack_type.currentText() == "Single-Stage":
        dashboard.ui.comboBox_library_attacks_subcategory.addItems(["Denial of Service", "Jamming", "Spoofing", "Sniffing/Snooping", "Probe Attacks", "Installation of Malware", "Misuse of Resources", "Other"])
        dashboard.ui.label2_library_attacks_new_name.setHidden(False)
        dashboard.ui.label2_library_attacks_new_name2.setHidden(False)
        dashboard.ui.textEdit_library_attacks_new_name.setHidden(False)
        dashboard.ui.label2_library_attacks_file_select.setText(".py File:")
        dashboard.ui.label2_library_attacks_modulation.setHidden(False)
        dashboard.ui.comboBox_library_attacks_modulation.setHidden(False)

    # elif dashboard.ui.comboBox_library_attacks_attack_type.currentText() == "Multi-Stage":
        # dashboard.ui.comboBox_library_attacks_subcategory.addItems(["Multi-Stage"])
        # dashboard.ui.label2_library_attacks_new_name.setHidden(True)
        # dashboard.ui.label2_library_attacks_new_name2.setHidden(True)
        # dashboard.ui.textEdit_library_attacks_new_name.setHidden(True)
        # dashboard.ui.label2_library_attacks_file_select.setText(".msa File:")
        # dashboard.ui.label2_library_attacks_modulation.setHidden(True)
        # dashboard.ui.comboBox_library_attacks_modulation.setHidden(True)

    # Reset State
    dashboard.ui.label_library_attacks_filepath.setText("")
    dashboard.ui.textEdit_library_attacks_name.setPlainText("")
    dashboard.ui.textEdit_library_attacks_new_name.setPlainText("")


@QtCore.pyqtSlot(QtCore.QObject)
def _slotAttackImportFileTypeChanged(dashboard: QtCore.QObject):
    """ 
    Toggles the "include .grc" check box.
    """
    # Enable Check Box
    if str(dashboard.ui.comboBox_library_attacks_file_type.currentText()) == "Flow Graph":
        dashboard.ui.checkBox_library_attacks_grc_file.setEnabled(True)
        dashboard.ui.checkBox_library_attacks_grc_file.setChecked(True)
    elif str(dashboard.ui.comboBox_library_attacks_file_type.currentText()) == "Flow Graph - GUI":
        dashboard.ui.checkBox_library_attacks_grc_file.setEnabled(True)
        dashboard.ui.checkBox_library_attacks_grc_file.setChecked(True)
    else:
        dashboard.ui.checkBox_library_attacks_grc_file.setEnabled(False)
        dashboard.ui.checkBox_library_attacks_grc_file.setChecked(False)


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryAddDataTypeChanged(dashboard: QtCore.QObject):
    """ 
    Changes the stacked widget for adding different types of protocol data to the library.
    """
    # Change Index
    get_type = str(dashboard.ui.comboBox_library_pd_data_type.currentText())
    if get_type == "Modulation Type":
        dashboard.ui.label1_library_add.setText("Add New Modulation Type to Library")
        dashboard.ui.stackedWidget2_library_pd.setCurrentIndex(1)
    elif get_type == "Packet Type":
        dashboard.ui.label1_library_add.setText("Add New Packet Type to Library")
        dashboard.ui.stackedWidget2_library_pd.setCurrentIndex(2)
    elif get_type == "Signal of Interest":
        dashboard.ui.label1_library_add.setText("Add New Signal of Interest to Library")
        dashboard.ui.stackedWidget2_library_pd.setCurrentIndex(3)
    elif get_type == "Demodulation Flow Graph":
        dashboard.ui.label1_library_add.setText("Add New Demodulation Flow Graph to Library")
        dashboard.ui.stackedWidget2_library_pd.setCurrentIndex(4)

        # Populate Demodulation Flow Graph Modulation Types
        get_protocol = str(dashboard.ui.comboBox_library_pd_protocol.currentText())
        if len(get_protocol) > 0:
            get_modulation_types = fissure.utils.library.getModulations(dashboard.backend.library, get_protocol)
            if len(get_modulation_types) > 0:
                dashboard.ui.comboBox_library_pd_modulation_types.addItems(get_modulation_types)

    elif get_type == "Attack":
        _slotAttackImportProtocolChanged(dashboard)
        dashboard.ui.label1_library_add.setText("Add New Attack to Library")
        dashboard.ui.stackedWidget2_library_pd.setCurrentIndex(5)


@QtCore.pyqtSlot(QtCore.QObject)
def _slotAttackImportProtocolChanged(dashboard: QtCore.QObject):
    """ 
    This changes the items in the modulation combobox to reflect the currently selected protocol. FIX - Is this a real slot?
    """
    # Update Comboboxes
    dashboard.ui.comboBox_library_attacks_modulation.clear()
    get_protocol = str(dashboard.ui.comboBox_library_pd_protocol.currentText())
    if get_protocol != "":
        try:
            modulation_types = fissure.utils.library.getModulations(dashboard.backend.library, get_protocol)
            dashboard.ui.comboBox_library_attacks_modulation.addItems(modulation_types)
        # No Modulation Types Available
        except KeyError:
            pass


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibrarySearchCurrentSOI_Clicked(dashboard: QtCore.QObject):
    """ 
    Populates the Search Library Fields with the current SOI.
    """
    # Set the Fields
    if len(dashboard.target_soi) > 0:
        dashboard.ui.textEdit_library_search_frequency.setPlainText(dashboard.target_soi[0])
        dashboard.ui.textEdit_library_search_modulation.setPlainText(dashboard.target_soi[1])
        dashboard.ui.textEdit_library_search_bandwidth.setPlainText(dashboard.target_soi[2])

        if dashboard.target_soi[3] == "True":
            dashboard.ui.comboBox_library_search_continuous.setCurrentIndex(0)
        else:
            dashboard.ui.comboBox_library_search_continuous.setCurrentIndex(1)

        dashboard.ui.textEdit_library_search_start_frequency.setPlainText(dashboard.target_soi[4])
        dashboard.ui.textEdit_library_search_end_frequency.setPlainText(dashboard.target_soi[5])


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryAddBrowseClicked(dashboard: QtCore.QObject):
    """ 
    Opens a file dialog to choose an existing python file for demodulating the protocol.
    """
    # Select a File
    dialog = QtWidgets.QFileDialog(dashboard)
    directory = os.path.join(fissure.utils.get_fg_library_dir(dashboard.backend.os_info), "PD Flow Graphs")
    dialog.setDirectory(directory)
    dialog.setNameFilters(['Flow Graphs (*.py)'])

    if dialog.exec_():
        for d in dialog.selectedFiles():
            folder = d
    try:
        dashboard.ui.textEdit_library_pd_demodulation_fg.setPlainText(str(folder))
    except:
        pass


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryAddCurrentSOI_Clicked(dashboard: QtCore.QObject):
    """ 
    Updates the edit boxes in the SOI Data section of the "Add to Library" tab with the current SOI information.
    """
    # Insert the Information
    if str(dashboard.ui.textEdit_pd_status_target.toPlainText()) != "":
        if len(dashboard.target_soi) > 0:
            dashboard.ui.textEdit_library_pd_soi_frequency.setPlainText(dashboard.target_soi[0])
            dashboard.ui.textEdit_library_pd_soi_modulation.setPlainText(dashboard.target_soi[1])
            dashboard.ui.textEdit_library_pd_soi_bandwidth.setPlainText(dashboard.target_soi[2])

            if dashboard.target_soi[3] == "True":
                dashboard.ui.comboBox_library_pd_soi_continuous.setCurrentIndex(0)
            else:
                dashboard.ui.comboBox_library_pd_soi_continuous.setCurrentIndex(1)

            dashboard.ui.textEdit_library_pd_soi_start_frequency.setPlainText(dashboard.target_soi[4])
            dashboard.ui.textEdit_library_pd_soi_end_frequency.setPlainText(dashboard.target_soi[5])
            dashboard.ui.textEdit_library_pd_soi_notes.setPlainText(dashboard.target_soi[6])


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryAddAddFieldClicked(dashboard: QtCore.QObject):
    """ 
    Adds a new row to the library packet table in the protocol discovery\add to library packet tab.
    """
    # Add Row
    dashboard.ui.tableWidget_library_pd_packet.setRowCount(dashboard.ui.tableWidget_library_pd_packet.rowCount()+1)
    header_item = QtWidgets.QTableWidgetItem("Field " + str(dashboard.ui.tableWidget_library_pd_packet.rowCount()))
    header_item.setTextAlignment(QtCore.Qt.AlignCenter)
    dashboard.ui.tableWidget_library_pd_packet.setVerticalHeaderItem(dashboard.ui.tableWidget_library_pd_packet.rowCount()-1,header_item)

    # CRC Range
    crc_range_item = QtWidgets.QTableWidgetItem("")
    crc_range_item.setTextAlignment(QtCore.Qt.AlignCenter)
    crc_range_item.setFlags(crc_range_item.flags() ^ QtCore.Qt.ItemIsEnabled)
    crc_range_item.setFlags(crc_range_item.flags() ^ QtCore.Qt.ItemIsEditable)
    dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.rowCount()-1,4,crc_range_item)

    # Is CRC Combobox
    new_combobox = QtWidgets.QComboBox(dashboard, objectName='comboBox2_')
    new_combobox.addItem("True")
    new_combobox.addItem("False")
    new_combobox.setCurrentIndex(1)
    dashboard.ui.tableWidget_library_pd_packet.setCellWidget(dashboard.ui.tableWidget_library_pd_packet.rowCount()-1,3,new_combobox)
    new_combobox.currentIndexChanged.connect(lambda: _slotPD_AddToLibraryIsCRC_Changed(dashboard))
    new_combobox.setProperty("row", dashboard.ui.tableWidget_library_pd_packet.rowCount()-1)

    # Resize the Table
    dashboard.ui.tableWidget_library_pd_packet.resizeRowsToContents()
    dashboard.ui.tableWidget_library_pd_packet.setColumnWidth(0,125)
    dashboard.ui.tableWidget_library_pd_packet.setColumnWidth(1,100)
    dashboard.ui.tableWidget_library_pd_packet.setColumnWidth(3,75)
    dashboard.ui.tableWidget_library_pd_packet.setColumnWidth(4,130)
    dashboard.ui.tableWidget_library_pd_packet.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.Stretch)


@QtCore.pyqtSlot(QtCore.QObject)
def _slotPD_AddToLibraryIsCRC_Changed(dashboard: QtCore.QObject):
    """ 
    Enable/Disable the "CRC Range" item in the protocol discovery add to library packet type table based on "Is CRC" value.
    """
    # Get Row, Value
    row = dashboard.sender().property("row")  # FIX
    current_selection = dashboard.ui.tableWidget_library_pd_packet.cellWidget(row,3).currentText()

    # Enable
    if current_selection == "True":
        dashboard.ui.tableWidget_library_pd_packet.item(row,4).setFlags(dashboard.ui.tableWidget_library_pd_packet.item(row,4).flags() ^ QtCore.Qt.ItemIsEnabled)
        dashboard.ui.tableWidget_library_pd_packet.item(row,4).setFlags(dashboard.ui.tableWidget_library_pd_packet.item(row,4).flags() ^ QtCore.Qt.ItemIsEditable)

    # Disable
    else:
        dashboard.ui.tableWidget_library_pd_packet.item(row,4).setText("")  # Clear existing text
        dashboard.ui.tableWidget_library_pd_packet.item(row,4).setFlags(dashboard.ui.tableWidget_library_pd_packet.item(row,4).flags() ^ QtCore.Qt.ItemIsEnabled)
        dashboard.ui.tableWidget_library_pd_packet.item(row,4).setFlags(dashboard.ui.tableWidget_library_pd_packet.item(row,4).flags() ^ QtCore.Qt.ItemIsEditable)


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryAddRemoveFieldClicked(dashboard: QtCore.QObject):
    """ 
    Removes the current row from the library packet table in the protocol discovery\construct packet tab.
    """
    # Remove Row
    dashboard.ui.tableWidget_library_pd_packet.removeRow(dashboard.ui.tableWidget_library_pd_packet.currentRow())

    # Relabel the Rows
    for rows in range(0,dashboard.ui.tableWidget_library_pd_packet.rowCount()):
        header_item = QtWidgets.QTableWidgetItem("Field " + str(rows+1))
        header_item.setTextAlignment(QtCore.Qt.AlignCenter)
        dashboard.ui.tableWidget_library_pd_packet.setVerticalHeaderItem(rows,header_item)

    # Resize
    dashboard.ui.tableWidget_library_pd_packet.resizeRowsToContents()


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryAddUpClicked(dashboard: QtCore.QObject):
    """ 
    Moves the current field up one position in the field table.
    """
    if dashboard.ui.tableWidget_library_pd_packet.currentRow() != 0:  # Ignore top row
        # Take the Row Above
        above_item0 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()-1,0)
        above_item1 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()-1,1)
        above_item2 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()-1,2)

        # Take the Current Row
        current_item0 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),0)
        current_item1 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),1)
        current_item2 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),2)

        # Set the Current Row
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),0,above_item0)
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),1,above_item1)
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),2,above_item2)

        # Set the Row Above
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()-1,0,current_item0)
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()-1,1,current_item1)
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()-1,2,current_item2)

        # Change the Selected Row
        dashboard.ui.tableWidget_library_pd_packet.setCurrentCell(dashboard.ui.tableWidget_library_pd_packet.currentRow()-1,0)

        # Resize
        dashboard.ui.tableWidget_library_pd_packet.resizeRowsToContents()


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryAddDownClicked(dashboard: QtCore.QObject):
    """ 
    Moves the current field down one position in the field table.
    """
    # Get Bottom Row
    bottom_row = dashboard.ui.tableWidget_library_pd_packet.rowCount()

    # Move it Down
    if dashboard.ui.tableWidget_library_pd_packet.currentRow() != bottom_row-1:  # Ignore bottom row
        # Take the Row Below
        below_item0 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()+1,0)
        below_item1 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()+1,1)
        below_item2 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()+1,2)

        # Take the Current Row
        current_item0 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),0)
        current_item1 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),1)
        current_item2 = dashboard.ui.tableWidget_library_pd_packet.takeItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),2)

        # Set the Current Row
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),0,below_item0)
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),1,below_item1)
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow(),2,below_item2)

        # Set the Row Above
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()+1,0,current_item0)
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()+1,1,current_item1)
        dashboard.ui.tableWidget_library_pd_packet.setItem(dashboard.ui.tableWidget_library_pd_packet.currentRow()+1,2,current_item2)

        # Change the Selected Row
        dashboard.ui.tableWidget_library_pd_packet.setCurrentCell(dashboard.ui.tableWidget_library_pd_packet.currentRow()+1,0)

        # Resize
        dashboard.ui.tableWidget_library_pd_packet.resizeRowsToContents()


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryAddAttacksSelectClicked(dashboard: QtCore.QObject):
    """ 
    This opens a file dialog to select a .py or .msa file as the source of the new attack template.
    """
    # Look for the Flow Graph Files or Multi-Stage Attack File
    directory = ""
    dialog_text = ""
    dialog_filter = ""
    if dashboard.ui.comboBox_library_attacks_attack_type.currentText() == "Multi-Stage":
        directory = os.path.join(fissure.utils.FISSURE_ROOT, "Multi-Stage Attack Files")
        dialog_text = "Select Multi-Stage Attack File..."
        dialog_filter = "Multi-Stage Attack Files (*.msa)"
    else:
        directory = fissure.utils.FISSURE_ROOT
        dialog_text = "Select Python File..."
        dialog_filter = "Python Files (*.py)"

    fpath = str(QtWidgets.QFileDialog.getOpenFileName(None,dialog_text, directory, filter=dialog_filter)[0])

    # If a Valid File
    if fpath != "":
        fname = fpath.rsplit("/",1)[1]
        fname = fname.rsplit(".py",1)[0]
        fname = fname.rsplit(".msa",1)[0]
        dashboard.ui.label_library_attacks_filepath.setText(fpath)
        dashboard.ui.textEdit_library_attacks_new_name.setPlainText(fname)

        dashboard.ui.textEdit_library_attacks_name.setPlainText(fname)
        dashboard.ui.textEdit_library_attacks_new_name.setPlainText(fpath.rsplit("/",1)[1])
    else:
        if dashboard.ui.textEdit_library_attacks_name.toPlainText() != "":
            pass


@qasync.asyncSlot(QtCore.QObject)
async def _slotLibrarySearchSearchLibraryClicked(dashboard: QtCore.QObject):
    """ 
    Sends a message to the HIPRFISR/PD to check the library for occurences of the selected preamble.
    """
    # Get SOI Data
    soi_data = ["","","","","","","","","",""]
    if dashboard.ui.checkBox_library_search_frequency.isChecked():
        soi_data[0] = str(dashboard.ui.textEdit_library_search_frequency.toPlainText())
        soi_data[6] = str(dashboard.ui.textEdit_library_search_frequency_margin.toPlainText())
    if dashboard.ui.checkBox_library_search_modulation.isChecked():
        soi_data[1] = str(dashboard.ui.textEdit_library_search_modulation.toPlainText())
    if dashboard.ui.checkBox_library_search_bandwidth.isChecked():
        soi_data[2] = str(dashboard.ui.textEdit_library_search_bandwidth.toPlainText())
        soi_data[7] = str(dashboard.ui.textEdit_library_search_bandwidth_margin.toPlainText())
    if dashboard.ui.checkBox_library_search_continuous.isChecked():
        soi_data[3] = str(dashboard.ui.comboBox_library_search_continuous.currentText())
    if dashboard.ui.checkBox_library_search_start_frequency.isChecked():
        soi_data[4] = str(dashboard.ui.textEdit_library_search_start_frequency.toPlainText())
        soi_data[8] = str(dashboard.ui.textEdit_library_search_start_frequency_margin.toPlainText())
    if dashboard.ui.checkBox_library_search_end_frequency.isChecked():
        soi_data[5] = str(dashboard.ui.textEdit_library_search_end_frequency.toPlainText())
        soi_data[9] = str(dashboard.ui.textEdit_library_search_end_frequency_margin.toPlainText())

    # Get Field Value
    field_data = ""
    if dashboard.ui.checkBox_library_search_field_value.isChecked():
        # Convert to Binary
        if dashboard.ui.radioButton_library_search_hex.isChecked():
            get_data = str(dashboard.ui.textEdit_library_search_field_value.toPlainText())
            get_data = get_data.replace(' ','')
            field_data = bin(int(get_data, 16))[2:].zfill(int(len(get_data)*4))
        else:
            field_data = str(dashboard.ui.textEdit_library_search_field_value.toPlainText())
            field_data.replace(' ','')

    # Clear Results Table
    dashboard.ui.tableWidget1_library_search_results.setRowCount(0)

    # Send Message
    await dashboard.backend.searchLibrary(soi_data, field_data)

    # Show the Label
    dashboard.ui.label2_library_search_searching.setVisible(True)


@qasync.asyncSlot(QtCore.QObject)
async def _slotLibraryAddAddToLibrary_Clicked(dashboard: QtCore.QObject):
    """ 
    Collects the data to be added to the library and sends it to the HIPRFISR.
    """
    protocol_name = ""
    get_modulation = ""
    new_packet_name = ""
    get_packet_data = []
    get_soi_data = {}
    demodulation_fg_data = {}
    attack_data = {}

    # Protocol Name
    if dashboard.ui.stackedWidget2_library_pd.currentIndex() == 0:
        protocol_name = str(dashboard.ui.textEdit_library_pd_new_protocol.toPlainText())
        protocols = fissure.utils.library.getProtocols(dashboard.backend.library)

        # Empty or Duplicate
        if len(protocol_name) == 0:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Enter valid protocol name.")
            return
        if protocol_name in protocols:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Protocol already exists.")
            return        
    else:
        protocol_name = str(dashboard.ui.comboBox_library_pd_protocol.currentText())

    # Modulation Type
    if dashboard.ui.stackedWidget2_library_pd.currentIndex() == 1:
        get_modulation = str(dashboard.ui.textEdit_library_pd_modulation_type.toPlainText())
        modulation_types = fissure.utils.library.getModulations(dashboard.backend.library, protocol_name)

        # Empty or Duplicate
        if len(get_modulation) == 0:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Enter valid modulation type.")
            return
        if get_modulation in modulation_types:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Modulation type already exists.")
            return

    # Packet Type
    elif dashboard.ui.stackedWidget2_library_pd.currentIndex() == 2:
        # Valid Packet Name
        new_packet_name = str(dashboard.ui.textEdit_library_pd_packet_name.toPlainText())
        packet_types = fissure.utils.library.getPacketTypes(dashboard.backend.library, protocol_name)

        # Empty or Duplicate
        if len(new_packet_name) == 0:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Enter valid packet name.")
            return
        if new_packet_name in packet_types:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Packet type already exists.")
            return

        # Check for Content
        if dashboard.ui.tableWidget_library_pd_packet.rowCount() == 0:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "The number of fields cannot be zero.")
            return

        # Get Packet Data
        for row in range(0,dashboard.ui.tableWidget_library_pd_packet.rowCount()):
            get_packet_data.append([])
            get_packet_data[row].append(str(dashboard.ui.tableWidget_library_pd_packet.item(row,0).text()))
            get_packet_data[row].append(str(dashboard.ui.tableWidget_library_pd_packet.item(row,1).text()))

            # Check Default Values for Binary Characters
            check_default_values = str(dashboard.ui.tableWidget_library_pd_packet.item(row,2).text())
            if set(check_default_values).issubset({'0','1',' '}) and bool(check_default_values):
                get_packet_data[row].append(check_default_values)
            else:
                await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Default values must be binary: 1010 0010 1111...")
                return

            get_packet_data[row].append(str(dashboard.ui.tableWidget_library_pd_packet.cellWidget(row,3).currentText()))
            get_packet_data[row].append(str(dashboard.ui.tableWidget_library_pd_packet.item(row,4).text()))

    # Signal of Interest
    elif dashboard.ui.stackedWidget2_library_pd.currentIndex() == 3:
        # Must Have Subtype/Label
        if len(str(dashboard.ui.textEdit_library_pd_soi_subtype.toPlainText()).replace(" ","")) == 0:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Requires Subtype/Label")
            return

        get_soi_data["soi_name"] = str(dashboard.ui.textEdit_library_pd_soi_subtype.toPlainText())
        get_soi_data["center_frequency"] = str(dashboard.ui.textEdit_library_pd_soi_frequency.toPlainText())
        get_soi_data["start_frequency"] = str(dashboard.ui.textEdit_library_pd_soi_start_frequency.toPlainText())
        get_soi_data["end_frequency"] = str(dashboard.ui.textEdit_library_pd_soi_end_frequency.toPlainText())
        get_soi_data["bandwidth"] = str(dashboard.ui.textEdit_library_pd_soi_bandwidth.toPlainText())
        get_soi_data["continuous"] = str(dashboard.ui.comboBox_library_pd_soi_continuous.currentText())
        get_soi_data["modulation"] = str(dashboard.ui.textEdit_library_pd_soi_modulation.toPlainText())
        get_soi_data["notes"] = str(dashboard.ui.textEdit_library_pd_soi_notes.toPlainText())

    # Demodulation Flow Graph
    elif dashboard.ui.stackedWidget2_library_pd.currentIndex() == 4:
        get_demodulation_fg = str(dashboard.ui.textEdit_library_pd_demodulation_fg.toPlainText())
        get_demodulation_type = str(dashboard.ui.comboBox_library_pd_modulation_types.currentText())
        get_demodulation_hardware = str(dashboard.ui.comboBox_library_pd_hardware.currentText())
        if dashboard.ui.radioButton_library_add_demodulation_fg_stream.isChecked():
            get_sniffer_type = "Stream"
        elif dashboard.ui.radioButton_library_add_demodulation_fg_tagged_stream.isChecked():
            get_sniffer_type = "Tagged Stream"
        elif dashboard.ui.radioButton_library_add_demodulation_fg_msg_pdu.isChecked():
            get_sniffer_type = "Message/PDU"

        # Invalid Demodulation Flow Graph
        if get_demodulation_fg == "":
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Enter valid demodulation flow graph filepath.")
            return
        if get_demodulation_type == "":
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Add modulation type for demodulation flow graph.")
            return

        # Add .py and .grc to "PD Flow Graphs"
        try:
            demod_py_filepath = get_demodulation_fg
            get_demodulation_fg = get_demodulation_fg.rsplit("/",1)[1]

            # Check for Duplicate
            demod_fg_exists = os.path.exists(os.path.join(fissure.utils.get_fg_library_dir(dashboard.backend.os_info), "PD Flow Graphs", get_demodulation_fg))
            if demod_fg_exists:
                await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Duplicate demodulation flow graph name")
                return

            shutil.copy(demod_py_filepath, os.path.join(fissure.utils.get_fg_library_dir(dashboard.backend.os_info), "PD Flow Graphs", get_demodulation_fg))
            demodulation_fg_data["output_type"] = get_sniffer_type
            demodulation_fg_data["filename"] = get_demodulation_fg
            demodulation_fg_data["hardware"] = get_demodulation_hardware
            demodulation_fg_data["modulation_type"] = get_demodulation_type

            demod_grc_file = get_demodulation_fg.replace('.py','.grc')
            demod_grc_filepath = demod_py_filepath.replace('.py','.grc')
            shutil.copy(demod_grc_filepath, os.path.join(fissure.utils.get_fg_library_dir(dashboard.backend.os_info), "PD Flow Graphs", demod_grc_file))
        except:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "New demodulation flow graph requires a valid .py and .grc file with the same name.")
            return

    # Attack
    elif dashboard.ui.stackedWidget2_library_pd.currentIndex() == 5:
        # Get Tree Parent, Attack Name, Hardware
        get_tree_parent = str(dashboard.ui.comboBox_library_attacks_subcategory.currentText())
        get_attack_name = str(dashboard.ui.textEdit_library_attacks_name.toPlainText())
        get_hardware = str(dashboard.ui.comboBox_library_attacks_hardware.currentText())
        get_file_type = str(dashboard.ui.comboBox_library_attacks_file_type.currentText())
        get_new_filename = str(dashboard.ui.textEdit_library_attacks_new_name.toPlainText())
        get_attack_type = str(dashboard.ui.comboBox_library_attacks_attack_type.currentText())

        # Assemble New Attack Filepath, Determine Single-Stage or Multi-Stage
        get_filepath = str(dashboard.ui.label_library_attacks_filepath.text())

        # Invalid Filepath
        if len(get_filepath) == 0:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, 'Select attack file.')
            return

        # Invalid Attack Template Name
        if len(get_attack_name) == 0:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, 'Enter new attack template name.')
            return

        # Invalid Attack Name
        if len(get_new_filename) == 0:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, 'Enter new attack name.')
            return

        # Format Filepath
        if get_filepath.rsplit(".",1)[-1] == "py":
            # Force it to End with ".py"
            if get_new_filename.rsplit(".",1)[-1] != "py":
                get_new_filename = get_new_filename + ".py"
                dashboard.ui.textEdit_library_attacks_new_name.setPlainText(get_new_filename)
            else:
                get_new_filename = str(dashboard.ui.textEdit_library_attacks_new_name.toPlainText())
        elif get_filepath.rsplit(".",1)[1] == "msa":
            get_new_filename = get_filepath.rsplit("/",1)[-1]
        else:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, 'Attack needs to end with ".py" or ".msa"')
            return
        
        # Multi-Stage Category Name
        if get_attack_type == "Multi-Stage":  # Multi-Stage and Fuzzing types not supported yet
            get_tree_parent = "Multi-Stage"

        # Get Modulation Type
        if get_attack_type == "Single-Stage":
            get_modulation = str(dashboard.ui.comboBox_library_attacks_modulation.currentText())

            # No Modulation Type
            if len(get_modulation) == 0:
                await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, 'Requires modulation type.')
                return

        # Check if File Already Exists
        if os.path.isfile(os.path.join(fissure.utils.get_fg_library_dir(dashboard.backend.os_info), "Single-Stage Flow Graphs", get_new_filename)):
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, 'File already exists in "Single-Stage Flow Graphs" folder.')
            return

        # Check if Attack Already Exists for the Protocol, Modulation, and Hardware Combination
        if fissure.utils.library.getAttackFilename(
            dashboard.backend.library, 
            protocol_name, 
            get_new_filename, 
            get_modulation, 
            get_hardware,
            fissure.utils.get_library_version()
        ) != None:
            await fissure.Dashboard.UI_Components.Qt5.async_ok_dialog(dashboard, "Attack name already exists for this protocol/modulation/hardware combination.")
            return

        # Assemble Message
        attack_data["protocol"] = protocol_name
        attack_data["attack_name"] = get_attack_name
        attack_data["modulation_type"] = get_modulation
        attack_data["hardware"] = get_hardware
        attack_data["attack_type"] = get_file_type
        attack_data["filename"] = get_new_filename
        attack_data["category_name"] = get_tree_parent

        # Add to "Flow Graph Library/Single-Stage Flow Graphs"
        shutil.copy(get_filepath, os.path.join(fissure.utils.get_fg_library_dir(dashboard.backend.os_info), "Single-Stage Flow Graphs", get_new_filename))

        # Add .grc File to "Flow Graph Library/Single-Stage Flow Graphs"
        if dashboard.ui.checkBox_library_attacks_grc_file.isChecked():
            shutil.copy(get_filepath.replace(".py",".grc"), os.path.join(fissure.utils.get_fg_library_dir(dashboard.backend.os_info), "Single-Stage Flow Graphs", get_new_filename.replace(".py",".grc")))

    # Valid Protocol Name
    if protocol_name != "":
        # Send Message to HIPRFISR/Protocol Discovery
        await dashboard.backend.addToLibrary(protocol_name, new_packet_name, get_packet_data, get_soi_data, get_modulation, demodulation_fg_data, attack_data, [])


def _slotPD_DemodHardwareChanged(dashboard: QtCore.QObject):
    """ 
    Updates the list of demodulation flow graphs. Not a slot.
    """
    # Get Hardware
    get_hardware = str(dashboard.ui.comboBox_pd_demod_hardware.currentText()).split(' - ')[0]

    # Clear the List
    dashboard.ui.listWidget_pd_flow_graphs_all_fgs.clear()

    # Get All Demodulation Flow Graphs
    all_demod_fgs = fissure.utils.library.getDemodulationFlowGraphFilenames(
        dashboard.backend.library, 
        protocol = None, 
        modulation = None, 
        hardware = get_hardware,
        version = fissure.utils.get_library_version()
    )

    # Update the List Widget
    for fg in sorted(all_demod_fgs,key=str.lower):
        dashboard.ui.listWidget_pd_flow_graphs_all_fgs.addItem(fg)


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryBrowseChanged(dashboard: QtCore.QObject):
    """ 
    Loads a table from the Dashboard's cached version of the FISSURE PostgreSQL database.
    """
    # Clear the Table
    dashboard.ui.tableWidget1_library_browse.setRowCount(0)
    dashboard.ui.tableWidget1_library_browse.setColumnCount(0)

    # Populate the Table
    get_table_name = str(dashboard.ui.comboBox_library_browse.currentText())

    if get_table_name == "archive_collection":
        get_rows = fissure.utils.library.getArchiveCollection(dashboard.backend.library)
        headers = ["id", "name", "file_list", "filepath", "files", "format", "size", "notes", "parent_id", "created_at"]
    elif get_table_name == "archive_favorites":
        get_rows = fissure.utils.library.getArchiveFavorites(dashboard.backend.library)
        headers = ["id", "file_name", "date", "format", "modulation", "notes", "protocol", "sample_rate", "samples", "size", "tuned_frequency"]
    elif get_table_name == "attack_categories":
        get_rows = fissure.utils.library.getAttackCategories(dashboard.backend.library)
        headers = ["id", "category_name", "parent"]
    elif get_table_name == "attacks":
        get_rows = fissure.utils.library.getAttacks(dashboard.backend.library, None, None)
        headers = ["id", "protocol", "attack_name", "modulation_type", "hardware", "attack_type", "filename", "category_name", "version"]
    elif get_table_name == "conditioner_flow_graphs":
        get_rows = fissure.utils.library.getConditionerFlowGraphsTable(dashboard.backend.library)
        headers = ["id", "isolation_category", "isolation_method", "hardware", "file_type", "data_type", "version", "parameter_names", "parameter_values", "parameter_labels", "filepath"] 
    elif get_table_name == "demodulation_flow_graphs":
        get_rows = fissure.utils.library.getDemodulationFlowGraphs(dashboard.backend.library)
        headers = ["id", "protocol", "modulation_type", "hardware", "filename", "output_type", "version"]
    elif get_table_name == "detector_flow_graphs":
        get_rows = fissure.utils.library.getDetectorFlowGraphsTable(dashboard.backend.library)
        headers = ["id", "detector_type", "hardware", "filename", "file_type", "version"]
    elif get_table_name == "inspection_flow_graphs":
        get_rows = fissure.utils.library.getInspectionFlowGraphs(dashboard.backend.library)
        headers = ["id", "hardware", "python_file", "version"]
    elif get_table_name == "modulation_types":
        get_rows = fissure.utils.library.getModulationTypes(dashboard.backend.library)
        headers = ["id", "protocol", "modulation_type"]
    elif get_table_name == "packet_types":
        get_rows = fissure.utils.library.getPacketTypesTable(dashboard.backend.library)
        headers = ["id", "protocol", "packet_name", "dissector", "fields", "sort_order"]
    elif get_table_name == "protocols":
        get_rows = fissure.utils.library.getProtocolsTable(dashboard.backend.library)
        headers = ["id", "protocol_name", "data_rates", "median_packet_lengths"]
    elif get_table_name == "soi_data":
        get_rows = fissure.utils.library.getSOIs(dashboard.backend.library, None)
        headers = ["id", "protocol", "soi_name", "center_frequency", "start_frequency", "end_frequency", "bandwidth", "continuous", "modulation", "notes"]   
    elif get_table_name == "triggers":
        get_rows = fissure.utils.library.getTriggersTable(dashboard.backend.library)
        headers = ["id", "category", "trigger_name", "default_settings", "filename", "file_type", "version"]
    else:
        return

    # Create Rows and Columns
    dashboard.ui.tableWidget1_library_browse.setRowCount(len(get_rows))
    dashboard.ui.tableWidget1_library_browse.setColumnCount(len(get_rows[0]))
    
    # Add Headers
    for index, header in enumerate(headers):
        header_item = QtWidgets.QTableWidgetItem(header)
        header_item.setTextAlignment(QtCore.Qt.AlignCenter)
        dashboard.ui.tableWidget1_library_browse.setHorizontalHeaderItem(index, header_item)

    # Add Items
    for r in range(0,len(get_rows)):
        for c in range(0,len(get_rows[0])):
            new_item = QtWidgets.QTableWidgetItem(str(get_rows[r][c]))
            new_item.setTextAlignment(QtCore.Qt.AlignCenter)
            dashboard.ui.tableWidget1_library_browse.setItem(r,c, QtWidgets.QTableWidgetItem(new_item))

    # Resize the Table
    dashboard.ui.tableWidget1_library_browse.resizeRowsToContents()


@QtCore.pyqtSlot(QtCore.QObject)
def _slotLibraryBrowsePgAdmin4_Clicked(dashboard: QtCore.QObject):
    """ 
    Opens a browser to pgAdmin 4 for viewing the FISSURE PostgreSQL database tables.
    """
    # Open a Browser
    os.system("xdg-open http://localhost:3000/browser/")


@qasync.asyncSlot(QtCore.QObject)
async def _slotLibraryBrowseDeleteRowClicked(dashboard: QtCore.QObject):
    """ 
    Sends a message to the HIPRFISR to delete a row in the database.
    """
    # Get Table and Row ID
    get_table_name = str(dashboard.ui.comboBox_library_browse.currentText())
    try:
        current_row = dashboard.ui.tableWidget1_library_browse.currentRow()
        get_row_id = str(dashboard.ui.tableWidget1_library_browse.item(current_row, 0).text())
    except:
        dashboard.logger.info("Select a table row to delete.")

    # Ask to Delete Row and then Files for Certain Tables
    delete_files = False
    ret = await fissure.Dashboard.UI_Components.Qt5.async_yes_no_dialog(dashboard, "Delete row with id: " + get_row_id + "?")
    if ret == QtWidgets.QMessageBox.Yes:
        if get_table_name == "demodulation_flow_graphs":
            get_filename = str(dashboard.ui.tableWidget1_library_browse.item(current_row, 4).text())
            ret = await fissure.Dashboard.UI_Components.Qt5.async_yes_no_dialog(dashboard, "Also delete filename: " + get_filename + "?")
            if ret == QtWidgets.QMessageBox.Yes:
                delete_files = True
        elif get_table_name == "inspection_flow_graphs":
            get_filename = str(dashboard.ui.tableWidget1_library_browse.item(current_row, 2).text())
            ret = await fissure.Dashboard.UI_Components.Qt5.async_yes_no_dialog(dashboard, "Also delete files (.py & .grc) for: " + get_filename + "?")
            if ret == QtWidgets.QMessageBox.Yes:
                delete_files = True
        elif get_table_name == "soi_data":
            pass  # Delete IQ files
        elif get_table_name == "triggers":
            get_filename = str(dashboard.ui.tableWidget1_library_browse.item(current_row, 4).text())
            ret = await fissure.Dashboard.UI_Components.Qt5.async_yes_no_dialog(dashboard, "Also delete filename: " + get_filename + "?")
            if ret == QtWidgets.QMessageBox.Yes:
                delete_files = True

        # Send Message to HIPRFISR/Protocol Discovery
        if get_row_id is not None:
            await dashboard.backend.removeFromLibrary(get_table_name, get_row_id, delete_files)

