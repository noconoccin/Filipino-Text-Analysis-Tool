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
# SØRENSEN-DICE AND WORD EMBEDDINGS CLUSTERING
# Groups words based on string or semantic similarity.
# > Sørensen-Dice Coefficient: https://esajournals.onlinelibrary.wiley.com/doi/abs/10.2307/1932409
#   > Library [strsim]: https://github.com/luozhouyang/python-string-similarity
# > Word2Vec: https://arxiv.org/pdf/1301.3781.pdf
# > FastText: https://arxiv.org/pdf/1607.04606.pdf
#   > Library [gensim]: https://radimrehurek.com/gensim/
#   > Pre-trained Tagalog Models for Word2Vec and FastText (Wikipedia): https://github.com/Kyubyong/wordvectors
#       > 'model/tl_word2vec/tl.bin
#       > 'model/tl_fasttext/tl.bin
#       > There's vocabulary Limit on Word2Vec
#   > Pre-trained Tagalog Model for FastText (CommonCrawl and Wikipedia): https://fasttext.cc/docs/en/crawl-vectors.html
#       > 'model/cc_tl_300_fasttext/cc.tl.300.bin'
#       > Processing time is a lot slower, high memory usage, and similarity scores aren't ideal
#   > Pre-trained English Model for Word2Vec (Google News): https://github.com/3Top/word2vec-api
#       > 'model/en_word2vec/GoogleNews-vectors-negative300.bin'
#       > Google News has largest vocabulary (3M)
#       > Processing time is a lot slower, high memory and disk usage
#   > Pre-trained English Model for FastText (Wikipedia News): https://fasttext.cc/docs/en/english-vectors.html
#       > 'model/en_fasttext/wiki-news-300d-1M-subword.vec'
#       > Wikipedia 2017, UMBC webbase corpus and statmt.org news
#       > Processing time is a lot slower, high memory and disk usage
#   > FastText Implementation with Target Clustering is slow because it was able to cluster a lot of nouns.
#   > Normalized texts are faster since they get to be clustered more than others (?)
#   > English Word Embeddings is not appropriate for implementation on the current machine. Despite this, Tagalog Word
#     Embeddings was able to join some English related words.
###################################################################################

import warnings
import data_utils
from collections import OrderedDict
from similarity.sorensen_dice import SorensenDice
from gensim.models import Word2Vec
from gensim.models.wrappers import FastText
from gensim.models import KeyedVectors
# import gensim.downloader as api


def string_similarity_fasttext(string1, string2):
    """
    Function for computing the FastText's vector similarity (how close, high is better) between two strings.

    Args:
        string1 (str): The string to be compared to.
        string2 (str): The string to be compared to.

    Returns:
        similarity: the resulting score computed from 'model.similarity(string1, string2)' function.
    """
    model = FastText.load_fasttext_format('model/tl_fasttext/tl.bin')
    return model.similarity(string1, string2)


def string_distance_fasttext(string1, string2):
    """
    Function for computing the FastText's vector distance (how far, low is better) between two strings.

    Args:
        string1 (str): The string to be compared to.
        string2 (str): The string to be compared to.

    Returns:
        distance: the resulting score computed from '1 - model.similarity(string1, string2)' function.
    """
    model = FastText.load_fasttext_format('model/tl_fasttext/tl.bin')
    return 1 - model.similarity(string1, string2)


def string_similarity_word2vec(string1, string2):
    """
    Function for computing the Word2Vec's vector similarity (how close, high is better) between two strings.

    Args:
        string1 (str): The string to be compared to.
        string2 (str): The string to be compared to.

    Returns:
        similarity: the resulting score computed from 'model.similarity(string1, string2)' function.
    """
    warnings.simplefilter('ignore', UserWarning)  # Ignore the C Extension warning of Gensim
    model = Word2Vec.load('model/tl_word2vec/tl.bin')
    return model.similarity(string1, string2)


def string_distance_word2vec(string1, string2):
    """
    Function for computing the Word2Vec's vector distance (how far, low is better) between two strings.

    Args:
        string1 (str): The string to be compared to.
        string2 (str): The string to be compared to.

    Returns:
        distance: the resulting score computed from '1 - model.similarity(string1, string2)' function.
    """
    warnings.simplefilter('ignore', UserWarning)  # Ignore the C Extension warning of Gensim
    model = Word2Vec.load('model/tl_word2vec/tl.bin')
    return 1 - model.similarity(string1, string2)


def string_similarity_dice(string1, string2):
    """
    Function for computing the Dice's coefficient similarity (how close, high is better) between two strings.

    Args:
        string1 (str): The string to be compared to.
        string2 (str): The string to be compared to.

    Returns:
        similarity: the resulting score computed from 'dice.similarity(string1, string2)' function.
    """
    similarity = 0.0
    dice = SorensenDice()  # 3-gram is default; Try 2-gram (to increase filtering and threshold 0.5)
    try:
        similarity = dice.similarity(string1, string2)
    except ZeroDivisionError as error:  # For words under 3 characters, result is 0.0
        print('Zero Division Error for: ' + string1 + ' ' + string2)

    return similarity


def string_distance_dice(string1, string2):
    """
    Function for computing the Dice's coefficient distance (how far, low is better) between two strings.

    Args:
        string1 (str): The string to be compared to.
        string2 (str): The string to be compared to.

    Returns:
        distance: the resulting score computed from 'dice.distance(string1, string2)' function.
    """
    distance = 1.0
    dice = SorensenDice()  # 3-gram is default; Try 2-gram (to increase filtering and threshold 0.5)
    try:
        distance = dice.distance(string1, string2)
    except ZeroDivisionError as error:  # For words under 3 characters, result is 0.0
        print('Zero Division Error for: ' + string1 + ' ' + string2)

    return distance


def collect_all_insights_from_object(malasakit_response_list, insights_type):
    """
    Function for retrieving all insights in the MalasakitResponse object and storing them in one list.

    Args:
        malasakit_response_list (list): The list containing MalasakitResponse objects.
        insights_type (str): A character/string indicating the type of insights to be collected. 'p' for phrases and 'w'
                            for word sets.

    Returns:
        insights_list: a list containing all of the insights taken from the object list.
    """
    insights_list = []

    for malasakit_response in malasakit_response_list:
        if malasakit_response:  # If not empty, add to list. Otherwise, ignore those without insights
            if insights_type == 'p':
                insights_list.append(malasakit_response.insights_phrase)
            elif insights_type == 'w':
                insights_list += malasakit_response.insights_words  # Did not use append to flatten list while joining

    return insights_list


def merge_cluster_insights(cluster, clustering_technique):
    """
    Function for merging the insights in one cluster into a single line. For target (noun) words, similar ones are
    grouped together based on the clustering technique given - which is same to the technique indicated in the outer
    function cluster_information()). Notation for clustering is: word1 (word2, ..., wordN).

    Args:
        cluster (list): The list containing the current cluster.
        clustering_technique (str): Select a clustering technique from the following: 'dice', 'word2vec', or 'fasttext'.

    Returns:
        cluster: a list containing the modified (merged) words in the cluster's insights.
    """
    while len(cluster) != 1:  # Continue as long as contents of cluster is not 1
        cluster[0][0] = str(cluster[0][0]) + "|" + str(cluster[1][0])  # Append response_ids
        cluster[0][1] = str(cluster[0][1]) + ", " + str(cluster[1][1])  # Append proposed action / verb
        cluster[1].pop(0)  # Remove response_id
        cluster[1].pop(0)  # Remove proposed action
        cluster[0].extend(cluster[1])  # Append the rest
        del cluster[1]  # Delete since all are appended already

    # Filter duplicate target/s or noun/s
    sub_cluster_a = cluster[0][:2]  # Slice first part: index 0-1
    sub_cluster_b = cluster[0][2:]  # Slice second part: index 2-onwards
    sub_cluster_b = remove_duplicate(sub_cluster_b)  # Remove duplicate in second part
    cluster[0] = sub_cluster_a + sub_cluster_b  # Combine two parts

    # Filter duplicate response ids
    ids = str(cluster[0][0]).split("|")  # Put unmerged ids in a list
    ids = remove_duplicate(ids)  # Filter duplicates
    ids.sort(key=int)  # Sort the id numbers in ascending order
    filtered_string = ""
    for element in ids:  # Merge filtered ids
        filtered_string += element + "|"
    filtered_string = filtered_string[:-1]  # Remove extra character at the end
    cluster[0][0] = filtered_string  # Replace old with new

    # Filter duplicate proposed actions / verbs (case-insensitive)
    actions = str(cluster[0][1]).split(",")  # Put unmerged action / verbs in a list
    actions = remove_duplicate(actions)  # Filter duplicates
    filtered_string = ""
    for element in actions:  # Merge filtered actions / verbs
        filtered_string += element + ","
    filtered_string = filtered_string[:-1]  # Remove extra character at the end
    cluster[0][1] = filtered_string  # Replace old with new

    # Append all target/s or noun/s
    counter = 3
    while counter < len(cluster[0]):
        cluster[0][2] += ", " + cluster[0][3]  # Join two strings
        cluster[0].pop(3)  # Remove string that has been attached

    # Cluster target/nouns using clustering technique (join using word1 (word2, ..., wordN) notation)
    # Note: Can be modified to perform lexicalization (one word to represent)
    target_word_list = cluster[0][2].split(', ')  # Tokenize
    # print('TWL:', target_word_list)
    # (1) TWL = [a, a, a1, a2, b, c]
    new_target_word_list = cluster_words(target_word_list, clustering_technique)  # Cluster
    # print('NTWL:', new_target_word_list)
    # (2) NTWL = [a (a1, a2), b, c]
    new_target_string = ''
    for token in new_target_word_list:  # Join the tokens
        new_target_string += token + ', '
    new_target_string = new_target_string[:-2]  # Remove extra ', ' characters at the end
    # (3) NTS = 'a (a1, a2), b, c'
    cluster[0][2] = new_target_string  # Update

    return cluster


def remove_duplicate(cluster_zero):
    """
    Function for removing duplicate strings.

    Args:
        cluster_zero (list): The list containing the current cluster.

    Returns:
        filtered_cluster_zero: a list containing the modified (filtered-off duplicates) words in the cluster, resulted
                                from the 'list(OrderedDict.fromkeys(cluster_zero))' function.
    """
    return list(OrderedDict.fromkeys(cluster_zero))


def cluster_words(target_word_list, clustering_technique):

    """
    Function for clustering words (intended for target/noun words). Given a list it will join similar words using the
    word1 (word2, ..., wordN) notation.

    Args:
        target_word_list (list): The list containing the words to be clustered.
        clustering_technique (str): Select a clustering technique from the following: 'dice', 'word2vec', or 'fasttext'.

    Returns:
         new_target_word_list:  a list containing the clustered and formatted words.
    """
    new_target_word_list = []  # dummy
    similarity = 0.0  # Variable for the similarity score of two strings
    threshold = 0.5  # Value for string similarity clustering threshold (0.5)
    deletion_occurred = False  # Used to correct index pointer after modifying/deleting a list

    # Load word embeddings model and set threshold
    if clustering_technique == 'word2vec':
        # print('Running Word2Vec for Target')
        warnings.simplefilter('ignore', UserWarning)  # Ignore the C Extension warning of Gensim
        model = Word2Vec.load('model/tl_word2vec/tl.bin')
        # threshold = 0.5  # Value for semantic clustering threshold
    elif clustering_technique == 'fasttext':
        # print('Running FastText for Target')
        model = FastText.load_fasttext_format('model/tl_fasttext/tl.bin')
        # threshold = 0.6  # Value for semantic clustering threshold

    while target_word_list:
        first_string = target_word_list[0].lower()  # Get and convert target / noun into lowercase
        cluster_string = first_string  # Store as current cluster (word only, format will change after finding similar)
        target_word_list.pop(0)  # Remove the current token from target_list
        index_ctr = 0  # Index tracker for accurate removal/deletion of matches in list
        first_join = True

        while index_ctr < len(target_word_list):
            second_string = target_word_list[index_ctr].lower()  # Get and convert word to lowercase for comparison

            # Choose how to cluster based on selected technique
            if clustering_technique == 'dice':
                similarity = string_similarity_dice(first_string, second_string)  # Computes the similarity of 2 strings
            elif clustering_technique == 'word2vec':
                # For those that are not seen by word2vec. Did not use api function to string_similarity_word2vec
                # to prevent repeating load of model per iteration
                try:
                    similarity = model.similarity(first_string, second_string)
                except KeyError:
                    similarity = 0.0  # No operation done, so set similarity to 0
                    # print('{} or {} not found'.format(first_string, second_string))
            elif clustering_technique == 'fasttext':
                try:
                    similarity = model.similarity(first_string, second_string)
                except KeyError:
                    similarity = 0.0  # No operation done, so set similarity to 0
                    # print('{} or {} not found'.format(first_string, second_string))

            # print(first_string, "and", second_string, "=", similarity)
            if similarity == 1.0 or first_string.casefold() == second_string.casefold():
                target_word_list.pop(index_ctr)  # Remove duplicate word from target_word_list
                deletion_occurred = True
            elif similarity > threshold:
                if first_join:
                    cluster_string += ' (' + second_string  # Append the second string inside the parenthesis
                    first_join = False
                else:
                    cluster_string += ', ' + second_string  # Append the second string beside another similar word
                target_word_list.pop(index_ctr)  # Remove word from target_word_list
                deletion_occurred = True

            if not deletion_occurred:
                index_ctr += 1  # Index increment
            deletion_occurred = False  # Reset variable
        if not first_join:
            cluster_string = cluster_string.strip(', ') + ')'  # Remove extra ', ' at the end and close the parenthesis
        new_target_word_list.append(cluster_string)
        # print('CLUSTER STRING:', cluster_string)
    # print('TARGET_WORD_LIST:', new_target_word_list)

    return new_target_word_list


def cluster_information(malasakit_response_list, clustering_technique):
    """
    Function for clustering text using either Sørensen-Dice Coefficient (String Clustering), Word2Vec, or FastText Word
    Embeddings (Semantic Clustering). Can toggle using "dice", "word2vec", or "fasttext". Returns a list of clusters.

    Args:
        malasakit_response_list (list): The list containing the MalasakitResponse objects.
        clustering_technique (str): Select a clustering technique from the following: 'dice', 'word2vec', or 'fasttext'.

    Returns:
        clusters_list: a list containing the clustered insights.
    """
    clusters_list = []  # List of list of clusters [[cluster1,...], [cluster2,...], ..., [clusterN,...]]
    # insights_list = []  # List of list of insights [[insight1,...], [insight2,...], ..., [insightN,...]]
    similarity = 0.0  # Variable for the similarity score of two strings
    frequency_count = 0  # Counts the number of times an idea has been presented
    threshold = 0.5  # Value for string similarity clustering threshold
    deletion_occurred = False  # Used to correct index pointer after modifying/deleting a list

    # Load word embeddings model and set threshold
    if clustering_technique == 'word2vec':
        # print('Running Word2Vec for Action')
        warnings.simplefilter('ignore', UserWarning)  # Ignore the C Extension warning of Gensim
        model = Word2Vec.load('model/tl_word2vec/tl.bin')
        # threshold = 0.5  # Value for semantic clustering threshold
    elif clustering_technique == 'fasttext':
        # print('Running FastText for Action')
        model = FastText.load_fasttext_format('model/tl_fasttext/tl.bin')
        # threshold = 0.6  # Value for semantic clustering threshold

    insights_list = collect_all_insights_from_object(malasakit_response_list, 'w')
    # print(insights_list)
    while insights_list:  # While insights_list is not empty
        insights_list[0][1] = insights_list[0][1].lower()  # Convert proposed action / verb into lowercase
        first_string = insights_list[0][1]  # Get the proposed action / verb for comparison
        cluster = [insights_list[0]]  # Store as the current cluster = cluster[0]
        # print("Current Cluster: ", cluster)
        # print("First String: ", first_string)
        insights_list.pop(0)  # Remove the current from insights_list
        # print(insights_list)
        # print()
        frequency_count += 1  # Add 1 to frequency count for the cluster to be inserted later on

        index_ctr = 0  # Index tracker for accurate removal/deletion in list
        # print("Precondition: ", index_ctr, "<", len(insights_list))
        while index_ctr < len(insights_list):
            # print("Current Insight: ", insights_list[index_ctr])
            insights_list[index_ctr][1] = insights_list[index_ctr][1].lower()  # Convert to lowercase
            second_string = insights_list[index_ctr][1]  # Get the proposed action / verb for comparison
            # print("Second String: ", second_string)

            # Choose how to cluster based on selected technique
            if clustering_technique == 'dice':
                similarity = string_similarity_dice(first_string, second_string)  # Computes the similarity of 2 strings
            elif clustering_technique == 'word2vec':
                # For those that are not seen by word2vec. Did not use api function to string_similarity_word2vec
                # to prevent repeating load of model per iteration
                try:
                    similarity = model.similarity(first_string, second_string)
                except KeyError:
                    similarity = 0.0  # No operation done, so set similarity to 0
                    # print('{} or {} not found'.format(first_string, second_string))
            elif clustering_technique == 'fasttext':
                try:
                    similarity = model.similarity(first_string, second_string)
                except KeyError:
                    similarity = 0.0  # No operation done, so set similarity to 0

            # print(first_string, "and", second_string, "=", similarity)
            if similarity == 1.0 or first_string.casefold() == second_string.casefold():
                cluster[0][0] = str(cluster[0][0]) + "|" + str(insights_list[index_ctr][0])  # Append response_ids
                # print("Cluster[0][0]:", cluster[0][0])
                insights_list[index_ctr].pop(0)  # Delete response_id of second string
                insights_list[index_ctr].pop(0)  # Delete proposed action / verb of second string (the duplicate)
                cluster[0].extend(insights_list[index_ctr])  # Add what's left: target/s or noun/s
                # print("New Cluster: ", cluster)
                # Remove duplicate target/s or noun/s
                insights_list.pop(index_ctr)  # Remove insight from insights_list
                deletion_occurred = True
                # print("New Insight List: ", insights_list)
                frequency_count += 1
            elif similarity > threshold:
                cluster.append(insights_list[index_ctr])  # Append the whole insight
                # print("New Cluster: ", cluster)
                insights_list.pop(index_ctr)  # Remove insight from insights_list
                deletion_occurred = True
                frequency_count += 1

            if not deletion_occurred:
                index_ctr += 1  # Index increment
            deletion_occurred = False  # Reset variable
            # print("Post-condition: ", index_ctr, "<", len(insights_list))

        # Combine insights under this cluster into one line
        cluster = merge_cluster_insights(cluster, clustering_technique)
        cluster[0].insert(1, frequency_count)  # Insert the frequency in between the response_ids and proposed action
        cluster = [element for insight in cluster for element in insight]  # Flatten list using list comprehension
        clusters_list.append(cluster)  # Add the cluster to clusters_list
        frequency_count = 0  # Reset frequency count

        # print("Clusters List: ", clusters_list)
        # print()

    return clusters_list


# EXPERIMENTAL FUNCTIONS
# Function for clustering text using Word2Vec Word Embeddings (Semantic Clustering). Returns a list of clusters.
# Not used.
def cluster_word2vec(malasakit_response_list):
    print('Running Word2Vec')
    # Load vectors directly from the file
    # model = api.load("glove-twitter-25")  # download the model and return as object ready for use
    # print(model.most_similar("cat"))
    warnings.simplefilter('ignore', UserWarning)  # Ignore the C Extension warning of Gensim
    model = Word2Vec.load('model/tl_word2vec/tl.bin')
    word = 'kumain'  # kumain not found
    word_2 = 'kainin'
    try:
        print(model.similarity(word, word_2))
        print(model.most_similar(word))
        print(model.most_similar(word_2))
    except KeyError:
        print(word, "not found! ")


# Function for clustering text using FastText Word Embeddings (Semantic Clustering). Returns a list of clusters.
# Not used.
def test_fasttext(file_name_model):
    print('Running FastText')
    # model = FastText.load_fasttext_format('model/cc_tl_300_fasttext/cc.tl.300.bin')
    # model = FastText.load_fasttext_format('model/tl_fasttext/tl.bin')
    # model = FastText.load_fasttext_format(file_name_model)
    # Use this for Wiki News
    model = KeyedVectors.load_word2vec_format(file_name_model, binary=False)
    # print(model.similarity('linisin', 'maglinis'))
    # print(model.similarity('malinis', 'maglinis'))
    # print(model.similarity('linisin', 'malinis'))
    # print(model.most_similar('linisin'))

    print(model.similarity('prepare', 'preparing'))
    print(model.similarity('perform', 'conduct'))
    print(model.similarity('inform', 'alert'))
    print(model.most_similar('prepare'))


def train_word2vec(file_name_input, file_name_model):
    corpus = data_utils.text_to_list(file_name_input)
    # print(corpus)
    model = Word2Vec(corpus)
    model.save(file_name_model)


def test_word2vec(file_name_model):
    model = Word2Vec.load(file_name_model)
    # Use this for Google News
    # model = KeyedVectors.load_word2vec_format(file_name_model, binary=True)
    # print(model.most_similar('kanal'))
    # print(model.similarity('linisin', 'maglinis'))
    # print(model.wv['linisin'])

    print(model.similarity('prepare', 'preparing'))
    print(model.similarity('perform', 'conduct'))
    print(model.similarity('inform', 'alert'))
    print(model.most_similar('prepare'))


# Self-run functions
# cluster_word2vec(malasakit_response_list=None)
# cluster_fasttext(malasakit_response_list=None)
# train_word2vec('test/train_malasakit_responses.txt', 'model/malasakit/malasakit.txt')
# test_word2vec('model/malasakit/malasakit.txt')
# test_word2vec('model/en_word2vec/GoogleNews-vectors-negative300.bin')
# test_fasttext('model/en_fasttext/wiki-news-300d-1M.vec')

# print("SIMILARITY TEST")
# print(string_similarity_dice('linisin', 'maglinis'), string_similarity_dice('malinis', 'maglinis'),
#       string_similarity_dice('linisin', 'malinis'))
