###################################################################################
#
# THESIS TITLE: EXTRACTING AND ORGANIZING DISASTER-RELATED PHILIPPINE COMMUNITY
#               RESPONSES FOR AIDING NATIONWIDE RISK REDUCTION PLANNING AND
#               RESPONSE (2020)
#
# AUTHOR/DEVELOPER: Nicco Nocon
# INSTITUTION: De La Salle University, Manila
# EMAIL: noconoccin@gmail.com or nicco_louis_nocon@dlsu.edu.ph
# CONTACT NUMBER: (+63) 917 819 9311
#
# SOURCE OF FUNDING: Philippine-California Advanced Research Institutes (PCARI)
#                    through Commission on Higher Education and Department of
#                    Science and Technology – Science Education Institute
#
###################################################################################
# TEXT NORMALIZATION
# Converts input text/s into standardized forms
# > Joins Unmerged Prefixes (e.g. mag karoon -> magkaroon)
#     > Prefix List based from: A GRAMMAR CHECKER FOR TAGALOG USING LANGUAGETOOL
#                               BY OCO & BORRA (2011)
#         > Paper: https://www.aclweb.org/anthology/W11-3402
#         > Prefixes that can possibly constitute a valid word in Filipino are
#           removed (e.g., na-, ma-, ka-, nang-, i-, makapa-, nakapa-, nakakapa-,
#           pang-, etc.)
# > Filipino Shortcut Text Normalizer: MOSES VERSION OF BUILDING A FILIPINO
#                                      COLLOQUIALISM TRANSLATOR USING SEQUENCE-TO-
#                                      SEQUENCE MODEL BY NOCON, KHO, & ARROYO
#                                      (2018)
#     > Paper: https://ieeexplore.ieee.org/document/8227910
###################################################################################

import os
import data_utils

# Default file paths
# normalizer_directory = 'C:\\cygwin\\[Nokhonfusion]-Filipino-Colloquialism-MT\\'
# model_file_path = normalizer_directory + 'model\\moses.ini'
normalizer_directory = os.path.abspath("model/[Nokhonfusion]-Filipino-Colloquialism-MT/")
dictionary_directory = 'model/dictionary/'
test_directory = 'test/'
input_file_path = test_directory + 'in'
output_file_path = test_directory + 'out'
model_file_path = normalizer_directory + '\\model\\moses.ini'
moses_file_path = 'C:\\cygwin\\mosesdecoder-master\\bin\\moses'
prefix_file_path = dictionary_directory + 'tl_prefixes.txt'


def normalize_object(malasakit_response_list):
    """
    Function that normalizes the MalasakitResponse object. Updates the object after normalization.

    Args:
        malasakit_response_list (list): The list containing MalasakitResponse objects with responses to be normalized.
    """
    text_list = []

    # Put all responses in a list
    for malasakit_response in malasakit_response_list:
        text_list.append(malasakit_response.response)

    # Normalize the list
    normalized_string_list = normalize_list(text_list)

    # Update malasakit_response object
    for malasakit_response, new_response in zip(malasakit_response_list, normalized_string_list):
        # print(malasakit_response.response, 'to', new_response)
        malasakit_response.response = new_response


def normalize_list(string_list):
    """
    Function that normalizes a given list of strings. Returns the normalized list.

    Args:
        string_list (list): The list of strings to be normalized.

    Returns:
        normalized_string_list: the normalized version of the input string list.
    """
    # Run Prefix-Word Joiner. Add to more prefixes to join in prefix_list
    joined_prefix_word_string_list = join_prefix_word(string_list)

    # Write the prefix-word joined list to a text file
    data_utils.write_text_file(input_file_path, joined_prefix_word_string_list)

    # Run Filipino Colloquialism Translator through command prompt (make sure that cygwin/moses is in system environment
    # variable and that file paths are correct). Uses the default file paths
    translate_filipino_colloquialism(moses_file_path, model_file_path, input_file_path, output_file_path)

    # Read the file with the normalized counterparts. Make sure to have the same file path of the output file
    normalized_string_list = data_utils.read_text_file(output_file_path)

    # print(normalized_string_list)

    return normalized_string_list


def normalize_string(string):
    """
    Function that normalizes a given string. Returns the normalized string.

    Args:
        string (string): The string to be normalized.

    Returns:
        normalized_string: the normalized version of the input string.
    """
    # Run Prefix-Word Joiner. Add to more prefixes to join in prefix_list
    joined_prefix_word_string_list = join_prefix_word([string])

    # Write the prefix-word joined list to a text file
    data_utils.write_text_file(input_file_path, joined_prefix_word_string_list)

    # Run Filipino Colloquialism Translator through command prompt (make sure that cygwin/moses is in system environment
    # variable and that file paths are correct). Uses the default file paths
    translate_filipino_colloquialism(moses_file_path, model_file_path, input_file_path, output_file_path)

    # Read the file with the normalized counterparts. Make sure to have the same file path of the output file
    normalized_string = data_utils.read_text_file(output_file_path)[0]  # Returns a list so only return the first elem.

    # print(normalized_string)

    return normalized_string


def join_prefix_word(string_list):
    """
    Function that joins the prefixes that are separated with a word by whitespace. More prefixes can be added in the
    tl_prefixes.txt file. Ex. mag karoon --> magkaroon.

    Args:
        string_list (list): The list of string to be processed.

    Returns:
        joined_prefix_word_string_list: a list of string with joined prefix-word modifications.
    """
    joined_prefix_word_string_list = []
    prefix_list = data_utils.read_text_file(prefix_file_path)  # prefix_list = ['mag', ...]
    print(prefix_list)

    for string in string_list:
        new_string = ''
        for word in string.split():
            if word in prefix_list:
                new_string += word  # Join, don't put a space
            else:
                new_string += word + ' '  # Shouldn't be joined, add as space
        joined_prefix_word_string_list.append(new_string)  # Add to the new list

    return joined_prefix_word_string_list


def translate_filipino_colloquialism(moses_file, model_file, input_file, output_file):
    """
    Function that runs the Filipino Colloquialism Translator through command prompt (make sure that cygwin/moses is in
    system environment variable and that file paths are correct). Parameters can be changed by user.

    Args:
        moses_file (str): The file location of Moses executable file.
        model_file (str): The file location of the normalizer model.
        input_file (str): The file location of the input text (source - to be normalized).
        output_file (str): The file location of the output text (target - normalized version of the input).
    """
    # Sample command: C:/cygwin/mosesdecoder-master/bin/moses -f
    #                 C:/cygwin/[Nokhonfusion]-Filipino-Colloquialism-MT/model/moses.ini < in > out -dl 0
    command = moses_file + ' -f ' + model_file + ' < ' + input_file + ' > ' + output_file + ' -dl 0'
    os.system('cmd /c ' + command)


def set_moses_file_path(filename):
    """
    Function that sets Moses' executable file path with the one provided by the user.

    Args:
        filename (str): The file location of the Moses executable file.
    """
    global moses_file_path
    moses_file_path = filename


def set_model_file_path(filename):
    """
    Function that sets Moses' model configuration file path with the one provided by the user.

    Args:
        filename (str): The file location of the normalizer model.
    """
    global model_file_path
    model_file_path = filename


def set_input_file_path(filename):
    """
    Function that sets Moses' input file path with the one provided by the user.

    Args:
        filename (str): The file location of the input text.
    """
    global input_file_path
    input_file_path = filename


def set_output_file_path(filename):
    """
    Function that sets Moses' output file path with the one provided by the user.

    Args:
        filename (str): The file location of the output text.
    """
    global output_file_path
    output_file_path = filename


def set_prefix_file_path(filename):
    """
    Function that sets a user-provided prefix list text file.

    Args:
        filename (str): The file location of the prefix list.
    """
    global prefix_file_path
    prefix_file_path = filename

# Local test
# normalize_string("mag karoon ng pagkakaiisa upang sa mga darating na mga sakuna ay malalagpasan khit wl")
# normalize_list(["khit wl kcguruhan kung mbbigyan ktuparan wish na yon bsta ippramdam qng mhal q cya at susuportahan q
#                 "
#                 "cya",
#                 "pra sa akin dpat lgi nla iinform ang mga tao kung kailangn n bng lumikas pra maiwasan ang sakuna at "
#                 "bgyan ng importansya lalo n ang mga pwd n kailngn ng tamang tulong",
#                 "lgi sana mgkaroon ang brgy ng mga gamot n kailngn lalo n sa di inaasahang sakuna",
#                 "karagdagang kagamitan sa brgy para sa disaster gaya ng disaster kit, megaphone, at iba pa. ",
#                 "mag karoon ng pagkakaiisa upang sa mga darating na mga sakuna ay malalagpasan",
#                 "mag tolungan o mag kaisa",
#                 "they prepare us on what we're going to do",
#                 "go ! keribels mo yan . hehe .",
#                 "Oh I see thought u r doing some voluntary service or something like that",
#                 "magdasal"])

# os.system('cmd /k "color a"')
# os.system('cmd /c "../bin/moses -f phrase-model/moses.ini < phrase-model/in > phrase-model/out"')
# os.system('cmd /k "cd /mosesdecoder-master/norm-model"')
# cd C:\cygwin\normapi
# C:/cygwin/mosesdecoder-master/bin/moses -f norm/training/model/moses.ini < in > normAPIout
# C:/cygwin/mosesdecoder-master/bin/moses -f C:/cygwin/[Nokhonfusion]-Filipino-Colloquialism-MT/model/moses.ini


# normalize_string("sn n kyo?")
# print(join_prefix_word(['mag karoon', 'pag laro']))
