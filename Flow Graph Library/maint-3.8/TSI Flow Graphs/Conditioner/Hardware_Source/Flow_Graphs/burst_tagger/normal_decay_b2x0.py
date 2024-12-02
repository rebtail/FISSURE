#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.8.5.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time


class normal_decay_b2x0(gr.top_block):

    def __init__(self, antenna='TX/RX', channel="A:A", decay='.0002', filepath="/home/user/Conditioner/Data/tpms/four_tires2.iq", frequency='311e6', gain='70', sample_rate='1e6', serial='', threshold='.004'):
        gr.top_block.__init__(self, "Not titled yet")

        ##################################################
        # Parameters
        ##################################################
        self.antenna = antenna
        self.channel = channel
        self.decay = decay
        self.filepath = filepath
        self.frequency = frequency
        self.gain = gain
        self.sample_rate = sample_rate
        self.serial = serial
        self.threshold = threshold

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
            ",".join((serial, "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0_0.set_subdev_spec(channel, 0)
        self.uhd_usrp_source_0_0.set_center_freq(float(frequency), 0)
        self.uhd_usrp_source_0_0.set_gain(float(gain), 0)
        self.uhd_usrp_source_0_0.set_antenna(antenna, 0)
        self.uhd_usrp_source_0_0.set_samp_rate(float(sample_rate))
        self.uhd_usrp_source_0_0.set_time_unknown_pps(uhd.time_spec())
        self.blocks_threshold_ff_0_0 = blocks.threshold_ff(float(threshold), float(threshold), 0)
        self.blocks_tagged_file_sink_0 = blocks.tagged_file_sink(gr.sizeof_gr_complex*1, int(float(sample_rate)))
        self.blocks_rms_xx_0 = blocks.rms_ff(float(decay))
        self.blocks_float_to_short_1 = blocks.float_to_short(1, 1)
        self.blocks_delay_1 = blocks.delay(gr.sizeof_gr_complex*1, 5000)
        self.blocks_complex_to_mag_squared_0_0 = blocks.complex_to_mag_squared(1)
        self.blocks_burst_tagger_1 = blocks.burst_tagger(gr.sizeof_gr_complex)
        self.blocks_burst_tagger_1.set_true_tag('burst',True)
        self.blocks_burst_tagger_1.set_false_tag('burst',False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_burst_tagger_1, 0), (self.blocks_tagged_file_sink_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0, 0), (self.blocks_rms_xx_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.blocks_burst_tagger_1, 0))
        self.connect((self.blocks_float_to_short_1, 0), (self.blocks_burst_tagger_1, 1))
        self.connect((self.blocks_rms_xx_0, 0), (self.blocks_threshold_ff_0_0, 0))
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_float_to_short_1, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_complex_to_mag_squared_0_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_delay_1, 0))


    def get_antenna(self):
        return self.antenna

    def set_antenna(self, antenna):
        self.antenna = antenna
        self.uhd_usrp_source_0_0.set_antenna(self.antenna, 0)

    def get_channel(self):
        return self.channel

    def set_channel(self, channel):
        self.channel = channel

    def get_decay(self):
        return self.decay

    def set_decay(self, decay):
        self.decay = decay
        self.blocks_rms_xx_0.set_alpha(float(self.decay))

    def get_filepath(self):
        return self.filepath

    def set_filepath(self, filepath):
        self.filepath = filepath

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.uhd_usrp_source_0_0.set_center_freq(float(self.frequency), 0)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0_0.set_gain(float(self.gain), 0)

    def get_sample_rate(self):
        return self.sample_rate

    def set_sample_rate(self, sample_rate):
        self.sample_rate = sample_rate
        self.uhd_usrp_source_0_0.set_samp_rate(float(self.sample_rate))

    def get_serial(self):
        return self.serial

    def set_serial(self, serial):
        self.serial = serial

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.blocks_threshold_ff_0_0.set_hi(float(self.threshold))
        self.blocks_threshold_ff_0_0.set_lo(float(self.threshold))




def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--antenna", dest="antenna", type=str, default='TX/RX',
        help="Set TX/RX [default=%(default)r]")
    parser.add_argument(
        "--channel", dest="channel", type=str, default="A:A",
        help="Set A:A [default=%(default)r]")
    parser.add_argument(
        "--decay", dest="decay", type=str, default='.0002',
        help="Set .0002 [default=%(default)r]")
    parser.add_argument(
        "--filepath", dest="filepath", type=str, default="/home/user/Conditioner/Data/tpms/four_tires2.iq",
        help="Set /home/user/Conditioner/Data/tpms/four_tires2.iq [default=%(default)r]")
    parser.add_argument(
        "--frequency", dest="frequency", type=str, default='311e6',
        help="Set 311e6 [default=%(default)r]")
    parser.add_argument(
        "--gain", dest="gain", type=str, default='70',
        help="Set 70 [default=%(default)r]")
    parser.add_argument(
        "--sample-rate", dest="sample_rate", type=str, default='1e6',
        help="Set 1e6 [default=%(default)r]")
    parser.add_argument(
        "--serial", dest="serial", type=str, default='',
        help="Set serial [default=%(default)r]")
    parser.add_argument(
        "--threshold", dest="threshold", type=str, default='.004',
        help="Set .004 [default=%(default)r]")
    return parser


def main(top_block_cls=normal_decay_b2x0, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(antenna=options.antenna, channel=options.channel, decay=options.decay, filepath=options.filepath, frequency=options.frequency, gain=options.gain, sample_rate=options.sample_rate, serial=options.serial, threshold=options.threshold)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    tb.wait()


if __name__ == '__main__':
    main()
