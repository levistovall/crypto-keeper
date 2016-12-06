# BASIC CRYPTANALYSIS
#
# The prompt for the problem was to use a text file as the source of valid words,
# read in a string of words assumed to be enciphered using a monoalphabetic cipher,
# and output a the same string, deciphered.

# A monoalphabetic cipher is one that maps each letter in the alphabet to itself or another letter in the alphabet

# this function creates a set of the words that occur in
# the file, changed to lower case
def get_word_set_from_file(file):
    in_file = open(file, 'r')
    return set(word.strip().lower() for word in in_file)

# this function takes a string as input and returns two values:
#   the first is the set of all words which occur in the string
#   the second is the set of all letters which occur in the string
def get_words_and_letters_in_string(st):
    st = st.split(" ")

    word_set = set(word.strip().lower() for word in st)
    letter_set = set(letter for word in word_set for letter in word)

    return word_set, letter_set

# this function takes a string as input and returns a list
# representing what I refer to as its pattern, which
# is constructed as follows:
#   each character, in order, is assigned an integer which increments as
#   new characters appear and is placed in the list at the corresponding
#   index, and characters which have already occurred once are assigned
#   the same integer as the first occurence
# EXAMPLE: get_pattern("cowboys") returns [0, 1, 2, 3, 1, 4, 5]
def get_pattern(st):
    ch_dict = {}
    ch_code = 0
    pattern = []
    for ch in st:
        if ch in ch_dict:
            pattern.append(ch_dict[ch])
        else:
            ch_code += 1
            pattern.append(ch_code)
            ch_dict[ch] = ch_code

    return pattern

# checks that two strings have the same "pattern" as described above
#   EXAMPLE: same_pattern("cowboys", "skulker") returns True
def same_pattern(st1, st2):
    return get_pattern(st1) == (get_pattern(st2))

# this function takes a string, st and a set of strings, s as input and returns
# a list of all strings in s whose patterns match that of st
def get_pattern_matches_from_set(st, s):
    return [word for word in s if same_pattern(st, word)]

# this function is used to construct as much of the substitution alphabet as
# possible by using only those encoded strings which have only one pattern match
# in the set of possible words(certainties)
# it takes as input
#   a set of the enciphered words from which to glean a substitution alphabet
#   a set of all strings(from dictionary.lst) which will be considered valid deciphered words,
#   and the set of letters which occur in the enciphered words
# it returns
#   a dictionary representing as complete an alphabet as possible without trying every combination of keys and values
#   the list of letter keys remaining to be assigned values in the dict
#   the list of letter values left which could possibly be assigned to a key in the dict
def exhaust_certainties(enciphered, s, ls):
    certainties = {word:get_pattern_matches_from_set(word, s)[0] for word in enciphered if len(get_pattern_matches_from_set(word, s)) == 1}
    alphabet = {}

    keys_remaining = [letter for letter in ls]
    vals_remaining = [chr(i) for i in range(ord("a"), ord("z")+1)]

    for key in certainties:
        for j in range(len(key)):
            if key[j] in alphabet:
                if alphabet[key[j]] != certainties[key][j]:
                    print("THINGS ARE LESS CERTAIN THAN THEY SEEMED")
                    return
            else:
                alphabet[key[j]] = certainties[key][j]
                keys_remaining.remove(key[j])
                vals_remaining.remove(certainties[key][j])
    return alphabet, keys_remaining, vals_remaining

# this function takes a string and a dictionary representing a substitution alphabet,
# and uses the dictionary to decipher the string a character at a time
# returns the deciphered string with asterisks in place of anything that went
# unaccounted for
def monoalphabetic_decipher(st, a):
    new_st = ""
    for ch in st:
        if ch == " ":
            new_st += " "
        else:
            if ch in a:
                new_st += a[ch]
            else:
                new_st += "*"
    return new_st

# this function takes two lists, and returns a list of all
# possible dictionaries that use the elements of the first list
# as keys and those of the second as values
def get_all_key_value_combos(keys, values):
    dict_list = []
    if len(keys) == 0:
        return {}
    elif len(keys) == 1:
        return [{keys[0]:v} for v in values]

    else:
        for i in range(len(values)):
            d = {keys[0]:values[i]}
            new_values = values[:]
            del new_values[i]

            minus_one = get_all_key_value_combos(keys[1:], new_values)
            for j in range(len(minus_one)):
                c = d.copy()
                c.update(minus_one[j])
                dict_list.append(c)

        return dict_list

# this function continues the work of exhaust_certainties by taking as input
#   -the set of enciphered words from which to glean a substitution alphabet
#   -the set of all valid words from dictionary.lst
#   -the previously established portion of the alphabet
#   -the list of remaining key-letters
#   -the list of remaining possible value-letters
# and using get_all_key_value_combos on the remaining keys and values to get a list of
# finishing pieces to try with the established alphabet, checking each one until one returns
# a valid word for every single string in the set of enciphered words, or until it finds that
# none can do so, in which case it returns the alphabet as it was before
def fill_in_alphabet_from_input(enciphered_set, word_set, alphabet, keys_remaining, vals_remaining):
    possible_solns = get_all_key_value_combos(keys_remaining, vals_remaining)
    verified = False
    for i in range(len(possible_solns)):
        b = alphabet.copy()
        b.update(possible_solns[i])
        verified = True
        for word in enciphered_set:
            if monoalphabetic_decipher(word, b) not in word_set:
                verified = False
                break
        if verified:
            return b
    if not verified:
        return alphabet


# The main function employs all functions defined above to print a deciphered version of your input.
# The analysis formed by the use of said functions only works for strings enciphered according to
# monoalphabetic substitution.
# Each comment below is an example input from hackerrank.com's basic cryptanalysis challenge

# lhpohes gvjhe ztytwojmmtel lgsfcgver segpsltjyl vftstelc djfl rml catrroel jscvjqjyfo mjlesl lcjmmfqe egvj gsfyhtyq sjfgver csfaotyq lfxtyq gjywplesl lxljm dxcel mpyctyq ztytwojmmtelel mfcgv spres mjm psgvty bfml ofle mjlc dtc tygfycfctjy dfsyl zpygvel csfao yealqsjpml atyl lgsjql qyfsotelc fseyf ojllel gjzmselltyq wpyhtelc zpltgl weygel afyher rstnesl aefleo rtyhes mvflel yphe rstnes qojder dtwwer lojml mfcgvel reocfl djzder djpygtyq gstmmoeafsel reg cpdel qspyqe mflctel csflvtyq vfcl avfghtyq vftsdfool mzer rsjye wjjol psol mplvtyq catrroe mvfqe lgseey leqzeycer wjseqsjpyrer lmjtoes msjwtoel docl djpyger cjpstlcl goefy gojddesl mjrl qjddoe gjy gpdtyql lyftotyq rjayojfr swgl vjle atrqec gjzmfgces frfl qotcgver gspzd zftodjzdl lyfsh

# xugsx qgxxgkv mzxzdugezvx svuaziqx jvvsx jgit sixhvt qgyed sqzuk dbbrzuv cvx bedlvu uvfxvx ygryirgade ydfjdw lvedx svvpx adiezxa jezaarv jglggex bzukvezuk egsvt kdshvex brgaavuzuk rdxzuk yhgzuzuk hgqqvevt qgeazgux srgwsvu ovrrdx tddexadsx tdfurdgtzuk gssx tdy qgzrjdqjvt px egmvx ugaiev kedp tdfu bddasezua afvgpx vcyr jdixaedshvtdu jill ahevgt keivx qgex kezutzuk yevvszuk sixh sibbvt sdpv sedkegq jzauvax tzupve adgt brgk yrdypx uvfjzvx vrvshguazuv vrmzxh yegxhvx svxxzqgrx tzuk jezaarve yegxhvt qvag uwvafdep vt bdepvt adkkrvt jvvs xvrmgkvx vezxvx xsrgax fgrtdx adkkrvx adgttvt rgiutedqga tvqdvt sdssvt bzcvx jglgge kugerzve fhgypvt jdekx xfzllrzuk xgra jdqjzuk xyevvux sedbzrv gyyiqirgadex ydqsdx ygux jgebx tdfux sibbzuk jgutfztahx pritkv

# btnpufhz esxfh vyhvefz ufhez xsgfnafcfz umabtfz qz kmhmgsjfg ghndf tiufhzumbfz ahneez ydsdafhfzasdw uhnanbne pmdwefz lmeeumufhz oymgz tnuz kmdz vncfz pmdwfgz dmsxf ltmbq wmz zdmsez zmiz pszkfmayhf aydf zyd zumdwef vvzfz wnvvefz khfflmhf tmpzafhz bndz sdksdsasfz mpnfvmz athmztfz tmppfh tfcfz bivfhuydq gnldfg ghsxfh pmdwefh zuskki zlmv zunnksdw gfmgfh ahsxsme dyqfg kemw pmhwsdme byvsdwfg enzfhz uzfygn bhsuueflmhf bmebyemanhz gnldsdw pydwz uyzt xmc uydafg zbhffd gsf enzfh difalnhq kenlbtmhaz venbqfg ayvf vmhkz zbmw jfhnfz ggfg kemxnh vhnqf vmhkfg kemxnhz pyaafhfg tmppfhsdw byvfz befmdfg hnvyzafh kenngsdw vhfmqz zunsefhz knzzsez bhmindz yhe ufzzspmefg bhfasdz hmdgnpdfzz bhfmasndszpz zsenz jnhbtsdw bnnqsf bendf oyfzfz meaz zpnqf zuffgnpfafh ztmhflmhf

# mrsjcm jm zsgfcpcd mrtgfkcm eqgcd arm mragfcm utem mkar chcujsgf vqtpecp dcucd eai ychcm mraak sgepam mxajcd paae yarrsgf xtgfkcp eaaksgf xtupakafscm ramem zkteecp xqeecpm btkdam uaxrpcmmcm lszzscm cuya dpsncp ksgem uagmcd am mbsooksgf mkqprsgf zktf osrrcd rmcqdam rpscmeyaad wctx myckk ksgqhcm upcesgm meqdkscp uytggckm eaqpsme pawqmecp rqzzcd uyqffsgf mrsjcd mrszzscme dpqx btkj zammskm ksncme ddcd oaxwscm eaffkc wtpg dpqxm msksuag bapxyakc jkqdfsgf mupaf gcbm xqgf epakkcd mraaksgf wkaujcd kamcpm zkteecme ptncd uiukc rsrcm ksnc fpqgfcm dtcxagm nth mrtxm uyqf zakkabqrm eycapscm ytspscme mqrrape fktmmcm psr tmussm dctdcme ztptdsoc rytfc wsem mgtpjm upsrrkcbtpc mrkte xaujsgfwspd ptgdaxm mktwm wpctjsgf zaakm uptiagm

# geyeno wshjemh hmtrmth enfpsjm hnmsymth qstgvetmg nedypm tkgmhj dzxmtwknyh xmsi ibnhjtbhejemh hwen hwbbp jbktehjed venneno mldp gmsgpbdyh hpeih tewbff nmtg hdtboomg tmwpedsjbth tsngbinmhhmh fbbjwtenj sgsh hktfeno ftzeno tbsdqeno xstnmz kwweno fknyemt gem dqsenmg hmprsomh bxhdktmt fbbph rehebnstemh hpbw hqbvhjbwwmt omnmtsjeno xbkhjtbwqmgbnh nmtgh ikhedh dqst oknneno fsuh xktxpmg nzxxpmg xmjsh nmjeukmjjmh hjkgpz mnoenm nkgm dtshq ikngsnm hjknneno sgs hweymg fetivstmh wmmyh seh wmbn xbxh psheno snheh hjsdy dbxbp iedtbfpbwwemh xsnnmt nedyh jkneno penjh fbhhep wshjem etbn onstpemt dsjh knel isdtbpboemh dtsz wbhjishjmth hpsxxmg kwpbsg wkffeno isenftsim ypkom oknnmg xsngvegjq wmnjeki pmjjmtxbix enjmtnmjh wbpph jmnjsdpm qkffeno wstd jtshqmg fpbbgmg hdtmmn tswmh hbhmh

def main():
    valid_word_set = get_word_set_from_file('dictionary.lst')
    enciphered_words = raw_input("Enter a string of enciphered words: ")
    enciphered_word_set, letter_set = get_words_and_letters_in_string(enciphered_words)

    a, kr, vr = exhaust_certainties(enciphered_word_set, valid_word_set, letter_set)
    if len(kr) > 0:
        a = fill_in_alphabet_from_input(enciphered_word_set, valid_word_set, a, kr, vr)

    print(monoalphabetic_decipher(enciphered_words, a))

main()