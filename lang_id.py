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
# LANGUAGE IDENTIFICATION
# > Paper: https://www.aclweb.org/anthology/P12-3005
# > Library [langid]: https://github.com/saffsd/langid.py
###################################################################################

import langid


def set_language(code_list):
    """
        Function that changes the scope of languages.

        Args:
            code_list (list): List of languages to be considered.
    """
    langid.set_languages(code_list)  # Filters the model to consider only given language set


def identify_language_string(sentence):
    """
    Function that identifies the language (ISO 639-1 code) of a given string. Output is a (language, confidence) tuple.

    Args:
        sentence (str): The sentence to be language identified.

    Returns:
        language: a tuple consisting of (language, confidence) fields.
    """
    language = langid.classify(sentence)
    return language


def identify_language_object_list(malasakit_response_list):
    """
    Function that identifies the language (tl = Tagalog/Filipino or en = English) of MalasakitResponse object's
    responses. This updates the MalasakitResponse object.

    Args:
        malasakit_response_list (list): The list containing MalasakitResponse objects.
    """
    langid.set_languages(['en', 'tl'])  # Filters the model to consider only two languages (English and Tagalog)
    for malasakit_response in malasakit_response_list:
        malasakit_response.language = identify_language_string(malasakit_response.response)


# Function that identifies the language of sentences in a list. Output is a list of lang. respective to the sentences.
def identify_language_string_list(sentence_list):
    """
    Function that identifies the language of sentences in a list. Output is a list of languages respective to the
    sentences.

    Args:
        sentence_list (list): The list of strings to be language identified.

    Returns:
        language_identified_list: a list containing the language result.
    """
    language_identified_list = []
    for sentence in sentence_list:
        language_identified_list.append(identify_language_string(sentence))
    return language_identified_list
