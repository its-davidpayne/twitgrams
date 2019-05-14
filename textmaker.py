import random

N = 3 # as in n-grams

textfile = input("What textfile to use?: ")

with open(f"data/{textfile}.txt") as reader:
    sentence_list = [sent.rstrip() for sent in reader]

list_of_lists = [sentence.split(" ") for sentence in sentence_list]

starting_words = [sentence[0] for sentence in list_of_lists]

ngram_dict = {}

for sentence in list_of_lists:
    for index in range(len(sentence)):
        if sentence[index] in ngram_dict:
            try:
                ngram_dict[sentence[index]].append([sentence[index + 1], sentence[index + 2]])
            except IndexError:
                try:
                    ngram_dict[sentence[index]].append([sentence[index + 1]])
                except IndexError:
                    pass
        else:
            try:
                ngram_dict[sentence[index]] = ([[sentence[index + 1], sentence[index + 2]]])
            except IndexError:
                try:
                    ngram_dict[sentence[index]] = [sentence[index + 1]]
                except IndexError:
                    pass

new_sentence = []

new_sentence.append(random.choice(starting_words))

while new_sentence[-1][-1][-1] not in ['.','?','!']:
    for element in random.choice(ngram_dict[new_sentence[-1]]):
        new_sentence.append(element)

output = ' '.join(new_sentence)

print(output)