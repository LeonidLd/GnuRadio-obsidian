#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: PSK_TEST
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class PSK_TEST(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "PSK_TEST", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("PSK_TEST")
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

        self.settings = Qt.QSettings("GNU Radio", "PSK_TEST")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.btis_per_chunk_bpsk = btis_per_chunk_bpsk = 1
        self.bpsk = bpsk = [-1+0j,1+0j]
        self.soft = soft = 2
        self.samp_rate = samp_rate = 32000
        self.qpsk = qpsk = [ -1-1j,-1+1j,+1-1j,1+1j ]
        self.delay = delay = 0
        self.constellation = constellation = bpsk
        self.btis_per_chunk_qpsk = btis_per_chunk_qpsk = 2
        self.btis_per_chunk_QAM = btis_per_chunk_QAM = 4
        self.btis_per_chunk = btis_per_chunk = btis_per_chunk_bpsk
        self.BPSK = BPSK = digital.constellation_bpsk().base()
        self.BPSK.set_npwr(1.0)

        ##################################################
        # Blocks
        ##################################################

        # Create the options list
        self._constellation_options = [[(-1+0j), (1+0j)], [(-1-1j), (-1+1j), (1-1j), (1+1j)]]
        # Create the labels list
        self._constellation_labels = ['bpsk', 'qpsk']
        # Create the combo box
        self._constellation_tool_bar = Qt.QToolBar(self)
        self._constellation_tool_bar.addWidget(Qt.QLabel("'constellation'" + ": "))
        self._constellation_combo_box = Qt.QComboBox()
        self._constellation_tool_bar.addWidget(self._constellation_combo_box)
        for _label in self._constellation_labels: self._constellation_combo_box.addItem(_label)
        self._constellation_callback = lambda i: Qt.QMetaObject.invokeMethod(self._constellation_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._constellation_options.index(i)))
        self._constellation_callback(self.constellation)
        self._constellation_combo_box.currentIndexChanged.connect(
            lambda i: self.set_constellation(self._constellation_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._constellation_tool_bar)
        # Create the options list
        self._btis_per_chunk_options = [1, 2]
        # Create the labels list
        self._btis_per_chunk_labels = ['btis_per_chunk_bpsk', 'btis_per_chunk_qpsk']
        # Create the combo box
        # Create the radio buttons
        self._btis_per_chunk_group_box = Qt.QGroupBox("'btis_per_chunk'" + ": ")
        self._btis_per_chunk_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._btis_per_chunk_button_group = variable_chooser_button_group()
        self._btis_per_chunk_group_box.setLayout(self._btis_per_chunk_box)
        for i, _label in enumerate(self._btis_per_chunk_labels):
            radio_button = Qt.QRadioButton(_label)
            self._btis_per_chunk_box.addWidget(radio_button)
            self._btis_per_chunk_button_group.addButton(radio_button, i)
        self._btis_per_chunk_callback = lambda i: Qt.QMetaObject.invokeMethod(self._btis_per_chunk_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._btis_per_chunk_options.index(i)))
        self._btis_per_chunk_callback(self.btis_per_chunk)
        self._btis_per_chunk_button_group.buttonClicked[int].connect(
            lambda i: self.set_btis_per_chunk(self._btis_per_chunk_options[i]))
        self.top_layout.addWidget(self._btis_per_chunk_group_box)
        self._soft_range = qtgui.Range(2, 10, 2, 2, 200)
        self._soft_win = qtgui.RangeWidget(self._soft_range, self.set_soft, "'soft'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._soft_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


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
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
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
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(constellation, 1)
        self._delay_range = qtgui.Range(0, 100, 1, 0, 200)
        self._delay_win = qtgui.RangeWidget(self._delay_range, self.set_delay, "'delay'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._delay_win)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, 100)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(btis_per_chunk, gr.GR_MSB_FIRST)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_complex_to_float_0_0 = blocks.complex_to_float(1)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)
        self.analog_random_source_x_0_0_0_0_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 255, 1000))), True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0_0_0_0_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_complex_to_float_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.qtgui_const_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "PSK_TEST")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_btis_per_chunk_bpsk(self):
        return self.btis_per_chunk_bpsk

    def set_btis_per_chunk_bpsk(self, btis_per_chunk_bpsk):
        self.btis_per_chunk_bpsk = btis_per_chunk_bpsk
        self.set_btis_per_chunk(self.btis_per_chunk_bpsk)

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk
        self.set_constellation(self.bpsk)

    def get_soft(self):
        return self.soft

    def set_soft(self, soft):
        self.soft = soft

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay

    def get_constellation(self):
        return self.constellation

    def set_constellation(self, constellation):
        self.constellation = constellation
        self._constellation_callback(self.constellation)
        self.digital_chunks_to_symbols_xx_0.set_symbol_table(self.constellation)

    def get_btis_per_chunk_qpsk(self):
        return self.btis_per_chunk_qpsk

    def set_btis_per_chunk_qpsk(self, btis_per_chunk_qpsk):
        self.btis_per_chunk_qpsk = btis_per_chunk_qpsk

    def get_btis_per_chunk_QAM(self):
        return self.btis_per_chunk_QAM

    def set_btis_per_chunk_QAM(self, btis_per_chunk_QAM):
        self.btis_per_chunk_QAM = btis_per_chunk_QAM

    def get_btis_per_chunk(self):
        return self.btis_per_chunk

    def set_btis_per_chunk(self, btis_per_chunk):
        self.btis_per_chunk = btis_per_chunk
        self._btis_per_chunk_callback(self.btis_per_chunk)

    def get_BPSK(self):
        return self.BPSK

    def set_BPSK(self, BPSK):
        self.BPSK = BPSK




def main(top_block_cls=PSK_TEST, options=None):

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
