"""
The class Racos represents Racos algorithm. It's inherited from RacosC.

Author:
    Yu-Ren Liu

"""

"""
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

 Copyright (C) 2017 Nanjing University, Nanjing, China
 """

import time

from zoo.algos.racos import RacosClassification
from zoo.algos.racos import RacosCommon
from zoo.utils import my_global


class Racos(RacosCommon):

    def __init__(self):
        RacosC.__init__(self)

    # racos optimization function
    def opt(self, parameter, ub=1):
        self.clear()
        self.set_parameters(parameter)
        t = self._parameter.get_budget() / self._parameter.get_negative_size()
        for i in range(t):
            if i == 0:
                time_log1 = time.time()
            for j in range(len(self._negative_data)):
                if my_global.rand.random() < self._parameter.get_probability():
                    classifier = RacosClassification(
                        self._parameter.get_objective().get_dim(), self._positive_data, self._negative_data, ub)
                    classifier.mixed_classification()
                    x = classifier.rand_sample()
                    ins = self._parameter.get_objective().construct_instance(x)
                else:
                    ins = self.distinct_sample(self._parameter.get_objective().get_dim())
                self._data.append(ins)
            self.selection()
            self._best_solution = self._positive_data[0]
            if i == 4:
                time_log2 = time.time()
                expected_time = t * (time_log2 - time_log1) / 5
                if expected_time > 5:
                    print 'expected run time is %f s:' % expected_time
        return self._best_solution

