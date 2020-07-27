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
# INFORMATION ORGANIZATION
# Sets up the initial steps in order to run cluster.py, rank.py, and
# generate.py modules. Choices include:
#   > Organize all entries (all entries will be clustered and ranked based solely
#     on frequency)
#   > Organize by response categories (information will be clustered based on
#     categories and ranked based on frequency)
###################################################################################

import cluster
import rank
import timeit


def organize_sublist(sub_malasakit_response_list_copy, clusters_list, ranked_clusters_list, clustering_technique,
                     current_category, clustering_time, ranking_time):
    """
    Function that organizes the given sublist (current or one category).

    Args:
        sub_malasakit_response_list_copy (list): The list containing a subset of MalasakitResponse objects.
        clusters_list (list): The list of clustered responses.
        ranked_clusters_list (list): The list of clustered and ranked responses.
        clustering_technique (str): Select a clustering technique from the following: 'dice', 'word2vec', or 'fasttext'.
        current_category (str): The label of the current category being processed.
        clustering_time (float): The variable for tracking the execution time of the clustering process.
        ranking_time (float): The variable for tracking the execution time of the ranking process.

    Returns:
        clusters_list: a list containing the clustered responses.
        ranked_clusters_list: a list containing the clustered and ranked responses.
        clustering_time: a float variable for tracking the execution time of the clustering process.
        ranking_time: a float variable for tracking the execution time of the ranking process.
    """
    # Process the sublist
    print(current_category)
    # -- START MODULE --
    start_clustering_time = timeit.default_timer()

    # INFORMATION CLUSTERING
    if clustering_technique == 'dice':
        # SORENSEN-DICE COEFFICIENT CLUSTERING
        sub_clusters_list = cluster.cluster_information(sub_malasakit_response_list_copy, 'dice')
    elif clustering_technique == 'word2vec':
        # WORD EMBEDDINGS CLUSTERING
        sub_clusters_list = cluster.cluster_information(sub_malasakit_response_list_copy, 'word2vec')
    elif clustering_technique == 'fasttext':
        # WORD EMBEDDINGS CLUSTERING
        sub_clusters_list = cluster.cluster_information(sub_malasakit_response_list_copy, 'fasttext')

    clustering_time += (timeit.default_timer() - start_clustering_time)
    # -- END MODULE --

    # -- START MODULE --
    start_ranking_time = timeit.default_timer()

    # INFORMATION RANKING (FREQUENCY)
    sub_ranked_clusters_list = rank.rank_clusters_by_frequency(sub_clusters_list)

    ranking_time += (timeit.default_timer() - start_ranking_time)
    # -- END MODULE --

    # Combine to outer list and insert at index 0 the category (Result Lists)
    clusters_list += [current_category] + sub_clusters_list.copy()
    ranked_clusters_list += [current_category] + sub_ranked_clusters_list.copy()

    return clusters_list, ranked_clusters_list, clustering_time, ranking_time


def organize_by_response_categories(malasakit_response_list_copy, clustering_technique, priority_categories=[]):
    """
    Function that organizes the information based on (or per) response categories.

    Args:
        malasakit_response_list_copy (list): The list containing MalasakitResponse objects.
        clustering_technique (str): Select a clustering technique from the following: 'dice', 'word2vec', or 'fasttext'.
        priority_categories (list): [] if prioritization of categories will use the default, otherwise pass a list.

    Returns:
        clusters_list: a list containing the clustered responses.
        ranked_clusters_list: a list containing the clustered and ranked responses.
    """
    print('Clustering and Ranking...')

    # Group by response categories - regardless of which Codebook is used.
    malasakit_response_list_copy.sort(key=lambda response: response.tag)

    clustering_time = 0.0
    ranking_time = 0.0
    sub_malasakit_response_list_copy = []
    clusters_list = []
    ranked_clusters_list = []
    current_category = malasakit_response_list_copy[0].tag  # First category to process

    # Get responses under the category and put them in a list, processing each sublist per category
    for malasakit_response in malasakit_response_list_copy:
        # print(current_category, malasakit_response.tag)
        if current_category == malasakit_response.tag:
            # Keep on adding to list as long as it is on the same category
            sub_malasakit_response_list_copy.append(malasakit_response)
        else:
            # Process the sublist
            clusters_list, ranked_clusters_list, clustering_time, ranking_time = organize_sublist(
                                                                sub_malasakit_response_list_copy, clusters_list,
                                                                ranked_clusters_list, clustering_technique,
                                                                current_category, clustering_time, ranking_time)
            # Setup new category sublist
            sub_malasakit_response_list_copy = [malasakit_response]
            current_category = malasakit_response.tag

    # Another run to process last sublist / category
    clusters_list, ranked_clusters_list, clustering_time, ranking_time = organize_sublist(
                                                                sub_malasakit_response_list_copy, clusters_list,
                                                                ranked_clusters_list, clustering_technique,
                                                                current_category, clustering_time, ranking_time)

    print('\x1b[5;30;42m', 'Clustering done! Elapsed time:', clustering_time, '\x1b[0m')

    # -- START MODULE --
    # print(ranked_clusters_list)
    start_ranking_time = timeit.default_timer()

    # INFORMATION RANKING (RESPONSE CATEGORIES)
    ranked_clusters_list = rank.rank_by_response_categories(ranked_clusters_list, priority_categories)

    ranking_time += (timeit.default_timer() - start_ranking_time)
    # print(ranked_clusters_list)
    # -- END MODULE --

    print('\x1b[5;30;42m', 'Ranking done! Elapsed time:', ranking_time, '\x1b[0m')

    return clusters_list, ranked_clusters_list


# Function that organizes the information among all entries
def organize_all_entries(malasakit_response_list_copy, clustering_technique):
    """
    Function that organizes the information among all entries

    Args:
        malasakit_response_list_copy (list): The list containing MalasakitResponse objects.
        clustering_technique (str): Select a clustering technique from the following: 'dice', 'word2vec', or 'fasttext'.

    Returns:
        clusters_list: a list containing the clustered responses.
        ranked_clusters_list: a list containing the clustered and ranked responses.
    """
    clusters_list = []
    # ranked_clusters_list = []

    # -- START MODULE --
    print('Clustering...')
    start_module_time = timeit.default_timer()

    # INFORMATION CLUSTERING
    if clustering_technique == 'dice':
        # SORENSEN-DICE COEFFICIENT CLUSTERING
        clusters_list = cluster.cluster_information(malasakit_response_list_copy, 'dice')
    elif clustering_technique == 'word2vec':
        # WORD EMBEDDINGS CLUSTERING
        clusters_list = cluster.cluster_information(malasakit_response_list_copy, 'word2vec')
    elif clustering_technique == 'fasttext':
        # WORD EMBEDDINGS CLUSTERING
        clusters_list = cluster.cluster_information(malasakit_response_list_copy, 'fasttext')

    print('\x1b[5;30;42m', 'Clustering done! Elapsed time:', (timeit.default_timer() - start_module_time), '\x1b[0m')
    # -- END MODULE --

    # -- START MODULE --
    print('Ranking...')
    start_module_time = timeit.default_timer()

    # INFORMATION RANKING
    ranked_clusters_list = rank.rank_clusters_by_frequency(clusters_list)

    print('\x1b[5;30;42m', 'Clustering done! Elapsed time:', (timeit.default_timer() - start_module_time), '\x1b[0m')
    # -- END MODULE --

    return clusters_list, ranked_clusters_list
