**News Recommendation System for iPrint media**

* Recommend new top 10 relevant articles to a user when he visits the app at the start of the day
* Recommend top 10 similar news articles that match the ones clicked by the user. Try different models for generating these recommendations and experiment with hybrid models for the same


**Approach :**

* EDA on dataset
* Collabrative filter recommendation
* Train/test split data and fill data matrix(distinct users * distinct items) with train and test data
* Calculate user/item similarity on train data
* Calculate user/item prediction matrix using test data
* Find top 10 recommendation for specific user using above matrix (e.g. user index 117). consumer_id will be input to model. These recommendations will be shown in New section developed on iPrint media App
* Find top 10 relavent news for 1st recommendation for user index 117. These recommendations will be shown on L2 page assuming user clicks first recommendation
* Content filter recommendation
* Find top 10 recommendation using content filter for 1st recommendation for user index 117
* Hybrid filter recommendation
* Combine results of Collabrative and content recommendation and show final top 10 recommendation for 1st recommendation for user index 117
* Evaluate MAE, RMSE, Precision@10, Global Precision@10 on test data and infer effectiveness of recommndation.
