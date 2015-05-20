# -*- coding: utf-8 -*-
#
# This file is part of Glances.
#
# Copyright (C) 2015 Nicolargo <nicolas@nicolargo.com>
#
# Glances is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Glances is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Manage bars for Glances output."""

# Import system lib
import locale
from math import modf


class Bar(object):

    r"""Manage bar (progression or status).

    import sys
    import time
    b = Bar(10)
    for p in range(0, 100):
        b.percent = p
        print("\r%s" % b),
        time.sleep(0.1)
        sys.stdout.flush()
    """

    def __init__(self, size,
                 pre_char='[',
                 post_char=']',
                 empty_char='_',
                 with_text=True):
        # Bar size
        self.__size = size
        # Bar current percent
        self.__percent = 0
        # Char used for the decoration
        self.__pre_char = pre_char
        self.__post_char = post_char
        self.__empty_char = empty_char
        self.__with_text = with_text
        # Char used for the bar
        self.curses_bars = self.__get_curses_bars()

    def __get_curses_bars(self):
        # Return the chars used to display the bar
        if locale.getdefaultlocale()[1] == 'UTF-8':
            return [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
        else:
            return [" ", " ", " ", " ", "|", "|", "|", "|", "|"]

    @property
    def size(self, with_decoration=False):
        # Return the bar size, with or without decoration
        if with_decoration:
            return self.__size
        if self.__with_text:
            return self.__size - 6

    # @size.setter
    # def size(self, value):
    #     self.__size = value

    @property
    def percent(self):
        return self.__percent

    @percent.setter
    def percent(self, value):
        assert value >= 0
        assert value <= 100
        self.__percent = value

    def __str__(self):
        """Return the bars."""
        frac, whole = modf(self.size * self.percent / 100.0)
        ret = self.curses_bars[8] * int(whole)
        if frac > 0:
            ret += self.curses_bars[int(frac * 8)]
            whole += 1
        ret += self.__empty_char * int(self.size - whole)
        if self.__with_text:
            ret = '{0}{1:>5}%'.format(ret, self.percent)
        return self.__pre_char + ret + self.__post_char
