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
# INFORMATION RANKING
# Ranks the clustered information based on the following choices:
#   > Frequency Count of Responses
#   > Response Categories
#   > Combination of both
###################################################################################


def rank_clusters_by_frequency(clusters_list):
    """
    Function for ranking the clusters based on their frequency counts (descending order: highest count first).
    lambda defines a mini-function which receives x (in this case, the row) and returns the second element of x (x[1]).

    Args:
        clusters_list (list): The list containing the clustered insights.

    Returns:
        updated_clusters_list: a list containing the ranked clusters using 'sorted(clusters_list, reverse=True,
                        key=lambda x: x[1])' function.
    """
    return sorted(clusters_list, reverse=True, key=lambda x: x[1])


def rank_by_response_categories(clusters_list, priority_categories):
    """
    Function for ranking (rearranging the groups) the clusters based on their response categories (prioritizing
    categories with concrete actions that can be implemented by decision makers). This function will only apply to
    'organize_by_response_categories' format and categories in Malasakit Codebook 4.7 that upon arrangement exhibits
    the following prioritization order:
        > Information Campaign and Capacity Building
        > Community-wide Logistic support for disaster response
        > Infrastructure Maintenance and Management
        > Early Warning System
        > Preparedness for emergency
        > Local government accountability
        > Filipino values
        > Others
    For custom categories, priority_categories has been provided to accommodate them.

    Args:
        clusters_list (list): The list containing the clustered insights.
        priority_categories (list): [] if prioritization of categories will use the default, otherwise pass a list.

    Returns:
        updated_clusters_list: a list containing the ranked clusters.
    """
    print("Rank by Response Categories...")
    updated_clusters_list = []
    if not priority_categories:
        # If toggle is empty, use default prioritization ranking
        priority_ranking = ['Information Campaign and Capacity Building',
                            'Disaster Relief',
                            'Community-wide Logistic support for disaster response',
                            'Infrastructure Maintenance and Management',
                            'Early Warning System',
                            'Preparedness for emergency',
                            'Local government accountability',
                            'Filipino values',
                            'Others']
    else:
        # If toggle contains a value, use it instead
        priority_ranking = priority_categories

    # Run through per categories in priority_ranking
    for category in priority_ranking:
        index_ctr = 0
        category_found = False
        # Get all in clusters that are under the current category
        # print('CL:', clusters_list)
        while clusters_list and index_ctr < len(clusters_list):
            if type(clusters_list[index_ctr]) is str:
                # print(clusters_list[index_ctr].casefold(), category.casefold())
                if clusters_list[index_ctr].lower() == category.lower():  # If same as the current category
                    updated_clusters_list.append(clusters_list[index_ctr])  # Insert clusters list on new list
                    # print(updated_clusters_list)
                    clusters_list.pop(index_ctr)  # Remove from clusters_list
                    index_ctr -= 1  # To prevent skipping items
                    category_found = True
                elif clusters_list[index_ctr].lower() != category.lower() and category_found:
                    break  # Exit while loop since a new category has been encountered
            elif category_found:
                updated_clusters_list.append(clusters_list[index_ctr])
                clusters_list.pop(index_ctr)  # Remove from clusters_list
                index_ctr -= 1  # To prevent skipping items
            index_ctr += 1
        # print('CL:', clusters_list)
        # print('NCL:', updated_clusters_list)

    return updated_clusters_list
