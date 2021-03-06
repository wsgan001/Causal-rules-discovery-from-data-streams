import SequenceGenerator as sg
import matplotlib.pyplot as plt
import numpy
import math
import ast

with open('config') as f:
    lines = f.readlines()

config_list = []
for line in lines:
    line = line.replace(" ", "").replace("\n", "")
    config = {}
    for elem in line.split(';'):
        elem = elem.split('=')
        config[elem[0]] = elem[1]
    config_list.append(config)

grouped_config_list = []
for config in config_list:
    key = config['attr'].replace("'","")
    if not any(key in d['attr_name'] for d in grouped_config_list):
        attr_dict = {}
        values_list = []
        values_list.append(config)
        attr_dict['attr_name'] = key
        attr_dict['value'] = values_list
        grouped_config_list.append(attr_dict)
    else:
        attr_dict = [d for d in grouped_config_list if d['attr_name'] == key][0]
        attr_dict['value'].append(config)

for conf in grouped_config_list:
    for key, value in conf.items():
        print key,": ", value if key == 'attr_name' else ' '
        if key != 'attr_name':
            for v in value:
                print "\t", v
    print

curr_state = max([abs(int(float(config_list[i]['from']))) for i in range(len(config_list)) if 'from' in config_list[i]])*2
last_state = curr_state + curr_state/2
seqs = []
k = len(grouped_config_list)
f, axarr = plt.subplots(k)
j = 0
for config in grouped_config_list:
    config_values = config['value']
    init_value = ast.literal_eval(config_values[0]['domain'])[0]
    seq = [init_value for k in range(0, last_state)]
    domain = ast.literal_eval(config_values[0]['domain'])
    operator = 'eq'
    for z in range(0,len(config_values)):
        value = ast.literal_eval(config_values[z]['value'])
        probability = float(config_values[z]['probability'])
        fr = curr_state - curr_state
        to = curr_state - last_state
        if 'from' in config_values[z]:
            fr = abs(int(float(config_values[z]['from'])))
            if config_values[z]['to'] != '0':
                to = abs(int(float(config_values[z]['to'])))

        seq = sg.generateSequence(seq, domain, value, operator, probability, curr_state-fr, curr_state-to)
        sg.plotSequence(axarr[j], seq, domain, config['attr_name'], curr_state)
    j += 1
    seqs.append(seq)

plt.show()

#sg.saveToCsv(li, seqs)
