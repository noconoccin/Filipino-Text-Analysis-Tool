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
# CLASS FILE FOR MALASAKIT RESPONSES
###################################################################################


class MalasakitResponse:
    """
    Class container for the Malasakit data.

    Args:
        response_id (int): The number indicating a response's order in the data (Response ID / Row Number).
        response (str): The string containing a response.
        tag (str): The string indicating a response's category.

    Attributes:
        response_id (int): The number indicating a response's order in the data (Response ID / Row Number).
        response (str): The string containing a response.
        tag (str): The string indicating a response's category.
        fspost_output (tuple): The Filipino Stanford Part-of-Speech Tagger (word, tag) tuple output.
        fspost_stanford_format (str): The Filipino Stanford Part-of-Speech Tagger output in word|tag Stanford notation.
        pos (str): The Filipino Stanford Part-of-Speech Tagger 'tags only' string.
        insights_phrase (list): The list of insights extracted from a response.
        insights_words (list): The list of list of words (action, target, ...) insights extracted from a response.
        location (str): The string holder for a response's location. This can be added by the users.
        language (str): The language identifier (tl = Tagalog/Filipino, en = English).
    """
    def __init__(self, response_id, response, tag):
        self.response_id = response_id  # Response ID (row ID)
        self.response = response  # Malasakit Response (words)
        self.tag = tag  # Response Category
        self.fspost_output = ('word', 'tag')  # FSPOST (word, tag) Tuple Output
        self.fspost_stanford_format = ""  # FSPOST Output in word|tag Stanford notation
        self.pos = ""  # FSPOST Output POS Tags only in one string
        self.insights_phrase = []  # List of insights extracted from a response
        self.insights_words = []   # List of list of word (action, target ...) insights extracted from a response
        self.location = ""  # Can be added by users
        self.language = ""  # Language identifier
