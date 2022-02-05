#!python3

TYPES_VIDMINKY = [
    'v_rod', # відмінки
    'v_dav', # відмінки
    'v_mis', # відмінки
    'v_oru', # відмінки
    'v_kly', # відмінки
    'v_zna', # відмінки
]

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
]

STOP_TYPES_RAND = [
    'coll',  # розмовна
    'rare',  # рідковживані
    'slang', # сленгові
    'alt',   # альтернативні написання
    'advp',  # дієприслівники
]

STOP_SYMBOLS = [
    '-', '\'', '.'
]

class Settings:
    def __init__(self):
        self.wlen = 5
        self.file = 'kobza_filtered_dict'
        self.only_type = None
        self.stop_symbols = STOP_SYMBOLS
        self.stop_types = STOP_TYPES
        self.skip_case = True
        self.skip_adj_t = False

    def dict_file_path(self):
        return 'out/{}.txt'.format(self.file)

    def words_file_path(self):
        return 'out/{}_words.txt'.format(self.file)

def check_word(word, wtype, settings=Settings()):
    if wlen != settings.wlen:
        return False
    for symb in settings.stop_symbols:
        if symb in word:
            return False
    if settings.skip_case and word.lower() != word:
        return False
    wtypes = wtype.split(':')
    # print(wtypes)
    if settings.only_type:
        if not settings.only_type in wtypes:
            return False
    for stype in settings.stop_types:
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
    if settings.skip_adj_t:
        if 'adj' in wtypes:
            if 'p' in wtypes or 'f' in wtypes or 'n' in wtypes:
                return False
    return True

BASE_SETTINGS = Settings()

RANDOM_SETTINGS = Settings()
RANDOM_SETTINGS.file = 'kobza_filtered_random'
RANDOM_SETTINGS.stop_types = STOP_TYPES + STOP_TYPES_RAND
RANDOM_SETTINGS.skip_adj_t = True

ONLY_GEO = Settings()
ONLY_GEO.file = 'kobza_only_geo'
ONLY_GEO.skip_case = False
ONLY_GEO.only_type = 'geo'
ONLY_GEO.stop_types = TYPES_VIDMINKY

ONLY_FNAME = Settings()
ONLY_FNAME.file = 'kobza_only_fname'
ONLY_FNAME.skip_case = False
ONLY_FNAME.only_type = 'fname'
ONLY_FNAME.stop_types = TYPES_VIDMINKY

ONLY_PROP = Settings()
ONLY_PROP.file = 'kobza_only_prop'
ONLY_PROP.skip_case = False
ONLY_PROP.only_type = 'prop'
ONLY_PROP.stop_types = TYPES_VIDMINKY + [
    'geo', 'fname', 'lname'
]

settings = RANDOM_SETTINGS

# Using readlines()
file1 = open('dict_corp_lt.txt', 'r')
lines = file1.readlines()

GEN_SETTINGS = [BASE_SETTINGS, RANDOM_SETTINGS]

for settings in GEN_SETTINGS:
    outfile = open(settings.dict_file_path(), 'w')
    outwords = open(settings.words_file_path(), 'w')

    # Strips the newline character
    for line in lines:
        parts = line.split()
        word = parts[0]
        wtype = parts[2]
        wlen = len(word)
        if check_word(word, wtype, settings):
            # if parts[0] != parts[1]:
            #     print(' '.join(parts))
            outfile.write(line)
            outwords.write(word)
            outwords.write('\n')

    outfile.close()
    outwords.close()