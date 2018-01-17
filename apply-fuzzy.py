
# dataset
arry_knee = [17.59927927,
17.28945179,
16.06049261,
14.4246481,
12.86550177,
11.86275768,
11.38867977,
10.68479908,
9.860243158,
10.41414899,
12.06726068,
15.19136752,
19.46519725,
23.93329121,
31.6320875,
42.17484563,
54.28323049,
61.6580829,
66.74923493,
65.02005142,
63.45315594,
60.32059381,
52.38898301,
45.10838471,
32.49755674,
19.22664054,
6.563132726,
3.669921835,
5.664933259,
]

arry_hip = [23.51402995,
24.32733697,
23.56235516,
22.39970365,
21.36611784,
19.14694349,
16.61982282,
14.1345282,
11.38213722,
8.070294415,
4.598295522,
2.025380196,
-1.082530365,
-4.121750065,
-7.022422597,
-9.677217496,
-11.79508167,
-13.03236501,
-14.02500795,
-14.14641925,
-13.49120222,
-10.05022507,
-4.511631299,
1.010036959,
6.118671359,
9.774170324,
14.02561353,
17.77709689,
20.34311095,
21.66003804,
21.8540178,
20.74251056,
18.78441528,
17.69198145,
16.81396641]

import numpy as np
import skfuzzy.control as ctrl
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import os


hip = ctrl.Antecedent(np.arange(-30, 30, 1), 'hip')
knee = ctrl.Antecedent(np.arange(0, 100, 1), 'knee')
time = ctrl.Antecedent(np.arange(0, 100, 1), 'time')
stage = ctrl.Antecedent(np.arange(0, 100, 1), 'stage')
phase = ctrl.Consequent(np.arange(0, 100, 1), 'phase')


hip['extension'] = fuzz.trimf(hip.universe, [-30, -30, 0])
hip['low'] = fuzz.trimf(hip.universe, [0, 0, 15])
hip['high'] = fuzz.trimf(hip.universe, [0, 15, 30])

knee['low'] = fuzz.trimf(knee.universe, [0, 0, 20])
knee['medium'] = fuzz.trimf(knee.universe, [0, 20, 40])
knee['high'] = fuzz.trimf(knee.universe, [20, 40, 70])

time['low'] = fuzz.trimf(time.universe, [0, 0, 25])
time['medium'] = fuzz.trimf(time.universe, [0, 25, 75])
time['high'] = fuzz.trimf(time.universe, [25, 75, 100])


stage['SLR'] = fuzz.trimf(stage.universe, [0, 0, 10])
stage['SMS'] = fuzz.trimf(stage.universe, [0, 10, 40])
stage['SSS'] = fuzz.trimf(stage.universe, [10, 40, 100])

phase['Loading_response'] = fuzz.trimf(phase.universe, [0, 0, 10])
phase['Mid_stance'] = fuzz.trimf(phase.universe, [0, 10, 30])
phase['Terminal_stance'] = fuzz.trimf(phase.universe, [10, 30, 50])
phase['Preswing'] = fuzz.trimf(phase.universe, [30, 50, 60])
phase['Initial_swing'] = fuzz.trimf(phase.universe, [50, 60, 73])
phase['Mid_swing'] = fuzz.trimf(phase.universe, [60, 73, 87])
phase['Terminal_swing'] = fuzz.trimf(phase.universe, [73, 87, 100])


hip.view()
knee.view()
time.view()
stage.view()


rule1 = ctrl.Rule(hip['high'] | knee['low'] | time['low'] | stage['SLR'] , phase['Loading_response'])
rule2 = ctrl.Rule(knee['low'] | time['low'] | stage['SMS'] , phase['Mid_stance'])
rule3 = ctrl.Rule(hip['low'] | knee['low'] | time['low'] | stage['SMS'] , phase['Mid_stance'])
rule4 = ctrl.Rule(hip['extension'] | knee['medium'] | time['medium'] | stage['SSS'] , phase['Terminal_stance'])
rule5 = ctrl.Rule(hip['extension'] | ~knee['low'] | time['medium'] | stage['SSS'] , phase['Preswing'])
rule6 = ctrl.Rule(hip['low'] | ~knee['low'] | time['medium'] | stage['SSS'] , phase['Initial_swing'])
rule7 = ctrl.Rule(hip['high'] | knee['high'] | time['high'] | stage['SSS'] , phase['Mid_swing'])
rule8 = ctrl.Rule(hip['high'] | knee['low'] | time['high'] | stage['SSS'] , phase['Terminal_swing'])

gait_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])
gait_ctrl.view()
gaiting = ctrl.ControlSystemSimulation(gait_ctrl)

#hip input
# for h in arry_hip:
#     print h

# for k in arry_knee:
#     print k


gaiting.input['hip'] = 20
gaiting.input['knee'] = 13
gaiting.input['time'] = 10
gaiting.input['stage'] = 10

gaiting.compute()

print gaiting.output

gaiting.print_state()


raw_input("Press Enter to continue ...")