import sys, os, re

data_path = sys.argv[1]



if 'mini' not in data_path:
    train_test = [data_path + '/train/', data_path + '/test/']
    vocab_file = open(data_path + '/movie.vocab', 'w')
    test_param_file = open(data_path + '/test/test-movie-review.NB', 'w')
    param_file = open(data_path + '/movie-review.NB', 'w')

    vocab_text = ''
    regex = ' -|- |(?!-|\')\W|\'{2,}|-{2,}|br \/'

    for path in train_test:
        meta_pos = ''
        meta_neg = ''
        if 'train' in path:
            splitter = ' '
            print('Processing Train\n-----------------')

            for text in os.listdir(path + '/pos'):
                review = open(path + '/pos/' + text, 'r')
                temp = review.read()
                review.close()
                review = temp
                review = review.lower()
                review = re.sub(regex, ' ',review)
    
                meta_pos += review + splitter

            meta_pos = re.sub(' {2,}', ' ',meta_pos)
            meta_pos = re.sub(' \n', '\n',meta_pos)
            meta_pos = meta_pos[:-1]

            print('MetaDoc creation for Neg\n-----------------')
        
            for text in os.listdir(path + '/neg'):

                review = open(path + '/neg/' + text, 'r')
                temp = review.read()
                review.close()
                review = temp
                review = review.lower()
                review = re.sub(regex, ' ',review)

                meta_neg += review + splitter
            meta_neg = re.sub(' {2,}', ' ',meta_neg)
            meta_neg = re.sub(' \n', '\n',meta_neg)
            meta_neg = meta_neg[:-1]

        else:
            print('Processing Test\n-----------------')
        
            print('Parameter creation for Pos\n-----------------')
            test_param_text = ''
            param_start = {word:0 for word in vocab_text}
            counter = 0
            percent_counter = 0

            for text in os.listdir(path + '/pos'):
                review = open(path + '/pos/' + text, 'r')
                temp = review.read()
                review.close()
                review = temp
                
                review = review.lower()
                review = re.sub(regex, ' ',review)
 
                counter += 1
                test_param_text += 'pos '
                pos_counts = dict(param_start)
                x = review.split(' ')
                for word in x:
                    if word in vocab:
                        pos_counts[word] += 1
                for word in vocab_text:
                    test_param_text += str(pos_counts[word]) + ' '
                test_param_text = test_param_text[:-1] + '\n'
                if percent_counter != (counter/12500*100)//1:
                    percent_counter = counter/12500*100//1
                    sys.stdout.flush()
                    sys.stdout.write(str(percent_counter))
    #


                ##
            print('Parameter creation for Neg\n-----------------')
            
            for text in os.listdir(path + '/neg'):

                review = open(path + '/neg/' + text, 'r')
                temp = review.read()
                review.close()
                review = temp
                review = review.lower()
                review = re.sub(regex, ' ',review)

  
                test_param_text += 'neg '
                neg_counts = dict(param_start)
                x = review.split(' ')
                for word in x:                    
                    if word in vocab:
                        neg_counts[word] += 1

                for word in vocab_text:
                    test_param_text += str(neg_counts[word]) + ' '
                test_param_text = test_param_text[:-1] + '\n'

            test_param_file.write(test_param_text[:-1])


    
        if 'train' in path:
            print('Vocab Creation\n-----------------')

            vocab = set(meta_pos.split(' ')).union(set(meta_neg.split(' ')))
            for word in vocab:
                vocab_text += word + '\n'
            vocab_text = vocab_text[:-1]
            vocab_file.write(vocab_text)
            vocab_text = vocab_text.split('\n')

            pos_counts = {word:1 for word in vocab_text}
            neg_counts = {word:1 for word in vocab_text}
            
            print('Parameter creation\n-----------------')

            for word in meta_pos.split(' '):
                pos_counts[word] += 1


            for word in meta_neg.split(' '):
                neg_counts[word] += 1
        
            pos_params = 'pos '
            neg_params = 'neg '

            for word in vocab_text:
                pos_params += str(pos_counts[word]) + ' '
                neg_params += str(neg_counts[word]) + ' '
            pos_params = pos_params[:-1]
            neg_params = neg_params[:-1]
            param_file.write(pos_params + '\n' + neg_params)
    

    
else:
    action_path = data_path + '/train/action'
    comedy_path = data_path + '/train/comedy'


    x = open(data_path + '/movie-review-small.NB','w')
    y = open(data_path + '/mini.vocab','r')
    temp = y.read()
    y.close()
    y = temp
    y = y.split('\n')
    del y[y.index('')]



    action_revs = os.listdir(action_path)
    comedy_revs = os.listdir(comedy_path)

    meta_action = ''
    meta_comedy = ''

    print(set(y))
    for review in action_revs:
        text = open(action_path + '/' + review)
        temp = text.read()
        text.close()
        text = temp.replace(',','')
        print(text)
        meta_action = meta_action + text + '\n'

    for review in comedy_revs:
        text = open(comedy_path + '/' + review)
        temp = text.read()
        text.close()
        text = temp.replace(',','')

        meta_comedy = meta_comedy + text + '\n'

    action_p = []
    comedy_p = [] 
    for word in y:
        action_p.append(meta_action.count(word)+1)
        comedy_p.append(meta_comedy.count(word)+1)

    x.write('action ')
    for i in action_p:
        x.write(str(i) + ' ')
    x.write('\ncomedy ')
    for i in comedy_p:
        x.write(str(i) + ' ')


