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
# MAIN - FULL RUN MODULE
# Runs all of the modules, processing a dataset provided (Malasakit responses by
# default). It follows the architectural diagram of the research.
###################################################################################

import data_utils
import fspost
import lang_id
import extract
import organize
import generate
import copy
import timeit
# import normalize
# import cluster

# START TIME
start_time = timeit.default_timer()

# -- START MODULE --
print('Setting up resources...')
start_module_time = timeit.default_timer()

# CONFIGURATIONS (USER MODIFIABLE) ####################################################################################
java_path = ''  # Java Path for Stanford POS Tagger (empty string for default)
malasakit_filename = 'test/MalasakitResponses_small.xlsx'
report_filename = 'test/Report.docx'
protected_cells = 2  # Protect the first two columns (response & tag)
organization_type = ''  # '' default for all entries, 'categories' for organize by response categories
clustering_technique = 'dice'  # dice, word2vec, fasttext
priority_categories = []  # [] for default categories
#######################################################################################################################
# gold_standard_filename = 'test/GoldStandard.xlsx'


# INITIALIZE NECESSARY OBJECTS
# malasakit_response_list = []  # List of Malasakit Response Objects

# INITIAL STEPS
fspost.set_java_path(java_path)  # Set Java Path for Stanford POS Tagger (empty string for default)
data_utils.refresh_excel(malasakit_filename, protected_cells)  # Refresh cells in Test Data

# READ MALASAKIT DATA
malasakit_response_list = data_utils.read_excel(malasakit_filename)

print('\x1b[5;30;42m', 'Resources set! Elapsed time:', (timeit.default_timer() - start_module_time), '\x1b[0m')
# -- END MODULE --

# # -- START MODULE --
# print('Normalizing...')
# start_module_time = timeit.default_timer()
#
# # NORMALIZATION (TYPOS, SHORTCUTS, SEPARATED PREFIXES)
# normalize.normalize_object(malasakit_response_list)
#
# print('\x1b[5;30;42m', 'Normalization done! Elapsed time:', (timeit.default_timer() - start_module_time), '\x1b[0m')
# # -- END MODULE --

# -- START MODULE --
print('Identifying Language...')
start_module_time = timeit.default_timer()

# LANGUAGE IDENTIFICATION (To be used in future functionalities -- English support)
lang_id.identify_language_object_list(malasakit_response_list)

print('\x1b[5;30;42m', 'Language Identification done! Elapsed time:', (timeit.default_timer() - start_module_time),
      '\x1b[0m')
# -- END MODULE --

# -- START MODULE --
print('Tagging POS...')
start_module_time = timeit.default_timer()

# PART-OF-SPEECH TAGGING
fspost.tag_object_list(malasakit_response_list)

print('\x1b[5;30;42m', 'POS Tagging done! Elapsed time:', (timeit.default_timer() - start_module_time), '\x1b[0m')
# -- END MODULE --

# -- START MODULE --
print('Extracting Information...')
start_module_time = timeit.default_timer()
ie_phrases_time = start_module_time

# PART-OF-SPEECH-BASED INFORMATION EXTRACTION
extract.extract_insights_phrases(malasakit_response_list)
print('\x1b[5;30;42m', 'Phrases done! Elapsed time:', (timeit.default_timer() - ie_phrases_time), '\x1b[0m')

ie_phrases_time = timeit.default_timer()

extract.extract_insights_words(malasakit_response_list)
print('\x1b[5;30;42m', 'Word Set done! Elapsed time:', (timeit.default_timer() - ie_phrases_time), '\x1b[0m')

print('\x1b[5;30;42m', 'Information Extraction done! Elapsed time:', (timeit.default_timer() - start_module_time),
      '\x1b[0m')
# -- END MODULE --

# COPY OBJECT - Created to prevent changes in clustering from being applied in malasakit_response_list object
malasakit_response_list_copy = copy.deepcopy(malasakit_response_list)

# INFORMATION ORGANIZATION
# Grouped by response categories and ranked based on frequency.
# The clustering_technique can be selected by one of the following input text: 'dice', 'word2vec', or 'fasttext'
# clusters_list, ranked_clusters_list = organize.organize_by_response_categories(malasakit_response_list_copy,
#                                                                               clustering_technique='fasttext')

# No grouping - no boundaries in clustering all entries
# The clustering_technique can be selected by one of the following input text: 'dice', 'word2vec', or 'fasttext'
# clusters_list, ranked_clusters_list = organize.organize_by_response_categories(malasakit_response_list_copy,
#                                                                                clustering_technique='dice')
# clusters_list, ranked_clusters_list = organize.organize_by_response_categories(malasakit_response_list_copy,
#                                                                                clustering_technique='fasttext',
#                                                                                priority_categories=['Entertainment',
#                                                                                                     'Opinion',
#                                                                                                     'Sports',
#                                                                                                     'World'])
if organization_type == 'categories':
    clusters_list, ranked_clusters_list = organize.organize_by_response_categories(malasakit_response_list_copy,
                                                                                   clustering_technique,
                                                                                   priority_categories)
else:
    clusters_list, ranked_clusters_list = organize.organize_all_entries(malasakit_response_list_copy,
                                                                        clustering_technique)

# -- START MODULE --
print('Generating Report...')
start_module_time = timeit.default_timer()

# REPORT GENERATION
generate.write_report(report_filename, malasakit_response_list, ranked_clusters_list)

print('\x1b[5;30;42m', 'Report Generation done! Elapsed time:', (timeit.default_timer() - start_module_time), '\x1b[0m')
# -- END MODULE --

# EVALUATION MODULE
# ie_list_phrases = cluster.collect_all_insights_from_object(malasakit_response_list, 'p')  # Retrieves all IE outputs
# ie_list_words = cluster.collect_all_insights_from_object(malasakit_response_list, 'w')
# gold_standard_list_phrases = data_utils.read_gold_standard_excel(gold_standard_filename, 2)
# gold_standard_list_words = data_utils.read_gold_standard_excel(gold_standard_filename, 3)
# print('IE LIST PHRASES:', ie_list_phrases)
# print('GS LIST PHRASES:', gold_standard_list_phrases)
# print('IE LIST WORDS:', ie_list_words)
# print('GS LIST WORDS:', gold_standard_list_words)
# evaluate.compare_ie_phrases(ie_list_phrases, gold_standard_list_phrases)
# evaluate.compare_ie_word_sets(ie_list_words, gold_standard_list_words)

# WRITE IN TEST DATA
data_utils.write_excel(malasakit_filename, malasakit_response_list, clusters_list, ranked_clusters_list)

stop_time = timeit.default_timer()

print('\x1b[5;30;42m', 'PROGRAM TIME:', (stop_time - start_time), '\x1b[0m')
# NOTES:

# SAMPLE CODE FOR TAGGING A SENTENCE
# print(fspost.tag_string('magkaisa dapat ang mga tao'))
# Sample Code for Tagging List of Sentences
# sentence_list = ['magkaisa dapat ang mga tao',
#                   'magkaroon ng komunikasyon kung saan magkikita sa panahon ng kalamaidad']
# tagged_list = fspost.tag_string_list(sentence_list)  # Output a tuple
# for sentence in tagged_list:
#    print(fspost.format_stanford(sentence)) # Output a Stanford word|tag format

# DISPLAY OUTPUT (FOR TRACING)
# print()
# for malasakit_response in malasakit_response_list:
#     print('RESPONSE #{}: '.format(malasakit_response.response_id))
#     print(malasakit_response.response)
#     print(malasakit_response.tag)
#     print(malasakit_response.fspost_output)
#     print(malasakit_response.fspost_stanford_format)
#     print(malasakit_response.pos)
#     print(malasakit_response.language)
#     print(malasakit_response.insights_phrase)
#     print(malasakit_response.insights_words)
#     print()
#
# print(clusters_list)
