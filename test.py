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
# TEST MODULE
# Contains sample code for each API module.
###################################################################################

# # Task: Show changes from original input text to its 'no stopwords' counterpart.
# import data_utils
#
# input_file = 'test/in'  # File with input sentences
#
# string_list_1 = data_utils.text_to_list(input_file)  # Get tokenized sentences from input
# string_list_2 = data_utils.text_to_list_without_stopwords(input_file)
#
# flattened_string_list_1 = [" ".join(sublist) for sublist in string_list_1]  # Join tokens into regular sentences
# flattened_string_list_2 = [" ".join(sublist) for sublist in string_list_2]
#
# combined_list = []  # Join the lists
# for fsl1, fsl2 in zip(flattened_string_list_1, flattened_string_list_2):
#     combined_list.append(fsl1 + ' --> ' + fsl2)
#
# data_utils.write_text_file('test/sample_code_result.txt', combined_list)  # Display using write feature

# # Task: Normalize a list of irregular strings.
# import normalize
#
# string_list = ['cge n nga', 'sn n kyo?', 'bro, g k b mmya mag laro?', 'edewups na mudrakels ko sa trip']
# print(normalize.normalize_list(string_list))

# # Task: Identify languages of strings in a list, set language code limits, and identify again.
# import lang_id
#
# string_list = ["I love you", "我爱你", "愛してる", "사랑해", "Σ΄αγαπώ", "Ich liebe Dich"]
# print(lang_id.identify_language_string_list(string_list))
#
# lang_id.set_language(['en', 'zh', 'ja'])
# print(lang_id.identify_language_string_list(string_list))

# # Task: Tag a string and change its formatting.
# import fspost
#
# fspost.set_java_path("")  # Empty string for default tagger model path
# tagged_string = fspost.tag_string('ako nalang ba dito o sasamahan ako ni Nicco ?')
#
# print("Tuple:", tagged_string)
# print("Stanford:", fspost.format_stanford(tagged_string))
# print("POS:", fspost.format_pos(tagged_string))

# # Task: Build a MalasakitResponse object.
#
# import malasakit_response
# import fspost
# import lang_id
# import extract
#
# fspost.set_java_path("")
# response = 'Maglinis ng mga kanal at kalye o itapon ang mga basura'
#
# response_object = malasakit_response.MalasakitResponse(1, response, 'Sanitation')
# response_object.fspost_output = fspost.tag_string(response_object.response)
# response_object.fspost_stanford_format = fspost.format_stanford(response_object.fspost_output)
# response_object.pos = fspost.format_pos(response_object.fspost_output)
# response_object.location = 'Manila, Philippines'
# response_object.language = lang_id.identify_language_string(response_object.response)[0]
#
# extract.extract_insights_phrases([response_object])  # Extraction
# extract.extract_insights_words([response_object])
#
# print('Response ID:', response_object.response_id)
# print('Response:', response_object.response)
# print('Category:', response_object.tag)
# print('FSPOST Tuple:', response_object.fspost_output)
# print('FSPOST Stanford:', response_object.fspost_stanford_format)
# print('FSPOST POS only:', response_object.pos)
# print('Insight Phrases:', response_object.insights_phrase)
# print('Insight Word Sets:', response_object.insights_words)
# print('Location:', response_object.location)
# print('Language:', response_object.language)

# # Task: Organize and cluster a set of insights.
#
# import malasakit_response
# import organize
#
# response_object_1 = malasakit_response.MalasakitResponse(1, 'response1', 'tag1')
# response_object_1.insights_words = [[1, 'maglinis', 'kanal', 'kalye'], [1, 'itapon', 'basura']]
# response_object_2 = malasakit_response.MalasakitResponse(2, 'response2', 'tag2')
# response_object_2.insights_words = [[2, 'magkaisa', 'tao']]
# response_object_3 = malasakit_response.MalasakitResponse(3, 'response3', 'tag3')
# response_object_3.insights_words = [[3, 'magkaroon', 'komunikasyon']]
# response_object_4 = malasakit_response.MalasakitResponse(4, 'response4', 'tag4')
# response_object_4.insights_words = [[4, 'wastong', 'pagtatapon'], [4, 'bantayan', 'gamit']]
# response_object_5 = malasakit_response.MalasakitResponse(5, 'response5', 'tag5')
# response_object_5.insights_words = [[5, 'dumating', 'pagkain'], [5, 'magkaroon', 'equipment'], [5, 'maglinis', 'kalsada']]
#
# response_list = [response_object_1, response_object_2, response_object_3, response_object_4, response_object_5]
#
# cluster_list, ranked_cluster_list = organize.organize_all_entries(response_list, 'dice')
#
# print(cluster_list)
# print(ranked_cluster_list)

# # Task: Compare two words using the three clustering approaches.
# # import cluster
# #
# # string1 = 'malinis'
# # string2 = 'kalinisan'
# #
# # print('Dice:', cluster.string_similarity_dice(string1, string2))
# #
# # try:
# #     similarity = cluster.string_similarity_word2vec(string1, string2)
# # except KeyError:
# #     similarity = 0.0  # No operation done if not on the model, so set similarity to 0
# # print('Word2Vec:', similarity)
# #
# # try:
# #     similarity = cluster.string_similarity_fasttext(string1, string2)
# # except KeyError:
# #     similarity = 0.0  # No operation done if not on the model, so set similarity to 0
# # print('FastText:', similarity)

# # Task: Rank a given list of clusters.
# import rank
#
# cluster_list = [['1|5', 2, 'maglinis', 'kanal, kalye, kalsada'], ['1', 1, 'itapon', 'basura'],
#                 ['2', 1, 'magkaisa', 'tao'], ['3|5', 2, 'magkaroon', 'komunikasyon, equipment'],
#                 ['4', 1, 'wastong', 'pagtatapon'], ['4', 1, 'bantayan', 'gamit'], ['5', 1, 'dumating', 'pagkain']]
#
# print(rank.rank_clusters_by_frequency(cluster_list))

# # Task: Generate a customized report.
#
# import generate
# from docx import Document
#
# document = Document()  # Create an instance of the document
#
# # Use API functions
# generate.set_document_margin(document, -1, 2, 2, 2, 2)
#
# generate.add_divider(document)  # Divider
# generate.add_title(document, 'THIS IS MY FIRST CUSTOMIZED REPORT')  # Title text
# generate.add_divider(document)  # Divider
# generate.add_timestamp(document)  # Timestamp
#
# # Carry on with basic document function/s
# p = document.add_paragraph("This is a paragraph.")
# p.add_run(' In ')
# p.add_run('BOLD').bold = True
# p.add_run(' and ')
# p.add_run('italic.').italic = True
#
# table = document.add_table(rows=1, cols=3)
#
# hdr_cells = table.rows[0].cells
# hdr_cells[0].text = 'Item'
# hdr_cells[1].text = 'Quantity'
# hdr_cells[2].text = 'Description'
#
#
# table_elements = (
#     ('Food', '350,000', 'Contains canned goods, vegetables, eggs, and meat.'),
#     ('Medicine', '93,500', 'Includes vaccines, herbs, and prescription drugs.'),
#     ('Clothes', '51,926', 'Donations consisting of shirt, pants, and underwear.')
# )
#
# for item, quantity, description in table_elements:
#     row_cells = table.add_row().cells
#     row_cells[0].text = str(item)
#     row_cells[1].text = quantity
#     row_cells[2].text = description
#
# p = document.add_paragraph("Additional document functions at: \n")
# p.add_run("https://python-docx.readthedocs.io/en/latest/").bold = True
#
# document.save('test/My First Report.docx')
