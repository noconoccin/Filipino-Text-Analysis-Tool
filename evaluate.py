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
# EVALUATION MODULE
# A collection of evaluation metrics (used for comparing two lists):
#   > Precision
#   > Recall
#   > F-Measure
###################################################################################

import data_utils
# import cluster
# import fspost

gold_standard_filename = 'test/MalasakitResponses_GoldStandard_Norm.xlsx'
system_output_filename = 'test/Experiments/MalasakitResponses_934_dice_org_all_norm.xlsx'
gold_standard_filename_small = 'test/GoldStandard_small.xlsx'
system_output_filename_small = 'test/MalasakitResponses_small.xlsx'


def precision(true_positive, false_positive):
    """
        Function for computing precision.

        Args:
            true_positive (int): System EXTRACTED a text that is an insight / in the Gold Standard.
            false_positive (int): System EXTRACTED a text that is not an insight / not in the Gold Standard.

        Returns:
            precision_value: score from TP / (TP + FP).
    """
    print('Compute Precision')
    # Precision = # of correct extractions given by the IE system / total # of extractions given by the IE system
    # Precision = TP / TP + FP
    # precision_value = correct_extractions / total_extractions
    precision_value = true_positive / (true_positive + false_positive)
    return precision_value


def recall(true_positive, false_negative):
    """
        Function for computing recall.

        Args:
            true_positive (int): System EXTRACTED a text that is an insight / in the Gold Standard.
            false_negative (int): System did NOT EXTRACT a text that is an insight / in the Gold Standard

        Returns:
            recall_value: score from TP / (TP + FN).
    """
    print('Compute Recall')
    # Recall = # of correct extractions given by the IE system / total # of possible correct extractions in text
    # Recall = TP / TP + FN
    # recall_value = correct_extractions / gold_standard_extractions
    recall_value = true_positive / (true_positive + false_negative)
    return recall_value


def accuracy(true_positive, false_positive, false_negative, true_negative):
    """
        Function for computing accuracy.

        Args:
            true_positive (int): System EXTRACTED a text that is an insight / in the Gold Standard.
            false_positive (int): System EXTRACTED a text that is not an insight / not in the Gold Standard.
            false_negative (int): System did NOT EXTRACT a text that is an insight / in the Gold Standard.
            true_negative: System did NOT EXTRACT a text that is not an insight / not in the Gold Standard.

        Returns:
            accuracy_value: score from (TP + TN) / (TP + FP + FN + TN).
    """
    print('Compute Accuracy')
    # Accuracy = TP + TN / TP + FP + FN + TN
    accuracy_value = (true_positive + true_negative) / (true_positive + false_positive + false_negative + true_negative)
    return accuracy_value


def f_measure(precision_value, recall_value):
    """
        Function for computing F-Measure.

        Args:
            precision_value (float): System EXTRACTED a text that is an insight / in the Gold Standard.
            recall_value (float): System EXTRACTED a text that is not an insight / not in the Gold Standard.

        Returns:
            f_measure_value: score from (2 * P * R) / (P + R).
    """
    print('Compute F-Measure')
    # F-Measure = 2 x Precision x Recall / Precision + Recall
    f_measure_value = (2 * precision_value * recall_value) / (precision_value + recall_value)
    return f_measure_value


def retrieve_text(candidate_filename, reference_filename):
    """
        Function for reading contents in candidate and gold standard excel files and stores their values in lists.

        Args:
            candidate_filename (str): file location of the candidate.
            reference_filename (str): file location of the reference / gold standard.

        Returns:
            phrase_list: a list of strings containing the system extracted (phrases) information.
            word_set_list: a list of strings containing the system extracted (word sets) information.
            reference_phrase_list: a list of strings containing the gold standard (phrases) information.
            reference_word_set_list: a list of strings containing the gold standard (word sets) information.
            word_counter: a value indicating the total number of words in the input sentence / whole corpus.
    """
    phrase_list = []
    word_set_list = []
    reference_phrase_list = []
    reference_word_set_list = []

    phrase_list, word_set_list, word_counter = data_utils.read_candidate_excel(candidate_filename)
    # print(phrase_list)
    # print(word_set_list)

    reference_phrase_list, reference_word_set_list = data_utils.read_gold_standard_excel(reference_filename)
    # print(reference_phrase_list)
    # print(reference_word_set_list)

    return phrase_list, word_set_list, reference_phrase_list, reference_word_set_list, word_counter


def compare_ie_phrases(system_output_list, gold_standard_list, word_count):
    """
        Function for evaluating insight phrases. Displays statistics and results of computed standard metrics.

        Args:
            system_output_list (list): a list of strings containing the system extracted (phrases) information.
            gold_standard_list (list): a list of strings containing the gold standard (phrases) information.
            word_count (int): a value indicating the total number of words in the input sentence / whole corpus.
    """
    print('Evaluate IE Phrases')

    # Result Containers
    complete_match_list = []
    over_extractions_list = []
    under_extractions_list = []
    overlapping_extractions_list = []
    complete_mismatch_list = []
    true_positive_list = []
    false_positive_list = []
    false_negative_list = []
    true_negative_list = []

    # Preliminary Values
    gold_standard_extractions = 0  # Gold Standard Extractions
    system_extractions = 0  # System Total Extractions

    # Insights - Fraction (complete matches / gold standard extractions)
    complete_match = 0  # Extracted text exactly matches the one in Gold Standard (tp)
    over_extractions = 0  # Partial match with System extractions greater than Gold Standard contents (partial tp)
    under_extractions = 0  # Partial match with system extractions lesser than Gold Standard contents (partial tp)
    overlapping_extractions = 0  # Partial match with equal lengths that have overlapping words like w1 w2 w3 - w2 w3 w4
    complete_mismatch = 0  # Extracted text did not match those in Gold Standard or vice-versa (fp, fn, tn)

    # Insight counts
    true_positive = 0  # System EXTRACTED a text that is an insight / in the Gold Standard
    false_positive = 0  # System EXTRACTED a text that is not an insight / not in the Gold Standard
    false_negative = 0  # System did NOT EXTRACT a text that is an insight / in the Gold Standard
    true_negative = 0  # System did NOT EXTRACT a text that is not an insight / not in the Gold Standard (no value)

    # Word counts
    true_positive_wc = 0  # System EXTRACTED a text that is an insight / in the Gold Standard
    false_positive_wc = 0  # System EXTRACTED a text that is not an insight / not in the Gold Standard
    false_negative_wc = 0  # System did NOT EXTRACT a text that is an insight / in the Gold Standard
    true_negative_wc = 0  # System did NOT EXTRACT a text that is not an insight / not in the Gold Standard
    # total word count - (tp + fp + fn word counts)

    # IE Phrases Comparison
    if len(system_output_list) == len(gold_standard_list):  # Check and retrieve list length
        max_row = len(system_output_list)

        # Parallel Loop
        row = 0
        while row < max_row:  # While loop to accommodate changes (will transfer results to separate lists for checking)
            # Per entry
            # print(system_output_list[row])
            # print(gold_standard_list[row])

            # Check if comparing the same sentence
            if system_output_list[row][0] == gold_standard_list[row][0]:
                sentence_number = system_output_list[row][0]
                system_output_list[row].pop(0)  # Remove from list then start comparing
                gold_standard_list[row].pop(0)

                if not len(system_output_list[row]) == 0:
                    system_extractions += len(system_output_list[row])  # Record extraction counts
                if not len(gold_standard_list[row]) == 0:
                    gold_standard_extractions += len(gold_standard_list[row])

                # Loop through the contents
                system_column = 0
                while system_column < len(system_output_list[row]):
                    system_phrase = system_output_list[row][system_column]  # Holder for the system's output phrase
                    system_phrase_split = system_phrase.split()  # Holder for selecting first and last word

                    gold_standard_column = 0
                    evaluated = False
                    while gold_standard_column < len(gold_standard_list[row]) and not evaluated:
                        gold_standard_phrase = gold_standard_list[row][gold_standard_column]  # Holder for gold standard

                        # Compare
                        # print('Comparing:', system_phrase, '/', gold_standard_phrase)

                        if system_phrase.casefold() == gold_standard_phrase.casefold():  # Exact match
                            list_entry = str(sentence_number) + ' / ' + system_phrase + ' / ' + gold_standard_phrase
                            complete_match_list.append(list_entry)  # Transfer to list
                            true_positive_list.append(list_entry)  # Transfer to list
                            system_output_list[row].pop(system_column)  # Remove in list to keep fp and fn
                            gold_standard_list[row].pop(gold_standard_column)  # Remove in list
                            complete_match += 1  # Add value to cm
                            true_positive += 1  # Add value to tp
                            true_positive_wc += len(system_phrase.split())  # Add value to tp
                            evaluated = True
                            # print('Result: Complete Match\n')
                        elif system_phrase_split[0].casefold() in gold_standard_phrase.casefold() \
                                or system_phrase_split[-1].casefold() in gold_standard_phrase.casefold():
                            # Check for partial matches (check only first/verb and last/noun word if exists in the GS)
                            # Check if over- or under-extracted
                            # print(system_phrase_split[0], gold_standard_phrase,
                            #       system_phrase_split[0].casefold() in gold_standard_phrase.casefold())
                            # print(system_phrase_split[-1], gold_standard_phrase,
                            #       system_phrase_split[-1].casefold() in gold_standard_phrase.casefold())
                            if len(system_phrase) > len(gold_standard_phrase):
                                list_entry = str(sentence_number) + ' / ' + system_phrase + ' / ' + gold_standard_phrase
                                over_extractions_list.append(list_entry)
                                true_positive_list.append(list_entry)
                                system_output_list[row].pop(system_column)  # Remove in list
                                gold_standard_list[row].pop(gold_standard_column)  # Remove in list
                                over_extractions += 1  # Add value to over-extraction
                            elif len(system_phrase) < len(gold_standard_phrase):
                                list_entry = str(sentence_number) + ' / ' + system_phrase + ' / ' + gold_standard_phrase
                                under_extractions_list.append(list_entry)
                                true_positive_list.append(list_entry)
                                system_output_list[row].pop(system_column)  # Remove in list
                                gold_standard_list[row].pop(gold_standard_column)  # Remove in list
                                under_extractions += 1  # Add value to under-extraction
                            else:
                                # If equal, overlapping
                                list_entry = str(sentence_number) + ' / ' + system_phrase + ' / ' + gold_standard_phrase
                                overlapping_extractions_list.append(list_entry)
                                system_output_list[row].pop(system_column)  # Remove in list
                                gold_standard_list[row].pop(gold_standard_column)  # Remove in list
                                overlapping_extractions += 1  # Add value to overlapping_extractions
                            true_positive += 1  # Add value to tp (partial tp?)
                            # TODO: MIGHT NEED TO SEPARATE PARTIAL / MIGHT BE GOLD_STANDARD_PHRASE
                            true_positive_wc += len(gold_standard_phrase.split())
                            evaluated = True
                            # print('Result: Partial Match\n')

                        if not evaluated:
                            gold_standard_column += 1

                    if not evaluated:
                        system_column += 1

                # Check for fp fn tn here, just before proceeding to the next sentence
                # Add complete mismatches
                complete_mismatch += len(system_output_list[row]) + len(gold_standard_list[row])
                list_entry = [str(sentence_number) + ' / ' + x for x in system_output_list[row]]
                complete_mismatch_list.extend(list_entry)
                list_entry = [str(sentence_number) + ' / ' + x for x in gold_standard_list[row]]
                complete_mismatch_list.extend(list_entry)

                # Transfer fp and fn details based on the lists' leftovers
                if system_output_list[row]:  # If list is not empty, transfer contents
                    false_positive += len(system_output_list[row])  # Add counts
                    false_positive_wc += len(str(system_output_list[row]).split())
                    list_entry = [str(sentence_number) + ' / ' + x for x in system_output_list[row]]
                    false_positive_list.extend(list_entry)

                if gold_standard_list[row]:  # If list is not empty, transfer contents
                    false_negative += len(gold_standard_list[row])  # Add counts
                    false_negative_wc += len(str(gold_standard_list[row]).split())
                    list_entry = [str(sentence_number) + ' / ' + x for x in gold_standard_list[row]]
                    false_negative_list.extend(list_entry)

                row += 1
            else:
                print('Sentence Mismatch. Check Documents and Repeat the Test.')

        # Additional Values
        partial_match = over_extractions + under_extractions + overlapping_extractions
        # Complete + Partial Extractions
        correct_extractions = complete_match + partial_match
        # Total Possible Extractions = (System - (System ^ GS)) + (GS - (System ^ GS)) + (System ^ GS)
        # or count whenever an extraction is seen on both System and GS
        # or complete_match + partial_match + complete_mismatch (should be the same)
        # or tp + fp + fn?
        # or basically the count of gold standard?
        # total_possible_extractions = complete_match + partial_match + complete_mismatch
        # *total_possible_extractions = gold_standard_extractions
        # *(system_extractions + gold_standard_extractions) - (complete_match + partial_match)
        total_possible_extractions = (system_extractions + gold_standard_extractions) - (complete_match + partial_match)
        true_negative_wc += word_count - (true_positive_wc + false_positive_wc + false_negative_wc)

        # Metrics
        precision_value = precision(true_positive, false_positive)
        recall_value = recall(true_positive, false_negative)
        accuracy_value = accuracy(true_positive, false_positive, false_negative, true_negative)
        f_measure_value = f_measure(precision_value, recall_value)

        precision_value_wc = precision(true_positive_wc, false_positive_wc)
        recall_value_wc = recall(true_positive_wc, false_negative_wc)
        accuracy_value_wc = accuracy(true_positive_wc, false_positive_wc, false_negative_wc, true_negative_wc)
        f_measure_value_wc = f_measure(precision_value_wc, recall_value_wc)

        print()
        print('EVALUATION RESULTS')
        print('-------------------------------------------------------------------------------------------------------')
        print('Gold Standard Extraction Count:', gold_standard_extractions)
        print('System Extraction Count:', system_extractions)
        print('Total Possible Extraction Count:', total_possible_extractions)
        print('-------------------------------------------------------------------------------------------------------')
        print('Complete Matches:', complete_match, complete_match / total_possible_extractions)
        print('Over-extractions:', over_extractions, over_extractions / total_possible_extractions)
        print('Under-extractions:', under_extractions, under_extractions / total_possible_extractions)
        print('Overlapping-extractions:', overlapping_extractions, overlapping_extractions / total_possible_extractions)
        print('Complete Mismatches:', complete_mismatch, complete_mismatch / total_possible_extractions)
        print('-------------------------------------------------------------------------------------------------------')
        print('True Positive (TP):', true_positive)
        print('False Positive (FP):', false_positive)
        print('False Negative (FN):', false_negative)
        print('True Negative (TN):', true_negative)
        print('-------------------------------------------------------------------------------------------------------')
        print('Precision:', precision_value)
        print('Recall:', recall_value)
        print('Accuracy:', accuracy_value)
        print('F-Measure:', f_measure_value)
        print('-------------------------------------------------------------------------------------------------------')
        print('Word Count:', word_count)
        print('True Positive (TP) Word Count:', true_positive_wc)
        print('False Positive (FP) Word Count:', false_positive_wc)
        print('False Negative (FN) Word Count:', false_negative_wc)
        print('True Negative (TN) Word Count:', true_negative_wc)
        print('-------------------------------------------------------------------------------------------------------')
        print('Precision Word Count:', precision_value_wc)
        print('Recall Word Count:', recall_value_wc)
        print('Accuracy Word Count:', accuracy_value_wc)
        print('F-Measure Word Count:', f_measure_value_wc)
        print('-------------------------------------------------------------------------------------------------------')
        print()
        print('EVALUATION LISTS')
        print('Complete Matches:', complete_match_list)
        print('Over-Extractions:', over_extractions_list)
        print('Under-Extractions:', under_extractions_list)
        print('Overlapping-Extractions:', overlapping_extractions_list)
        print('Complete Mismatches:', complete_mismatch_list)
        print('True Positives:', true_positive_list)
        print('False Positives:', false_positive_list)
        print('False Negatives:', false_negative_list)
        print('True Negatives:', true_negative_list)

    else:
        print('System and Gold Standard Sentence Lengths are NOT EQUAL. Check Documents and Repeat the Test.')


def compare_ie_word_sets(system_output_list, gold_standard_list, word_count):
    """
        Function for evaluating insight word sets. Displays statistics and results of computed standard metrics.

        Args:
            system_output_list (list): a list of strings containing the system extracted (phrases) information.
            gold_standard_list (list): a list of strings containing the gold standard (phrases) information.
    """
    print('Evaluate IE Word Sets')

    # Result Containers
    action_match_list = []
    target_match_list = []
    exact_match_list = []
    partial_match_list = []
    no_match_system_output_list = []
    no_match_gold_standard_list = []
    crossover_match_list = []

    # Preliminary Values
    gold_standard_extractions = len(gold_standard_list)  # Gold Standard Extractions
    system_extractions = len(system_output_list)  # System Total Extractions

    # Insights - Fraction (complete matches / gold standard extractions)
    exact_match = 0  # Exact match, both verb and noun matches with the actual/gold standard
    partial_match = 0  # Verb exactly matches, but noun matches are not exact with the actual/gold standard
    action_match = 0  # Only the action/verb matches with the actual/gold standard
    target_match = 0  # Only the target/noun matches with the actual/gold standard
    no_match_system_output = 0  # Doesn't match with the actual/gold standard
    no_match_gold_standard = 0  # Doesn't match with the system output
    crossover_match = 0  # System action/verb matches the noun of gold standard or vice-versa

    # Insight counts
    true_positive = 0  # System EXTRACTED a text that is an insight / in the Gold Standard
    false_positive = 0  # System EXTRACTED a text that is not an insight / not in the Gold Standard
    false_negative = 0  # System did NOT EXTRACT a text that is an insight / in the Gold Standard
    true_negative = 0  # System did NOT EXTRACT a text that is not an insight / not in the Gold Standard (no value)

    # IE Word Set Comparison
    # print(system_output_list)
    # print(gold_standard_list)

    system_index = 0
    gold_standard_index = 0
    action_added = False
    target_added = False
    stopper = len(gold_standard_list)
    # print(len(system_output_list), len(gold_standard_list))
    while system_output_list:  # While system output list is not empty (will transfer contents like queueing)
        # Compare to Gold Standard
        match_count = 0
        # Check if comparing the same sentence

        # print('Current Sentence No:', system_output_list[system_index], gold_standard_list[gold_standard_index])
        if int(system_output_list[system_index][0]) == int(gold_standard_list[gold_standard_index][0]) and \
                len(system_output_list[system_index]) > 1 and len(gold_standard_list[gold_standard_index]) > 1:
            # Check verb and noun if exact matches of the one in gold standard
            if system_output_list[system_index] == gold_standard_list[gold_standard_index]:
                # print('Exact Match', system_output_list[system_index], gold_standard_list[gold_standard_index])
                exact_match_list.append(system_output_list[system_index])
                system_output_list.pop(system_index)
                gold_standard_list.pop(gold_standard_index)
                # print('STORED-EM1', len(system_output_list), len(gold_standard_list), len(exact_match_list),
                #       len(action_match_list), len(target_match_list), len(crossover_match_list),
                #       len(no_match_system_output_list), len(no_match_gold_standard_list))
            else:
                searching = True  # Toggle if still searching
                while searching:
                    # print(system_index, gold_standard_index)
                    if int(system_output_list[system_index][0]) == int(gold_standard_list[gold_standard_index][0]):
                        # Check verb/noun if partial match
                        # print('Comparing:', system_output_list[system_index][1],
                        #       gold_standard_list[gold_standard_index][1])
                        if action_added and gold_standard_index > 0:
                            action_added = True
                        else:
                            action_added = False  # While action/verb hasn't been added yet
                        if target_added and gold_standard_index > 0:
                            target_added = True
                        else:
                            target_added = False

                        # Verb Matches
                        if system_output_list[system_index][1].casefold() == \
                                gold_standard_list[gold_standard_index][1].casefold():  # Verb check
                            # print('Verb Match', system_output_list[system_index][1].casefold(),
                            #       gold_standard_list[gold_standard_index][1].casefold())
                            match_count += 1
                            action_added = True
                            append_string = str(system_output_list[system_index]) + " / " + \
                                            str(gold_standard_list[gold_standard_index])
                            action_match_list.append(append_string)
                        # else:
                        #     # Multiple words in verb
                        #     tokens_system = system_output_list[system_index][1].split()  # Transform into tokens
                        #     tokens_gold_standard = gold_standard_list[gold_standard_index][1].split()
                        #     # Per word check if it is in the gold standard list of tokens
                        #     for token in tokens_system:
                        #         if token.casefold() in tokens_gold_standard:  # Verb check
                        #             print('Verb Match', system_output_list[system_index][1].casefold(),
                        #                   gold_standard_list[gold_standard_index][1].casefold())
                        #             action_match += 1
                        #             action_added = True
                        #             action_match_list.append(system_output_list[system_index])
                        #             break  # Stop loop if a word has been found

                        # Noun Matches
                        for current in system_output_list[system_index][2:]:  # Loop through every noun
                            gold_standard_noun_list = gold_standard_list[gold_standard_index][2:]
                            if current.casefold() in gold_standard_noun_list:
                                match_count += 1
                                if not system_output_list[system_index] in target_match_list:
                                    # print('Target Match', system_output_list[system_index],
                                    #       gold_standard_list[gold_standard_index])
                                    target_added = True
                                    append_string = str(system_output_list[system_index]) + " / " + \
                                                    str(gold_standard_list[gold_standard_index])
                                    target_match_list.append(append_string)
                                    break  # Stop loop if one word matched

                        # print('Match count compare:', match_count, (len(gold_standard_list[gold_standard_index]) - 1))

                        if match_count == len(gold_standard_list[gold_standard_index]) - 1:  # Complete match recording
                            # print('Exact Match 2', system_output_list[system_index],
                            #       gold_standard_list[gold_standard_index])
                            exact_match_list.append(system_output_list[system_index])
                            if action_added:
                                action_match_list.pop(-1)  # Pop recently added
                                action_added = False
                            if target_added:
                                target_match_list.pop(-1)
                                target_added = False
                            system_output_list.pop(system_index)
                            gold_standard_list.pop(gold_standard_index)
                            # print('STORED-EM2', len(system_output_list), len(gold_standard_list), len(exact_match_list),
                            #       len(action_match_list), len(target_match_list), len(crossover_match_list),
                            #       len(no_match_system_output_list), len(no_match_gold_standard_list))
                            searching = False
                        elif action_added or target_added:
                            if action_added and target_added:
                                # choose only one to store, either action_match or target_match
                                # Can make another variable but so far placed to action_match
                                # TODO: If going to add another variable
                                partial_match_list.append(action_match_list.pop(-1))
                                target_match_list.pop(-1)
                                # print('STORED-NEM', len(partial_match_list))

                            system_output_list.pop(system_index)
                            gold_standard_list.pop(gold_standard_index)
                            # print('STORED-AM/TM', len(system_output_list), len(gold_standard_list), len(exact_match_list),
                            #       len(action_match_list), len(target_match_list), len(crossover_match_list),
                            #       len(no_match_system_output_list), len(no_match_gold_standard_list))
                            action_added = False
                            target_added = False
                            searching = False
                        else:  # match_count < len or == 0
                            # print('Check Next GS')
                            # print(system_output_list[0], gold_standard_index, gold_standard_list[0], gold_standard_list[1])
                            # gold_standard_index_max = len(gold_standard_list)
                            # print(gold_standard_list[gold_standard_index], stopper)
                            # print(gold_standard_list[gold_standard_index] == stopper)
                            # if gold_standard_list[gold_standard_index] == stopper:
                            # #     # Last sentences to be compared doesn't match, throw both on their no_match_list
                            #     print('No Match (for SYS)', system_output_list[system_index])
                            #     no_match_system_output += 1
                            #     no_match_system_output_list.append(system_output_list[system_index])
                            #     system_output_list.pop(0)
                            #     no_match_gold_standard += 1
                            #     no_match_gold_standard_list.append(gold_standard_list[gold_standard_index])
                            #     gold_standard_list.pop(0)
                            #     gold_standard_index = 0
                            #     searching = False
                            gold_standard_index += 1  # Check for the next gold standard insight
                            match_count = 0

                            if len(gold_standard_list) == 1:  # If no more entries after
                                # print('No Match (for SYS)', system_output_list[system_index])
                                no_match_system_output_list.append(system_output_list[system_index])
                                system_output_list.pop(system_index)
                                # print('STORED-NMS1', len(system_output_list), len(gold_standard_list), len(exact_match_list),
                                #       len(action_match_list), len(target_match_list), len(crossover_match_list),
                                #       len(no_match_system_output_list), len(no_match_gold_standard_list))
                                gold_standard_index = 0
                                searching = False

                    else:
                        if not action_added and not target_added:
                            # print('No Match (for SYS2)', system_output_list[system_index])
                            no_match_system_output_list.append(system_output_list[system_index])
                        system_output_list.pop(system_index)
                        # print('STORED-NMS2', len(system_output_list), len(gold_standard_list), len(exact_match_list),
                        #       len(action_match_list), len(target_match_list), len(crossover_match_list),
                        #       len(no_match_system_output_list), len(no_match_gold_standard_list))
                        gold_standard_index = 0
                        searching = False

        elif int(system_output_list[system_index][0]) < int(gold_standard_list[gold_standard_index][0]) or \
                len(gold_standard_list[gold_standard_index]) == 1:  # No insight in gold standard
            if len(gold_standard_list[gold_standard_index]) == 1:
                gold_standard_list.pop(gold_standard_index)
                # print('STORED-NMGS1', len(system_output_list), len(gold_standard_list), len(exact_match_list),
                #       len(action_match_list), len(target_match_list), len(crossover_match_list),
                #       len(no_match_system_output_list), len(no_match_gold_standard_list))
            else:
                # print('No Match (SYS)', system_output_list[system_index])
                no_match_system_output_list.append(system_output_list[system_index])
                system_output_list.pop(system_index)
                # print('STORED-NMS3', len(system_output_list), len(gold_standard_list), len(exact_match_list),
                #       len(action_match_list), len(target_match_list), len(crossover_match_list),
                #       len(no_match_system_output_list), len(no_match_gold_standard_list))
        elif int(system_output_list[system_index][0]) > int(gold_standard_list[gold_standard_index][0]) or \
                len(system_output_list[system_index]) == 1:  # No extracted output
            if len(system_output_list[system_index]) == 1:
                system_output_list.pop(system_index)
                # print('STORED-NMS4', len(system_output_list), len(gold_standard_list), len(exact_match_list),
                #       len(action_match_list), len(target_match_list), len(crossover_match_list),
                #       len(no_match_system_output_list), len(no_match_gold_standard_list))
            else:
                # print('No Match (GS2)', gold_standard_list[gold_standard_index])
                no_match_gold_standard_list.append(gold_standard_list[gold_standard_index])
                gold_standard_list.pop(gold_standard_index)
                # print('STORED-NMGS2', len(system_output_list), len(gold_standard_list), len(exact_match_list),
                #       len(action_match_list), len(target_match_list), len(crossover_match_list),
                #       len(no_match_system_output_list), len(no_match_gold_standard_list))

    # Place counts
    exact_match = len(exact_match_list)
    partial_match = len(partial_match_list)
    action_match = len(action_match_list)
    target_match = len(target_match_list)

    # print()
    # print('Crossover Match Check')
    # print(no_match_system_output_list)
    # print(gold_standard_list)

    # Crossover Matches
    if gold_standard_list:  # If there's still contents inside this, flush into no match gold standard list
        no_match_gold_standard_list.extend(gold_standard_list)

    # print('STORED-NMGS3', len(system_output_list), len(gold_standard_list), len(exact_match_list),
    #       len(action_match_list), len(target_match_list), len(crossover_match_list),
    #       len(no_match_system_output_list), len(no_match_gold_standard_list))

    index_system = 0
    index_gold_standard = 0
    while index_system < len(no_match_system_output_list):
        match = False
        # print('1', len(crossover_match_list) / 2)
        # print(index_system, len(no_match_system_output_list), index_gold_standard, len(no_match_gold_standard_list))
        # print('Comparing', no_match_system_output_list[index_system], no_match_gold_standard_list[index_gold_standard])
        # If comparing the same sentence number, and both lists have elements greater than 1 (other than sentence no.)
        if int(no_match_system_output_list[index_system][0]) == \
            int(no_match_gold_standard_list[index_gold_standard][0]) \
                and len(no_match_system_output_list[index_system]) > 1 \
                and len(no_match_gold_standard_list[index_gold_standard]) > 1:
            # Check if an element in one list can be found on the other
            if no_match_system_output_list[index_system][1] in no_match_gold_standard_list[index_gold_standard][2:] or \
                    no_match_gold_standard_list[index_gold_standard][1] in \
                    no_match_system_output_list[index_system][2:]:
                # no_match_system_output_list[index_system][1] in no_match_gold_standard_list[index_gold_standard][1]:
                # print('Crossover Match', no_match_system_output_list[index_system],
                #       no_match_gold_standard_list[index_gold_standard])
                append_string = str(no_match_system_output_list[index_system]) + " / " + \
                                str(no_match_gold_standard_list[index_gold_standard])
                crossover_match_list.append(append_string)
                # print('2', len(crossover_match_list) / 2)
                no_match_system_output_list.pop(index_system)
                no_match_gold_standard_list.pop(index_gold_standard)
                # print('STORED-COM1', len(system_output_list), len(gold_standard_list), len(exact_match_list),
                #       len(action_match_list), len(target_match_list), len(crossover_match_list),
                #       len(no_match_system_output_list), len(no_match_gold_standard_list))
                index_system -= 1
                index_gold_standard = 0
                match = True
            else:  # Try for multiple words comparison
                combined_system = [words for tokens in no_match_system_output_list[index_system][1:]
                                   for words in tokens.split()]  # Transform list into tokens
                combined_gold_standard = [words for tokens in no_match_gold_standard_list[index_gold_standard][1:]
                                          for words in tokens.split()]  # Transform list into tokens
                # Per word check if it is in the gold standard list of tokens
                for word in combined_system:
                    if word.casefold() in combined_gold_standard:
                        # print('Crossover Match', no_match_system_output_list[index_system],
                        #        no_match_gold_standard_list[index_gold_standard])
                        append_string = str(no_match_system_output_list[index_system]) + " / " + \
                                        str(no_match_gold_standard_list[index_gold_standard])
                        crossover_match_list.append(append_string)
                        # print('3', len(crossover_match_list) / 2)
                        no_match_system_output_list.pop(index_system)
                        no_match_gold_standard_list.pop(index_gold_standard)
                        # print('STORED-COM2', len(system_output_list), len(gold_standard_list), len(exact_match_list),
                        #       len(action_match_list), len(target_match_list), len(crossover_match_list),
                        #       len(no_match_system_output_list), len(no_match_gold_standard_list))
                        index_system -= 1
                        index_gold_standard = 0
                        match = True
                        break  # Stop loop if a word has been found

            if (index_gold_standard + 1) < len(no_match_gold_standard_list) and not match:
                index_gold_standard += 1
            else:
                index_system += 1
        # If system output has lower sentence no., just skip it. If gold standard has lower sentence no., just skip it.
        elif int(no_match_system_output_list[index_system][0]) < \
                int(no_match_gold_standard_list[index_gold_standard][0]) or \
                len(no_match_gold_standard_list[index_gold_standard]) == 1:
            index_system += 1
            # print(no_match_system_output_list)
        elif int(no_match_system_output_list[index_system][0]) > \
                int(no_match_gold_standard_list[index_gold_standard][0]) or \
                len(no_match_system_output_list[index_system]) == 1:
            index_gold_standard += 1
    # print(crossover_match / 2, len(crossover_match_list) / 2)

    crossover_match = len(crossover_match_list)

    # Remove single element in No Matches
    counter = 0
    while counter < len(no_match_system_output_list):
        # print(no_match_system_output_list[counter], len(no_match_system_output_list[counter]) == 1,
        #       not no_match_system_output_list[counter])
        if len(no_match_system_output_list[counter]) == 1 or not no_match_system_output_list[counter]:
            no_match_system_output_list.pop(counter)
            counter -= 1
        counter += 1

    counter = 0
    while counter < len(no_match_gold_standard_list):
        # print(no_match_gold_standard_list[counter], len(no_match_gold_standard_list[counter]) == 1,
        #       not no_match_gold_standard_list[counter])
        if len(no_match_gold_standard_list[counter]) == 1 or not no_match_gold_standard_list[counter]:
            no_match_gold_standard_list.pop(counter)
            counter -= 1
        counter += 1

    # Update no match system output
    no_match_system_output = len(no_match_system_output_list)
    no_match_gold_standard = len(no_match_gold_standard_list)

    # print('STORED-LAST', len(system_output_list), len(gold_standard_list), len(exact_match_list),
    #       len(action_match_list), len(target_match_list), len(crossover_match_list),
    #       len(no_match_system_output_list), len(no_match_gold_standard_list))

    # Additional Values
    partial_matches = action_match + target_match + crossover_match + partial_match
    correct_extractions = exact_match + partial_matches
    # *total_possible_extractions = gold_standard_extractions
    # *(system_extractions + gold_standard_extractions) - (complete_match + partial_match)
    total_possible_extractions = (system_extractions + gold_standard_extractions) - correct_extractions
    total_possible_extractions = gold_standard_extractions

    true_positive = correct_extractions  # System EXTRACTED a text that is an insight / in the Gold Standard
    false_positive = no_match_system_output  # System EXTRACTED a text that is not an insight / not in the Gold Standard
    false_negative = no_match_gold_standard  # System did NOT EXTRACT a text that is an insight / in the Gold Standard

    # Metrics
    precision_value = precision(true_positive, false_positive)
    recall_value = recall(true_positive, false_negative)
    accuracy_value = accuracy(true_positive, false_positive, false_negative, true_negative)
    f_measure_value = f_measure(precision_value, recall_value)

    print()
    print('EVALUATION RESULTS')
    print('-------------------------------------------------------------------------------------------------------')
    print('Gold Standard Extraction Count:', gold_standard_extractions)
    print('System Extraction Count:', system_extractions)
    print('Total Possible Extraction Count:', total_possible_extractions)
    print('-------------------------------------------------------------------------------------------------------')
    print('Exact Matches:', exact_match, exact_match / total_possible_extractions)
    print('Partial Matches:', partial_match, partial_match / total_possible_extractions)
    print('Action/Verb Matches:', action_match, action_match / total_possible_extractions)
    print('Target/Noun Matches:', target_match, target_match / total_possible_extractions)
    print('Crossover Matches:', crossover_match, crossover_match / total_possible_extractions)  # / 2 for pairs
    print('No Matches (System Output on Gold Standard):', no_match_system_output, no_match_system_output /
          total_possible_extractions)
    print('No Matches (Gold Standard on System Output):', no_match_gold_standard, no_match_gold_standard /
          total_possible_extractions)
    print('-------------------------------------------------------------------------------------------------------')
    print('True Positive (TP):', true_positive)
    print('False Positive (FP):', false_positive)
    print('False Negative (FN):', false_negative)
    print('True Negative (TN):', true_negative)
    print('-------------------------------------------------------------------------------------------------------')
    print('Precision:', precision_value)
    print('Recall:', recall_value)
    print('Accuracy:', accuracy_value)
    print('F-Measure:', f_measure_value)
    print('-------------------------------------------------------------------------------------------------------')
    print()
    print('EVALUATION LISTS')
    print('Exact Matches:', exact_match_list)
    print('Partial Matches:', partial_match_list)
    print('Action/Verb Matches:', action_match_list)
    print('Target/Noun Matches:', target_match_list)
    print('Crossover Matches:', crossover_match_list)
    print('No Matches (System Output on Gold Standard):', no_match_system_output_list)
    print('No Matches (Gold Standard on System Output):', no_match_gold_standard_list)


# RUN EVALUATION
# Transform document insights into lists
candidate_phrase_list, candidate_word_set_list, gold_standard_phrase_list, gold_standard_word_set_list, total_words = \
    retrieve_text(system_output_filename, gold_standard_filename)

print(len(candidate_phrase_list), len(gold_standard_phrase_list))

print()

# Compare extracted phrases to know the performance in extracting insights
compare_ie_phrases(candidate_phrase_list, gold_standard_phrase_list, total_words)

print()

# Compare extracted word sets to know the performance in extracting verbs and nouns
compare_ie_word_sets(candidate_word_set_list, gold_standard_word_set_list, total_words)

# COMPARISON TEST
# print(cluster.string_similarity_dice('barangay', 'xbarangay'))
# print(cluster.string_similarity_dice('barangay', 'baraxngay'))
# print(cluster.string_similarity_dice('barangay', 'barangayx'))
# print(cluster.string_similarity_dice('barangay', 'arangay'))
# print(cluster.string_similarity_dice('barangay', 'barngay'))
# print(cluster.string_similarity_dice('barangay', 'baranga'))
# print()
# print(cluster.string_similarity_dice('mag', 'xag'))
# print(cluster.string_similarity_dice('magi', 'xagi'))
# print(cluster.string_similarity_dice('magik', 'xagik'))
# print(cluster.string_similarity_dice('magiko', 'xagiko'))
# print(cluster.string_similarity_dice('magikot', 'xagikot'))
# print()
# print(cluster.string_similarity_dice('mag', 'mxg'))
# print(cluster.string_similarity_dice('magi', 'mxgi'))
# print(cluster.string_similarity_dice('magik', 'mxgik'))
# print(cluster.string_similarity_dice('magiko', 'mxgiko'))
# print(cluster.string_similarity_dice('magikot', 'mxgikot'))
# print()
# print(cluster.string_similarity_dice('mag', 'max'))
# print(cluster.string_similarity_dice('magi', 'magx'))
# print(cluster.string_similarity_dice('magik', 'magix'))
# print(cluster.string_similarity_dice('magiko', 'magikx'))
# print(cluster.string_similarity_dice('magikot', 'magikox'))
# print(cluster.string_similarity_dice('magikoti', 'magikotx'))
# print(cluster.string_similarity_dice('magikotik', 'magikotix'))
# print(cluster.string_similarity_dice('magikotiko', 'magikotikx'))
# print(cluster.string_similarity_dice('magikotikot', 'magikotikox'))
# print(cluster.string_similarity_dice('magikotikott', 'magikotikotx'))
# print(cluster.string_similarity_dice('magikotikottt', 'magikotikottx'))
# print(cluster.string_similarity_word2vec('gamit', 'bagay'))