# -*- coding: utf-8 -*-
from __future__ import division
# python imports
from math import degrees
import numpy as np
# pyfuzzy imports
from fuzzy.storage.fcl.Reader import Reader


class FuzzyController:
    global counter
    counter = 0

    def __init__(self, fcl_path):
        self.system = Reader().load_from_file(fcl_path)

    def _make_input(self, world):
        return dict(
            cp=world.x,
            cv=world.v,
            pa=degrees(world.theta),
            pv=degrees(world.omega)
        )

    def _make_output(self):
        return dict(
            force=0.
        )

    def cp(self, x):
        left_far = 0
        left_near = 0
        stop = 0
        right_near = 0
        right_far = 0

        if x == -10.0:
            left_far = 1
        elif x >= -10.0 and x <= -5.0:
            left_far = ((-0.2)*x) - 1
        elif x < -10.0:
            left_far = 1

        if x >= -10 and x <= -2.5:
            left_near = ((1/(7.5)) * x) + (10/(7.5))
        elif x >= -2.5 and x <= 0:
            left_near = -0.4 * x

        if x >= -2.5 and x <= 0:
            stop = 0.4 * x + 1
        elif x >= 0 and x <= 2.5:
            stop = -0.4 * x + 1

        if x >= 0 and x <= 2.5:
            right_near = 0.4 * x
        elif x >= 2.5 and x <= 10:
            right_near = -1/(7.5) * x + (10/(7.5))

        if x >= 5 and x <= 10:
            right_far = 0.2 * x - 1
        elif x == 10:
            right_far = 1
        elif x > 10:
            right_far = 1

        return dict(left_far=left_far,
                    left_near=left_near,
                    stop=stop,
                    right_near=right_near,
                    right_far=right_far)

    def cv(self, cv):
        left_fast = 0
        left_slow = 0
        stop = 0
        right_slow = 0
        right_fast = 0

        if cv == -5:
            left_fast = 1
        elif cv >= -5 and cv <= -2.5:
            left_fast = -0.4 * cv - 1
        elif cv < -5:
            left_fast = 1

        if cv >= -5 and cv <= -1:
            left_slow = 0.25 * cv + 1.25
        elif cv >= -1 and cv <= 0:
            left_slow = -cv

        if cv >= -1 and cv <= 0:
            stop = cv + 1
        elif cv >= 0 and cv <= 1:
            stop = -cv + 1

        if cv >= 0 and cv <= 1:
            right_slow = cv
        elif cv >= 1 and cv <= 5:
            right_slow = -0.25 * cv + 1.25

        if cv >= 2.5 and cv <= 5:
            right_fast = 0.4 * cv - 1
        elif cv == 5:
            right_fast = 1
        elif cv > 5:
            right_fast = 1

        return dict(left_fast=left_fast,
                    left_slow=left_slow,
                    stop=stop,
                    right_slow=right_slow,
                    right_fast=right_fast)

    def pa(self, x):
        up_more_right = 0
        up_right = 0
        up = 0
        up_left = 0
        up_more_left = 0
        down_more_left = 0
        down_left = 0
        down = 0
        down_right = 0
        down_more_right = 0

        if x >= 0.0 and x <= 30.0:
            up_more_right = (1/30)*x

        if x >= 30.0 and x <= 60.0:
            up_more_right = ((-1)*(1/30)*x)+2
            up_right = ((1/30)*x)-1

        if x >= 60.0 and x <= 90.0:
            up_right = ((-1)*(1/30)*x)+3
            up = ((1/30)*x)-2

        if x >= 90.0 and x <= 120.0:
            up = ((-1)*(1/30)*x)+4
            up_left = ((1/30)*x)-3

        if x >= 120.0 and x <= 150.0:
            up_left = ((-1)*(1/30)*x)+5
            up_more_left = ((1/30)*x)-4

        if x >= 150.0 and x <= 180.0:
            up_more_left = ((-1)*(1/30)*x)+6

        if x >= 180.0 and x <= 210.0:
            down_more_left = ((1/30)*x)-6

        if x >= 210.0 and x <= 240.0:
            down_more_left = ((-1)*(1/30)*x)+8
            down_left = ((1/30)*x)-7

        if x >= 240.0 and x <= 270.0:
            down_left = ((-1)*(1/30)*x)+9
            down = ((1/30)*x)-8

        if x >= 270.0 and x <= 300.0:
            down = ((-1)*(1/30)*x)+10
            down_right = ((1/30)*x)-9

        if x >= 300.0 and x <= 330.0:
            down_right = ((-1)*(1/30)*x)+11
            down_more_right = ((1/30)*x)-10

        if x >= 330.0 and x <= 360.0:
            down_more_right = ((-1)*(1/30)*x)+12

        return dict(up_more_right=up_more_right,
                    up_right=up_right,
                    up=up,
                    up_left=up_left,
                    up_more_left=up_more_left,
                    down_more_left=down_more_left,
                    down_left=down_left,
                    down=down,
                    down_right=down_right,
                    down_more_right=down_more_right)

    def pv(self, x):
        cw_fast = 0
        cw_slow = 0
        stop = 0
        ccw_slow = 0
        ccw_fast = 0

        if x == -200:
            cw_fast = 1
        elif x >= -200.0 and x <= -100.0:
            cw_fast = ((-0.01)*x)-1
        elif x < -200.0:
            cw_fast = 1

        if x >= -200.0 and x <= -100.0:
            cw_slow = ((0.01)*x)+2

        if x >= -100.0 and x <= 0.0:
            cw_slow = ((-0.01)*x)
            stop = ((0.01)*x)+1

        if x >= 0.0 and x <= 100.0:
            stop = ((-0.01)*x)+1
            ccw_slow = ((0.01)*x)

        if x >= 100.0 and x <= 200.0:
            ccw_slow = ((-0.01)*x)+2
            ccw_fast = ((0.01)*x)-1
        elif x == 200:
            ccw_fast = 1
        elif x > 200.0:
            ccw_fast = 1

        return dict(cw_fast=cw_fast,
                    cw_slow=cw_slow,
                    stop=stop,
                    ccw_slow=ccw_slow,
                    ccw_fast=ccw_fast)

    def force_calc(self, x):
        left_fast = 0
        left_slow = 0
        stop = 0
        right_slow = 0
        right_fast = 0

        if x >= -100.0 and x <= -80.0:
            left_fast = (0.05*x)+5

        if x >= -80.0 and x <= -60.0:
            left_fast = ((-0.05)*x)-3
            left_slow = ((0.05)*x)+4

        if x >= -60.0 and x <= 0.0:
            left_slow = ((-1/60)*x)
            stop = ((1/60)*x)+1

        if x >= 0.0 and x <= 60.0:
            stop = ((-1/60)*x)+1
            right_slow = ((1/60)*x)

        if x >= 60.0 and x <= 80.0:
            right_slow = ((-0.05)*x)+4
            right_fast = ((0.05)*x)-3

        if x >= 80.0 and x <= 100.0:
            right_fast = ((-0.05)*x)+5

        return dict(left_fast=left_fast,
                    left_slow=left_slow,
                    stop=stop,
                    right_slow=right_slow,
                    right_fast=right_fast)

    def inference(self, input):
        pa = self.pa(input['pa'])
        pv = self.pv(input['pv'])
        cv = self.cv(input['cv'])
        cp = self.cp(input['cp'])

        RULE0 = max(min(pa['up'], pv['stop']), min(
            pa['up_right'], pv['ccw_slow']), min(pa['up_left'], pv['cw_slow']))
        RULE1 = min((pa['up_more_right']), (pv['ccw_slow']))
        RULE2 = min((pa['up_more_right']), (pv['cw_slow']))
        RULE3 = min((pa['up_more_left']), (pv['cw_slow']))
        RULE4 = min((pa['up_more_left']), (pv['ccw_slow']))
        RULE5 = min((pa['up_more_right']), (pv['ccw_fast']))
        RULE6 = min((pa['up_more_right']), (pv['cw_fast']))
        RULE7 = min((pa['up_more_left']), (pv['cw_fast']))
        RULE8 = min((pa['up_more_left']), (pv['ccw_fast']))
        RULE9 = min((pa['down_more_right']), (pv['ccw_slow']))
        RULE10 = min((pa['down_more_right']), (pv['cw_slow']))
        RULE11 = min((pa['down_more_left']), (pv['cw_slow']))
        RULE12 = min((pa['down_more_left']), (pv['ccw_slow']))
        RULE13 = min((pa['down_more_right']), (pv['ccw_fast']))
        RULE14 = min((pa['down_more_right']), (pv['cw_fast']))
        RULE15 = min((pa['down_more_left']), (pv['cw_fast']))
        RULE16 = min((pa['down_more_left']), (pv['ccw_fast']))
        RULE17 = min((pa['down_right']), (pv['ccw_slow']))
        RULE18 = min((pa['down_right']), (pv['cw_slow']))
        RULE19 = min((pa['down_left']), (pv['cw_slow']), cv['right_slow'])
        RULE20 = min((pa['down_left']), (pv['ccw_slow']))
        RULE21 = min((pa['down_right']), (pv['ccw_fast']))
        RULE22 = min((pa['down_right']), (pv['cw_fast']))
        RULE23 = min((pa['down_left']), (pv['cw_fast']))
        RULE24 = min((pa['down_left']), (pv['ccw_fast']))
        RULE25 = min((pa['up_right']), (pv['ccw_slow']))
        RULE26 = min((pa['up_right']), (pv['cw_slow']))
        RULE27 = min((pa['up_right']), (pv['stop']))
        RULE28 = min((pa['up_left']), (pv['cw_slow']))
        RULE29 = min((pa['up_left']), (pv['ccw_slow']))
        RULE30 = min((pa['up_left']), (pv['stop']))
        RULE31 = min((pa['up_right']), (pv['ccw_fast']))
        RULE32 = min((pa['up_right']), (pv['cw_fast']))
        RULE33 = min((pa['up_left']), (pv['cw_fast']))
        RULE34 = min((pa['up_left']), (pv['ccw_fast']))
        RULE35 = min((pa['down']), (pv['stop']), cv['right_fast'])
        RULE36 = min((pa['down']), (pv['cw_fast']))
        RULE37 = min((pa['down']), (pv['ccw_fast']))
        RULE38 = min((pa['up']), (pv['ccw_slow']))
        RULE39 = min((pa['up']), (pv['ccw_fast']))
        RULE40 = min((pa['up']), (pv['cw_slow']))
        RULE41 = min((pa['up']), (pv['cw_fast']))
        RULE42 = min((pa['up']), (pv['stop']))
    

        return dict(RULE0=RULE0, RULE1=RULE1, RULE2=RULE2, RULE3=RULE3, RULE4=RULE4, RULE5=RULE5, RULE6=RULE6,
                    RULE7=RULE7, RULE8=RULE8, RULE9=RULE9, RULE10=RULE10, RULE11=RULE11, RULE12=RULE12, RULE13=RULE13,
                    RULE14=RULE14, RULE15=RULE15, RULE16=RULE16, RULE17=RULE17, RULE18=RULE18, RULE19=RULE19,
                    RULE20=RULE20, RULE21=RULE21, RULE22=RULE22, RULE23=RULE23, RULE24=RULE24, RULE25=RULE25,
                    RULE26=RULE26, RULE27=RULE27, RULE28=RULE28, RULE29=RULE29,
                    RULE30=RULE30, RULE31=RULE31, RULE32=RULE32, RULE33=RULE33, RULE34=RULE34, RULE35=RULE35,
                    RULE36=RULE36, RULE37=RULE37, RULE38=RULE38, RULE39=RULE39, RULE40=RULE40, RULE41=RULE41, RULE42=RULE42)

    def defuzzification(self, input):
        sum1 = 0.0
        sum2 = 0.0
        left_fast = 0.0
        left_slow = 0.0
        stop = 0.0
        right_slow = 0.0
        right_fast = 0.0

        rules = self.inference(input)
        # print(rules)

        left_fast = max(rules['RULE3'], rules['RULE4'], rules['RULE8'],
                        rules['RULE11'], rules['RULE19'], rules['RULE20'],
                        rules['RULE29'], rules['RULE30'], rules['RULE31'],
                        rules['RULE34'], rules['RULE39'])

        left_slow = max(rules['RULE5'], rules['RULE24'],
                        rules['RULE28'], rules['RULE38'])

        stop = max(rules['RULE0'], rules['RULE10'], rules['RULE12'], rules['RULE13'], rules['RULE14'], rules['RULE15'],
                   rules['RULE16'], rules['RULE21'], rules['RULE23'], rules['RULE36'], rules['RULE37'], rules['RULE42'])

        right_slow = max(rules['RULE7'], rules['RULE22'],
                         rules['RULE25'], rules['RULE40'])

        right_fast = max(rules['RULE1'], rules['RULE2'], rules['RULE6'], rules['RULE9'],
                         rules['RULE17'], rules['RULE18'], rules['RULE26'], rules['RULE27'],
                         rules['RULE32'], rules['RULE33'], rules['RULE35'], rules['RULE41'])

        # print(left_fast,left_slow,stop,right_slow,right_fast)

        points = np.linspace(-100, 100, 1000)
        dx = points[1] - points[0]
        for point in points:
            force_calc_output = self.force_calc(point)

            if force_calc_output['left_fast'] >= left_fast:
                force_calc_output['left_fast'] = left_fast

            if force_calc_output['left_slow'] >= left_slow:
                force_calc_output['left_slow'] = left_slow

            if force_calc_output['stop'] >= stop:
                force_calc_output['stop'] = stop

            if force_calc_output['right_slow'] >= right_slow:
                force_calc_output['right_slow'] = right_slow

            if force_calc_output['right_fast'] >= right_fast:
                force_calc_output['right_fast'] = right_fast

            sum1 += max(force_calc_output.values()) * point * dx
            sum2 += max(force_calc_output.values()) * dx

        if sum2 != 0.0:
            output_force = sum1/sum2
        else:
            output_force = 0
        return output_force

    def decide(self, world):
        input = self._make_input(world)
        output = self.defuzzification(input)
        return output
