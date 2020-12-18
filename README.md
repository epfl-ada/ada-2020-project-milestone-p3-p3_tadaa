**1. Title :** Empowering Effects : Thunberg’s movement on Climate Change

**2. Abstract :**

In the replicated publication on “Chilling effects”, the goal was to look at the change in behaviour of the public as a potential reaction to the revelations of surveillance of June 2013. This effect is definitely detrimental to society since the public imposes on themselves restrictions by fear of retribution. In this extension, it is questioned whether the mediatic appearances of climate activist Greta Thunberg induced a positive change in behaviour in the public. Using data from Twitter, it will be possible to see to what extent the topic is discussed and shared (for movement followers as well as for people against it). Then using the number of wikipedia pageviews per day on specific climate change related articles, it will be possible to assess if the movement stays only on social media or if the public actually tries to get informed on the topic by reading on wikipedia. That behaviour would arguably increase the freedom of individuals due to their expanded knowledge.


**3. Research Questions :**
1. What is the short and long term impact of Thunberg's 2 media appearances on the use of Twitter hashtags related to the topic of climate change ?

2. What is the proportion of Twitter hashtags related to the topic of climate change in support of the movement and what fraction is against it (across the time window considered) ?

3. What is the short and long term impact of Thunberg's media appearance on the propensity of the public to get climate change related information on Wikipedia ?

**4. Proposed dataset :**

First and foremost, the selected interest period depends on the choice of events that will be the pivots of the interrupted time series analysis. (ITS) These events are as follows: the school strike of August 20, 2018 led by Greta Thunberg and the 2018 United Nations Climate Change Conference (COP24) on December 14, 2018. The period of analysis is between January 2018 and February 2020. (we thought that COVID-19 period might influence the data a bit too much).
 
Wikipedia: Take the daily pageviews number of 3 different corpus: climate change related, nature related and a control group (we can take the same  control group as in the publication that is: the most popular articles on Wikipedia). We take the dataset out of the english wikipedia. (https://pageviews.toolforge.org/pageviews/).
Twitter : Finding a large dataset of old tweets seems to be a recurring problem. Twitter's API limits the number of requests and most software solutions for extracting tweets are chargeable. We therefore considered taking a dataset extracted by institutions in the past for future analyzes. Unfortunately, this data is collected under specific hashtags or does not include dates for longitudinal analysis. An archive.org project ( https://archive.org/details/twitterstream ) passively collected all of the general stream's tweets. We can take a specific period to the day, but this requires selecting the tweets in very large data structures. (2 Go per day of tweets) The main logistic problem will be to gradually download the data and select the tweets according to a corpus of hashtags defined to represent the different movements linked to the climate. Downloading, managing the storage of as much data (momentarily before sorting) and the calculation time to iterate through these large JSON files (to select the tweets belonging to the corpus) are the constituents of the challenge imposed by the use of this data. Another problem will be the merging of all the JSON files in a format usable by Pandas


**5. Methods :**

*Data collection :* 
For Wikipedia collection we will use: https://pageviews.toolforge.org/pageviews/
We will define the 3 different corpus of article thanks to predefined Wikipedia list such as: https://en.wikipedia.org/wiki/Index_of_climate_change_articles
For Twitter we will use the data from the archive.org project mentioned before. The tweets will be selected based on the presence of a hashtag corresponding to one of the three corpus of hashtags. The first corpus corresponds to the 10 hashtags commonly used by the movement defending the climate cause. The second corpus are the 10 hashtags used by climate change skeptics. And the latest corpus is a control group of 10 commonly used hashtags on Twitter not "buzzed" to check general Twitter activity during the period. Once we have the data sorted and merged, we can make a dataframe with the sum of the tweets per day for the different hashtags. We will therefore find a set of data similar to the article on the chilling effect and we will be able to do a longitudinal analysis.
 
*Linear regression :*
Once we have all the Wikipedia data we can follow the same study as in the paper. We will use the same ITS design with 2 events and combine it with a segmented regression analysis.
For Twitter the principle is similar. An ITS is applied between the events and the unit of analysis is the number of hashtags mentions per day. (Similar to the number of views per article for the Wikipedia side) The days will be aggregated into an adequate time unit for representation.
 
*Data analysis :* 
Our analysis will be in 2 parts.
First we want to check if the Twitter community is sensitive to Greta’s mediatic intervention. As we have the dataset with climatoseptic hashtag and pro-climate hashtag, we want to see if people against and people who believe in climate change are influenced the same way. We will be able to see that thanks to the linear regression on the twitter dataset.
Then we will analyse if the people are getting more interested in climate change topics thanks to Greta’s mobilisation. This is shown through the Wikipedia dataset. Thanks to the linear regression, we will be able to see if, indeed, people are going more to Wikipedia pages concerning climate change than before Greta.

**6. Proposed timeline :**

*Week 1 :* All Twitter data will be downloaded gradually and selected according to the hashtag corpora. Once all of the JSON files are sorted for the entire period of interest, they will be merged and transposed into a compatible format. This process takes a long time due to the amount of data and the limitation in download speed and storage space.
Wikipedia data will be downloaded 10 pages by 10 pages thanks to the previous cited website. It might take a long time to have the 3 different corpus of 50 articles. Then we have to merge them.

*Week 2 :* Do the linear regression and the data analysis + start to think what to put in the data story and the short video

*Week 3 :* Do the data story and the short video + write the report.


**7. Organization within the team :**

*Milestone 3.1, week 1 :* Danny collects the data on Twitter. If it is shown to be too complicated because of the size of the dataset, we will do the work only with Wikipedia. Lea collects the one on Wikipedia. Both will clean their dataset. Information about retrieved datas will be given to Jonathan as well. Jonathan continues to research information about our topic.

*Milestone 3.2, week 2 :* Jonathan will do the regression analysis. Then a meeting is planned with all of us to talk about the data analysis, to see what conclusions we can draw from our graphs + to see the big lines of what we want to put in the video and datastory.

*Milestone 3.3, week 2 :* A script of the short video is produced by Lea and agreed upon by the team members after a zoom meeting.

*Milestone 3.4, week 3 :* Lea will do the datastory, Jonathan will do the short video with Lea’s help and Danny will write the most part of the report. Of course, communication needs to be a huge part of this project, so all of us will have a say on the job of other team members and give comments and extra help if any needed.



**8. Questions for TAs (optional) :**

The data found for the twitter analysis is very heavy and somewhat incomplete. By discussing with other groups for comparison, it seems to us that this part should be removed to make for a more suitable workload. That part of the analysis seems useful to us since it would allow us to compare how the topic trends on twitter to how the public actually takes action on it. Do you think it is feasible ? We are just worried about the technical aspect regarding connection speed, storage space and processing time. Processing the data is simple (Find a value in a JSON) but it is hard to assess how slow it can get considering the amount of data. The fear is to have a technical problem that blocks the rest of the analysis. We also worry about having too much work and not being able to do it all on time.



**9. Contributions :**

*Danny :* wrote a large part of the code, participated in the interpretation of the results, helped with data gathering.

*Léa :* Gathered the data, wrote the data story, participated in the interpretation of the results, participated in the recording of the video

*Jonathan :* Helped with data gathering, helped with writing the code, participated in the interpretation of the results, participated in the recording of the video.
