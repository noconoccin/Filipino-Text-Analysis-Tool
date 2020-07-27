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
# FILIPINO STANFORD PART-OF-SPEECH TAGGER (FSPOST) BY GO & NOCON (2017)
# > Paper: https://www.aclweb.org/anthology/Y17-1014
# > Library [nltk]: https://www.nltk.org/
###################################################################################

import os
import nltk
from nltk.tag.stanford import StanfordPOSTagger

model = 'model\\filipino-left5words-owlqn2-distsim-pref6-inf2.tagger'
jar = 'lib\\stanford-postagger.jar'
fspost = StanfordPOSTagger(model, path_to_jar=jar)  # Load Tagger Model
fspost._SEPARATOR = '|'  # Set separator for proper tuple formatting (word, tag)


def set_java_path(file_path):
    """
    Function for setting java path to make Stanford POS Tagger work. Makes use of the 'os' library. Input "" to use
    default java path, otherwise set the location.

    Args:
        file_path (str): The java file path / location.
    """
    if file_path == "":
        java_path = "C:/Program Files/Java/jdk1.8.0_111/bin/java.exe"
        print("Java path set by default")
    else:
        java_path = file_path
        print("Java path set from given")
    os.environ['JAVAHOME'] = java_path


def tag_string(sentence):
    """
    Function for tagging a sentence/string. Output is a (word, pos) tuple. To output a POS-only string, enclose this
    function with 'format_pos' function. Ex. fspost.format_pos(fspost.tag_string('this is a string')). Same goes for
    Stanford's word|tag notation, use 'format_stanford' function.

    Args:
        sentence (str): The string to be tagged.

    Returns:
        tagged_string: a list of string tokens containing POS labeled (word, pos) tuples.
    """
    tokens = sentence.split()  # Tokenize Sentence by whitespaces
    # print(tokens)
    tagged_string = fspost.tag(tokens)
    return tagged_string


def tag_object_list(malasakit_response_list):
    """
    Function for tagging a list of MalasakitResponse object's sentence. This updates the MalasakitResponse object.

    Args:
        malasakit_response_list (list): The list containing the MalasakitResponse objects.
    """
    progress_ctr = 0
    # tagged_list = []  # Initialize an empty list
    for malasakit_response in malasakit_response_list:
        if malasakit_response.language[0] == 'tl':
            tagged_tuple = tag_string(malasakit_response.response)  # Tag each sentence in the list
        else:
            tagged_tuple = nltk.pos_tag(malasakit_response.response.split())
        malasakit_response.fspost_output = tagged_tuple  # Set tagged string to MalasakitResponse object
        tagged_string = format_stanford(tagged_tuple)  # Format the tuple into Stanford word|tag notation
        malasakit_response.fspost_stanford_format = tagged_string  # Set Stanford format
        tagged_string = format_pos(tagged_tuple)  # Collects all POS in the sentence into one string
        malasakit_response.pos = tagged_string  # Set POS-only string
        # tagged_list.append(tagged_string)  # Insert tagged sentence in the new list
        progress_ctr += 1
        print(progress_ctr, "/", len(malasakit_response_list))  # Progress Counter / Total # of Responses
    # return tagged_list


# Function for tagging a list of sentences. Output is a list of (word, pos) tuple.
def tag_string_list(sentence_list):
    """
    Function for tagging a list of sentences. Output is a list of (word, pos) tuple. To output a POS-only string,
    enclose the elements in this function with 'format_pos' function. Same goes for Stanford's word|tag notation, use
    'format_stanford' function.

    Args:
        sentence_list (list): The list of strings to be tagged.

    Returns:
        tagged_list: a list of strings containing POS labelled (word, pos) tuples.
    """
    progress_ctr = 0
    tagged_list = []  # Initialize an empty list
    for sentence in sentence_list:
        tagged_tuple = tag_string(sentence)  # Tag each sentence in the list
        tagged_list.append(tagged_tuple)  # Insert tagged sentence in the new list
        progress_ctr += 1
        print(progress_ctr, "/", len(sentence_list))  # Progress Counter
    return tagged_list


def format_pos(input_tuple):
    """
    Function for formatting a tuple into a POS-only string.

    Args:
        input_tuple (tuple): The tuple to be formatted.

    Returns:
        tagged_string: a string containing POS labels.
    """
    tagged_string = ""
    for curr_tuple in input_tuple:
        tagged_string += curr_tuple[1] + " "
    return tagged_string.strip()


def format_stanford(input_tuple):
    """
    Function for formatting a tuple into Stanford word|tag string.

    Args:
        input_tuple (tuple): The tuple to be formatted.

    Returns:
        tagged_string: a string containing POS labels in Stanford's word|tag notation.
    """
    tagged_string = ""
    for curr_tuple in input_tuple:
        tagged_string += curr_tuple[0] + "|" + curr_tuple[1] + " "
    return tagged_string.strip()
