import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import pairwise_distances 
from sklearn.model_selection import train_test_split

def convert(val):
    if val == 'content_followed':
        return 5
    elif val == 'content_commented_on':
        return 4
    elif val == 'content_saved':
        return 3
    elif val == 'content_liked':
        return 2
    else:
        return 1

def recommend(id): 

    ## Import consumer transactions
    consumertxn = pd.read_csv('consumer_transanctions.csv')

    ## Import platform content master
    platformcontent = pd.read_csv('platform_content.csv')

    ## add rating column
    consumertxn['rating'] = consumertxn['interaction_type'].apply(convert)

    ## distinct users/items
    n_items = consumertxn['item_id'].nunique()
    n_users = consumertxn['consumer_id'].nunique()


    consumertxn_train, consumertxn_test = train_test_split(consumertxn, test_size=0.30, random_state=31)


    data_matrix = consumertxn.pivot_table(
        index='consumer_id',
        columns='item_id',
        values='rating'
    ).fillna(0)

    for col in data_matrix.columns:
        data_matrix[col].values[:] = 0

    ## fill with train data
    for idx, line in consumertxn_train.iterrows():
        data_matrix.loc[line['consumer_id'], line['item_id']] = line['rating']


    ## used for evaluation phase
    data_matrix_test = consumertxn.pivot_table(
        index='consumer_id',
        columns='item_id',
        values='rating'
    ).fillna(0)

    for col in data_matrix_test.columns:
        data_matrix_test[col].values[:] = 0

    ## fill test data
    for idx, line in consumertxn_test.iterrows():
        data_matrix_test.loc[line['consumer_id'], line['item_id']] = line['rating']


    consumerid = data_matrix.index.get_loc(int(id))

    ## train with train data
    user_similarity = 1- pairwise_distances(data_matrix, metric='cosine')

    ## item similarity 
    item_similarity = 1- pairwise_distances(data_matrix.T, metric='cosine')

    item_prediction = np.dot(user_similarity,data_matrix_test)

    prediction_df = pd.DataFrame(item_prediction)

    recommended_movie_df = pd.DataFrame(prediction_df.iloc[consumerid].sort_values(ascending=False))

    recommended_movie_df.reset_index(inplace=True)

    recommended_movie_df.columns = ['item_id', 'score']

    recommended_movie_df['item_id'] = recommended_movie_df['item_id'].apply(lambda x : data_matrix_test.columns[x])

    merged_user = pd.merge(recommended_movie_df, platformcontent, on='item_id', how='left')

    ## Already watched contents for user index 117
    alreadyWatchedItems = consumertxn[(consumertxn['consumer_id']==data_matrix.index[consumerid]) & (consumertxn['interaction_type']=='content_watched')]['item_id']

    ##  top 10 news for customer id -8078450058314350213 - 
    ## This can be shown in new section for Iprint containing top 10 recommendation customized for user index 117
    ## only show valid contents and new ones
    recom_list  = merged_user[(merged_user['interaction_type']!='content_pulled_out')&(~merged_user['item_id'].isin(alreadyWatchedItems))]['title'].values
    return list(recom_list)[1:11]
