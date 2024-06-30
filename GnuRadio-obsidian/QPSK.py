#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: QPSK
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
import math
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class QPSK(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "QPSK", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("QPSK")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "QPSK")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.qpsk = qpsk = [ -1-1j,-1+1j,+1-1j,1+1j ]
        self.delay = delay = 0
        self.btis_per_chunk_qpsk = btis_per_chunk_qpsk = 2

        ##################################################
        # Blocks
        ##################################################

        self._delay_range = qtgui.Range(0, 100, 1, 0, 200)
        self._delay_win = qtgui.RangeWidget(self._delay_range, self.set_delay, "'delay'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._delay_win)
        self.qtgui_time_sink_x_0_4_0_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_4_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_4_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_4_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_4_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_4_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_4_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_4_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_4_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_4_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_4_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_4_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_4_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_4_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_4_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_4_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_4_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_4_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_4_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_4_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_4_0_0_win)
        self.qtgui_time_sink_x_0_4_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_4_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_4_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_4_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_4_0.enable_tags(True)
        self.qtgui_time_sink_x_0_4_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_4_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_4_0.enable_grid(False)
        self.qtgui_time_sink_x_0_4_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_4_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_4_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_4_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_4_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_4_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_4_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_4_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_4_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_4_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_4_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_4_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_4_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(1,  firdes.low_pass(1.0,samp_rate,900,300), 1.5e3, samp_rate)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(qpsk, 1)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, 14)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(2, gr.GR_MSB_FIRST)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, delay)
        self.blocks_complex_to_float_0_0 = blocks.complex_to_float(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)
        self.analog_random_source_x_0_0_0_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 1000))), True)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(10)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.analog_random_source_x_0_0_0_0_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.qtgui_time_sink_x_0_4_0, 1))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.qtgui_time_sink_x_0_4_0_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.qtgui_time_sink_x_0_4_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_time_sink_x_0_4_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_complex_to_float_0_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "QPSK")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps( firdes.low_pass(1.0,self.samp_rate,900,300))
        self.qtgui_time_sink_x_0_4_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_4_0_0.set_samp_rate(self.samp_rate)

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk
        self.digital_chunks_to_symbols_xx_0.set_symbol_table(self.qpsk)

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0.set_dly(int(self.delay))

    def get_btis_per_chunk_qpsk(self):
        return self.btis_per_chunk_qpsk

    def set_btis_per_chunk_qpsk(self, btis_per_chunk_qpsk):
        self.btis_per_chunk_qpsk = btis_per_chunk_qpsk




def main(top_block_cls=QPSK, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
