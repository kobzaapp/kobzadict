# Using readlines()
file1 = open('dict_corp_lt.txt', 'r')
lines = file1.readlines()

outfile = open('out/kobza_filtered_dict.txt', 'w')
outwords = open('out/kobza_filtered_dict_words.txt', 'w')
count = 0
COUNT_LIMIT = 100000

STOP_TYPES = [
    'fname', # імена
    'lname', # прізвища
    'geo',   # топоніми
    'prop',  # власна назва
    'v_rod', # відмінки
    'v_dav', # відмінки
    'v_mis', # відмінки
    'v_oru', # відмінки
    'v_kly', # відмінки
    'v_zna', # відмінки
    'intj',  # вигуки
    'vulg',  # вульгарні слова
    'abbr',  # аббревіатури
    'bad',   # покручі
    'arch',  # архаїзми
    'coll',  # розмовна
    'rare',  # рідковживані
    'slang', # сленгові
    'alt',   # альтернативні написання
    'advp',  # дієприкметники
]

STOP_SYMBOLS = [
    '-', '\'', '.'
]

def check_word(word, wtype):
    if wlen != 5:
        return False
    for symb in STOP_SYMBOLS:
        if symb in word:
            return False
    if word.lower() != word:
        return False
    wtypes = wtype.split(':')
    # print(wtypes)
    for stype in STOP_TYPES:
        if stype in wtypes:
            return False
    # Тільки дієслова в інфінитиві і нескороченої форми
    if 'verb' in wtypes:
        if 'short' in wtypes:
            return False
        if not 'inf' in wtypes:
            return False
    # Іменники в множині, які мають тільки множину
    if 'noun' in wtypes and 'p' in wtypes:
        if not 'ns' in wtypes:
            return False
    if 'adj' in wtypes:
        if 'p' in wtypes or 'f' in wtypes or 'n' in wtypes:
            return False
    # if 'advp' in wtypes:
    #     return True
    # else:
    #     return False
    return True

# Strips the newline character
for line in lines:
    parts = line.split()
    word = parts[0]
    wtype = parts[2]
    wlen = len(word)
    if check_word(word, wtype):
        if parts[0] != parts[1]:
            print(' '.join(parts))
        count = count + 1
        if count < COUNT_LIMIT:
            outfile.write(line)
            outwords.write(word)
            outwords.write('\n')
        else:
            break

outfile.close()