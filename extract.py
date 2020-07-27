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
# PART-OF-SPEECH-BASED INFORMATION EXTRACTION
# Extracts information by using Part-of-Speech (e.g., verbs, noun, etc.) patterns
# to determine key points in a text. Uses Filipino Stanford Part-of-Speech Tagger
# by Go & Nocon (2017).
###################################################################################


def extract_insights_phrases(malasakit_response_list):
    """
    Function for extracting phrase insights (action word to target/s). The MalasakitResponse object is updated after
    this function.

    Args:
        malasakit_response_list (list): The list containing MalasakitResponse objects with responses to be extracted.
    """
    # insights_list = []  #  A list of all the insights in the data (not used)
    extracted_phrase = ""

    # Iterate through all responses/sentences
    for malasakit_response in malasakit_response_list:
        insights = []  # Insights list: [response_id, action, target/s]
        record = False
        index_ctr = 0
        words = malasakit_response.response.split()
        tags = malasakit_response.pos.split()

        # Looking per word, trace the Verb Phrases / Insights
        # Criteria: Record those that starts with VB and ends with NN or FW, and record var. should end with False
        for word, tag in zip(words, tags):
            # print(word, tag, record, tags.index(tag), len(tags)-1)
            # If not recording and a VB (verb) is seen, start recording
            if not record:
                # If tag contains VB and is not the last tag in the list
                if "VB" in tag and index_ctr != (len(tags)-1):  # tags.index(tag) has been changed into index_ctr
                    # print("Start Recording VB at:", word, tag)
                    record = True  # Starts recording
                    extracted_phrase += word + " "
                # VB as last word (Check: doesn't capture single word VB and VB without Noun shouldn't be accepted)
                # elif "VB" in tag and index_ctr == (len(tags)-1):
                #    extracted_phrase += word + " "
                #    insights.append(extracted_phrase.replace(".", " ").strip())
                #    extracted_phrase = ""  # Reset variable
                # elif "NN" in tag: # NNC CCB/CCT NNC
                #    record = True
                #    extracted_phrase += word + " "
                # Included instances of JJD/JJD_CCP as starting word
                elif "JJD" in tag or "JJD_CCP" in tag:  # How about JJ?
                    # print("Start Recording JJD/JJD_CCP at:", word, tag)
                    record = True
                    extracted_phrase += word + " "
            # If recording...
            else:
                # If the last word, deliberate whether the recording has been completed (stopped at NN/FW)
                if index_ctr == (len(tags)-1):
                    # print("Stop Recording Last Word at:", word, tag)
                    record = False  # For those with short responses that doesn't stop at NN
                    if "NN" in tag or "FW" in tag:
                        extracted_phrase += word + " "
                    else:
                        extracted_phrase = ""  # Penalty for not completing criteria of an insight, thus discarded
                # If not the last word, find NN (noun) or FW (foreign word)
                # If it is found, check the next tag to know if recording should be continued or not
                elif (index_ctr + 1) < len(tags):
                    if "NN" in tag:
                        # Check next tag, if NN, PMC, or CCA: continue; if not, stop recording
                        if "NN" not in tags[index_ctr + 1]:  # Split into 2 ifs to shorten paragraph
                            if "PMC" not in tags[index_ctr + 1] and "CCA" not in tags[index_ctr + 1]:
                                # print("Stop Recording NN at:", word, tag)
                                record = False  # Stop recording
                        # else, do nothing, continue scanning
                    elif "FW" in tag:
                        # Check next tag, if FW, PMC, or CCA: continue; if not, stop recording
                        if "FW" not in tags[index_ctr + 1]:  # Split into 2 ifs to shorten paragraph
                            if "PMC" not in tags[index_ctr + 1] and "CCA" not in tags[index_ctr + 1]:
                                # print("Stop Recording FW at:", word, tag)
                                record = False  # Stop recording
                        # else, do nothing, continue scanning
                    # If record is true, extract and join the word in extracted_phrase
                    extracted_phrase += word + " "

                # Validation: if criteria is met, set to object
                if extracted_phrase != "" and not record:
                    insights.append(extracted_phrase.replace(".", " ").strip())
                    malasakit_response.insights_phrase = insights  # Store in the object
                    extracted_phrase = ""  # Reset variable

            # Pass by if conditions are met
            index_ctr += 1

        # print("Insight is empty:", not insights)
        if not insights:
            print('No insights (phrase) extracted at Response #:', malasakit_response.response_id)
        else:
            insights.insert(0, malasakit_response.response_id)  # Add reference to which response they belong to
            # print(insights)

        # insights_list.append(insights)
    # return insights_list


# Function for extracting word insights (action word and target/s).
def extract_insights_words(malasakit_response_list):
    """
    Function for extracting word insights (action word and target/s). The MalasakitResponse object is updated after this
    function.

    Args:
        malasakit_response_list (list): The list containing MalasakitResponse objects with responses to be extracted.
    """
    extracted_noun_group = ""

    # Iterate through all the responses/sentences
    for malasakit_response in malasakit_response_list:
        insights_list = []  # 2D container list of insights per response
        insights = []  # Insights list: [response_id, action, target/s]
        record = False
        index_ctr = 0
        words = malasakit_response.response.split()
        tags = malasakit_response.pos.split()

        # Looking per word, extract the action and target/s of the insights
        # Put in list the response_id, action, and target/s
        for word, tag in zip(words, tags):
            # If not recording and a VB (verb) is seen, extract and start recording
            if not record:
                # If tag contains VB and is not the last tag in the list
                if "VB" in tag and index_ctr != (len(tags) - 1):  # tags.index(tag) has been changed into index_ctr
                    # print("Start Recording VB at:", word, tag)
                    record = True  # Starts recording
                    insights.append(word.strip())
                    # print(insights)
                # VB as last word (Check: doesn't capture single word VB and VB without Noun shouldn't be accepted)
                # elif "VB" in tag and index_ctr == (len(tags)-1):
                #    insights.append(word.strip())
                # elif "NN" in tag: # NNC CCB/CCT NNC
                #    record = True
                #    insights.append(word.strip())
                # Included instances of JJD/JJD_CCP as starting word
                elif "JJD" in tag or "JJD_CCP" in tag:  # How about JJ?
                    # print("Start Recording JJD/JJD_CCP at:", word, tag)
                    record = True
                    insights.append(word.strip())
                    # print(insights)
            # If recording...
            else:
                # If the last word, deliberate whether the recording has been completed (stopped at NN/FW)
                if index_ctr == (len(tags) - 1):
                    # print("Stop Recording Last Word at:", word, tag)
                    record = False  # For those with short responses that doesn't stop at NN
                    if "NN" in tag or "FW" in tag:
                        extracted_noun_group += word
                        insights.append(extracted_noun_group.strip())
                        # print(insights)
                        extracted_noun_group = ""
                    # Else: Penalty for not completing criteria of an insight, thus discarded/do nothing
                # If not the last word, find NN (noun) or FW (foreign word)
                # If it is found, check the next tag to know if recording should be continued or not
                # This is for concatenating the targets
                elif (index_ctr + 1) < len(tags):
                    if "NN" in tag:
                        insights.append(word)
                        # print(insights)
                        if "NN" not in tags[index_ctr + 1]:
                            if "PMC" not in tags[index_ctr + 1] and "CCA" not in tags[index_ctr + 1]:
                                record = False  # Stop recording
                        # FUTURE ISSUE: Multi-word Nouns (perform lexicalization? one word to represent all targets)
                        # Removed this to prevent joining Kanal Kalye (this is harder without commas)
                        # Check next tag: if NN, concatenate
                        #                 if PMC or CCA: continue
                        #                 if not, stop recording
                        # if "NN" in tags[index_ctr + 1]:
                        #    # Joins connected NNs: bahay kubo, poso negro (pending examples)
                        #    extracted_noun_group += word + " "
                        # else:
                        #    # If there are non-FW words after
                        #    extracted_noun_group += word
                        #    insights.append(extracted_noun_group.strip())
                        #    print(insights)
                        #    extracted_noun_group = ""  # Reset variable
                        #    if "PMC" not in tags[index_ctr + 1] and "CCA" not in tags[index_ctr + 1]:
                        #        record = False  # Stop recording
                    elif "FW" in tag:
                        insights.append(word)
                        # print(insights)
                        if "FW" not in tags[index_ctr + 1]:
                            if "PMC" not in tags[index_ctr + 1] and "CCA" not in tags[index_ctr + 1]:
                                record = False  # Stop recording
                        # Check next tag: if FW, concatenate
                        #                 if PMC or CCA: continue
                        #                 if not, stop recording
                        # if "FW" in tags[index_ctr + 1]:
                        #    # Joins connected FWs: Medical Kit, Garbage Can
                        #    extracted_noun_group += word + " "
                        # else:
                        #    # If there are non-FW words after
                        #    extracted_noun_group += word
                        #    insights.append(extracted_noun_group.strip())
                        #    print(insights)
                        #    extracted_noun_group = ""  # Reset variable
                        #    if "PMC" not in tags[index_ctr + 1] and "CCA" not in tags[index_ctr + 1]:
                        #        record = False  # Stop recording

                # Validation: if criteria is met, set to object
                if insights and not record and len(insights) != 1:
                    insights.insert(0, malasakit_response.response_id)  # Add reference to which response they belong to
                    insights_list.append(insights)
                    # print(insights)
                    # print(insights_list)
                    insights = []  # Reset list

            # Pass by if conditions are met
            index_ctr += 1

        # print("Insight List is empty:", not insights_list)
        if not insights_list:
            print('No insights (words) extracted at Response #:', malasakit_response.response_id)
        else:
            malasakit_response.insights_words = insights_list  # Store in the object
            # print(insights_list)

    # return insights_list
