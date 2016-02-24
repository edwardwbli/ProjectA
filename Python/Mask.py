def censor(text, word):
    result_text = []
    length_word = len(word)
    mask = "*" * length_word
    for text_word in text.split():
        if text_word == word:
            result_text.append(mask)  
        else:
            result_text.append(text_word)
    print  " ".join(result_text)
    return " ".join(result_text)

text_string = raw_input("Your text: ")
word_string = raw_input("What to mask: ")

censor(text_string, word_string)



