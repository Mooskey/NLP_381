import DocumentClass
###PRE-PROCESSING###
brown_train = DocumentClass.Document(open('brown-train.txt', 'r').read())
brown_test = DocumentClass.Document(open('brown-test.txt', 'r').read())
learner_test = DocumentClass.Document(open('learner-test.txt', 'r').read())

brown_train_unkowned = brown_train.unknownify()


#unigram_mle = brown_train_unkowned.generateUnigramMLE()
#bigram_mle = brown_train_unkowned.generateBigramMLE()
#bigram_smooth = brown_train_unkowned.generateBigramSmoothed()


###POST-PROCESSING###

#Question 1

print('How many word types (unique words) are there in the training corpus? Please include the padding symbols and the unknown token.')

word_types = len(brown_train_unkowned.token_counts.keys())

print(word_types)

#Question 2

print('\nHow many word tokens are there in the training corpus?')

print(brown_train_unkowned.total_token_count)

#Question 3
print('\nWhat percentage of word tokens and word types in each of the test corpora did not occur in training?')

brown_test_word_types = set(brown_test.token_counts.keys())
learner_test_word_types = set(learner_test.token_counts.keys())
brown_train_word_types = set(brown_train.token_counts.keys())


brown_test_distinct_words = brown_test_word_types - brown_train_word_types
learner_test_distinct_words = learner_test_word_types - brown_train_word_types

percent_brown = str(round(100*len(brown_test_distinct_words)/len(brown_test_word_types), 2))
percent_learner = str(round(100*len(learner_test_distinct_words)/len(learner_test_word_types), 2))


print('percent of unique brown test words: ' + percent_brown )
print('percent of unique learner test words: ' + percent_learner )
