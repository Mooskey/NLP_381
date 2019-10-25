import sys, os, math, glob

data_path = sys.argv[1]


model = glob.glob(data_path + '/*.NB')[0]
test_data = glob.glob(data_path + '/test/*.NB')[0]

output = open(data_path + '/output.txt', 'w')
output_text = 'Class Prediction\n----- ----------\n'

model = open(model,'r').read()
test_data = open(test_data,'r').read()

model = model.split('\n')

if '' in model:
    del model[model.index('')]
for i in range(2):
    model[i] = model[i].split(' ')
    if '' in model[i]:
        del model[i][model[i].index('')]

test_data = test_data.split('\n')
if '' in test_data:
    del test_data[test_data.index('')]
for i in range(len(test_data)):
    test_data[i] = test_data[i].split(' ')
    if '' in test_data[i]:
        del test_data[i][test_data[i].index('')]


if 'mini' in data_path:
    output_text = ''
    test_data = test_data[0]
    test_data = [int(x) for x in test_data]
    if model[0][0] == 'action':
        action = model[0][1:]
        comedy = model[1][1:]
    else:
        comedy = model[0][1:]
        action = model[1][1:]

    action = [int(x) for x in action]
    comedy = [int(x) for x in comedy]
    
    sum_act = sum(action)
    sum_com = sum(comedy)
    
    action = [x/sum_act for x in action]
    comedy = [x/sum_com for x in comedy]

    action_result = math.log2(3/5)
    comedy_result = math.log2(2/5)
    
    for i in range(len(action)):
        action_result += math.log2(action[i]**test_data[i])
        comedy_result += math.log2(comedy[i]**test_data[i])
    if(action_result > comedy_result):
        output_text += 'Prediction: action\n'
    else:
        output_text += 'Prediction: comedy\n'
    output_text += 'Log Probability of comedy' + str(comedy_result) + '\n'
    output_text += 'Log Probability of action:' + str(action_result)
    output.write(output_text)

else:
    if model[0][0] == 'pos':
        pos = model[0][1:]
        neg = model[1][1:]
    else:
        neg = model[0][1:]
        pos = model[1][1:]
    
    pos = [int(x) for x in pos]
    neg = [int(x) for x in neg]

    sum_pos = sum(pos)
    sum_neg = sum(neg)

    pos = [x/sum_pos for x in pos]
    neg = [x/sum_neg for x in neg]

    correct_count = 0
    all_count = 0
    vec_size = len(pos)
    
    for x in test_data:
        all_count+=1
        tag = x[0]
        test = x[1:]
        test = [int(y) for y in test]
        log_sum_pos = math.log2(1/2)
        log_sum_neg = math.log2(1/2)
    
        for i in range(vec_size):
            log_sum_pos += math.log2(pos[i])*test[i]
            log_sum_neg += math.log2(neg[i])*test[i]
        if log_sum_neg > log_sum_pos:
            answer = 'neg'
        else:
            answer = 'pos'
        if answer == tag:
            correct_count += 1
        output_text += tag + '   '+ answer + '\n'
    
    output.write(output_text + 'Accuracy: ' + str(correct_count/all_count*100) + '%')

