# -*- coding: UTF-8 -*-
# Copyright 2011 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: $

class InvalidVersionStringError(Exception):
    """
    Raised if anything goes wrong with parsing a version string
    """

    def __init__(self, version_string):
        self.version_string = version_string

    def __str__(self):
        return '\'' + self.version_string + '\''

class Version(object):
    """
    A class representing a simple version like 1.10.3
    """

    def __init__(self, version_string):

        self.version_components = []

        if type(version_string) != str:
            raise InvalidVersionStringError("Version argument is not a string")

        components = version_string.split('.')
        for comp in components:
            try :
                self.version_components.append(int(comp))
            except:
                raise InvalidVersionStringError(version_string)

    def __str__(self):
        return self.version_components.join('.')

    def __eq__(self, other):
        return self.compare_to(other) == 0

    def __ne__(self, other):
        return self.compare_to(other) != 0

    def __lt__(self, other):
        return self.compare_to(other) < 0

    def __gt__(self, other):
        return self.compare_to(other) > 0

    def __le__(self, other):
        return self.compare_to(other) <= 0

    def __ge__(self, other):
        return self.compare_to(other) >= 0

    def compare_to(self, other):
        idx = 0
        own_length = len(self.version_components)
        other_length = len(other.version_components)

        while(True):
            if own_length <= idx:
                if other_length <= idx:
                    return 0
                return -1
            if other_length <= idx:
                return 1

            if self.version_components[idx] < other.version_components[idx]:
                return -1
            if self.version_components[idx] > other.version_components[idx]:
                return 1

            idx += 1
