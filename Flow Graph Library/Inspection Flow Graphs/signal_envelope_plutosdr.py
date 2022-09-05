#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Signal Envelope Plutosdr
# Generated: Sun Sep  4 22:18:52 2022
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import iio
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sip
import sys
from gnuradio import qtgui


class signal_envelope_plutosdr(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Signal Envelope Plutosdr")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Signal Envelope Plutosdr")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "signal_envelope_plutosdr")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.sample_rate = sample_rate = 1e6
        self.rx_gain = rx_gain = 64
        self.rx_frequency = rx_frequency = 2412
        self.ip_address = ip_address = "192.168.2.1"
        self.decimation = decimation = 1

        ##################################################
        # Blocks
        ##################################################
        self._sample_rate_options = [1e6, 5e6, 10e6, 20e6]
        self._sample_rate_labels = ["1 MS/s", "5 MS/s", "10 MS/s", "20 MS/s"]
        self._sample_rate_tool_bar = Qt.QToolBar(self)
        self._sample_rate_tool_bar.addWidget(Qt.QLabel('Sample Rate'+": "))
        self._sample_rate_combo_box = Qt.QComboBox()
        self._sample_rate_tool_bar.addWidget(self._sample_rate_combo_box)
        for label in self._sample_rate_labels: self._sample_rate_combo_box.addItem(label)
        self._sample_rate_callback = lambda i: Qt.QMetaObject.invokeMethod(self._sample_rate_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._sample_rate_options.index(i)))
        self._sample_rate_callback(self.sample_rate)
        self._sample_rate_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_sample_rate(self._sample_rate_options[i]))
        self.top_grid_layout.addWidget(self._sample_rate_tool_bar, 0, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,1)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self._rx_gain_range = Range(0, 71, 1, 64, 200)
        self._rx_gain_win = RangeWidget(self._rx_gain_range, self.set_rx_gain, '              Gain:', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_gain_win, 1, 0, 1, 4)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(1,2)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,4)]
        self._rx_frequency_range = Range(325, 3800, .1, 2412, 200)
        self._rx_frequency_win = RangeWidget(self._rx_frequency_range, self.set_rx_frequency, ' Freq. (MHz):', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rx_frequency_win, 2, 0, 1, 4)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(2,3)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,4)]
        self._decimation_options = [1,10,100,1000]
        self._decimation_labels = ["1","10","100","1000"]
        self._decimation_tool_bar = Qt.QToolBar(self)
        self._decimation_tool_bar.addWidget(Qt.QLabel('  Keep 1 in N'+": "))
        self._decimation_combo_box = Qt.QComboBox()
        self._decimation_tool_bar.addWidget(self._decimation_combo_box)
        for label in self._decimation_labels: self._decimation_combo_box.addItem(label)
        self._decimation_callback = lambda i: Qt.QMetaObject.invokeMethod(self._decimation_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._decimation_options.index(i)))
        self._decimation_callback(self.decimation)
        self._decimation_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_decimation(self._decimation_options[i]))
        self.top_grid_layout.addWidget(self._decimation_tool_bar, 0, 2, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,1)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(2,3)]
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	100000, #size
        	sample_rate/decimation, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.1)
        self.qtgui_time_sink_x_0.set_y_axis(-.1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.005, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 3, 0, 20, 4)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(3,23)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,4)]
        self.pluto_source_0 = iio.pluto_source("ip:" + str(ip_address), int(float(rx_frequency)*1e6), int(float(sample_rate)), int(20000000), 0x8000, False, True, True, "manual", float(rx_gain), '', True)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, decimation)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.pluto_source_0, 0), (self.blocks_keep_one_in_n_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "signal_envelope_plutosdr")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self._sample_rate_callback(self.sample_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.sample_rate/self.decimation)
        self.pluto_source_0.set_params(int(float(self.rx_frequency)*1e6), int(float(self.sample_rate)), int(20000000), False, True, True, "manual", float(self.rx_gain), '', True)

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.pluto_source_0.set_params(int(float(self.rx_frequency)*1e6), int(float(self.sample_rate)), int(20000000), False, True, True, "manual", float(self.rx_gain), '', True)

    def get_rx_frequency(self):
        return self.rx_frequency

    def set_rx_frequency(self, rx_frequency):
        self.rx_frequency = rx_frequency
        self.pluto_source_0.set_params(int(float(self.rx_frequency)*1e6), int(float(self.sample_rate)), int(20000000), False, True, True, "manual", float(self.rx_gain), '', True)

    def get_ip_address(self):
        return self.ip_address

    def set_ip_address(self, ip_address):
        self.ip_address = ip_address

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self._decimation_callback(self.decimation)
        self.qtgui_time_sink_x_0.set_samp_rate(self.sample_rate/self.decimation)
        self.blocks_keep_one_in_n_0.set_n(self.decimation)


def main(top_block_cls=signal_envelope_plutosdr, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()