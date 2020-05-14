# -*- coding: utf-8 -*-
from __future__ import absolute_import
from PyQt5.QtWidgets import QAction, QApplication, QMessageBox
from puddlestuff.plugins import add_shortcuts, status
from datetime import timedelta, datetime
import os
from puddlestuff.audioinfo import lngtime
from puddlestuff.puddleobjects import progress
import time
import six
from six.moves import zip

def init(parent=None):
    action = QAction('Add 2 seconds to modified time', parent)
    action.triggered.connect(lambda: add_seconds(parent))
    action.setShortcut('Ctrl+M')
    
    def sep():
        k = QAction(parent)
        k.setSeparator(True)
        return k
    add_shortcuts('&Plugins', [sep(), action, sep()])

def add_seconds(parent=None):
    if status['previewmode']:
        QMessageBox.information(parent, 'puddletag',
            QApplication.translate("Previews",
                'You need to disable preview mode first.'))
        return

    files = status['selectedfiles']
    rows = status['selectedrows']
    def func():
        for row, f in zip(rows, files):
            modified_time = lngtime(f['__modified'])
            modified_time = datetime.fromtimestamp(modified_time) + timedelta(seconds=2)
            accessed_time = lngtime(f['__accessed'])
            try:
                os.utime(f.filepath, (accessed_time, time.mktime(modified_time.timetuple())))
            except (IOError, OSError) as e:
                filename = f[audioinfo.PATH]
                m = six.text_type(QApplication.translate("Defaults",
                    'An error occured while setting the modification time of <b>%1</b>. (%2)').arg(filename).arg(e.strerror))
                if row == rows[-1]:
                    yield m, 1
                else:
                    yield m, len(rows)

    s = progress(func, QApplication.translate("Adding 2 seconds to mod times...",
        'Setting modification time '), len(files))
    s(parent)