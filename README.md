# Turn Language into Action: A Natural Language Hackathon for Good


We developed a web application with the purpose of creating ways to improve the world using deep Natural Language Processing and Expert.ai's Natural Language API, as part of [Expert.ai's hackathon](https://expertai-nlapi-092022.devpost.com/).

## Competion Category
ESG (Environmental, Social, Governance)

## Application Name
***SustainaMeter***: *Raising ESG Standards*.
Access the app [here!](https://holistic-insights-turn-language-into-action-2022-home-tmsf71.streamlitapp.com/)


## 👥 Authors
* [Diogo Polónia](https://www.linkedin.com/in/diogovalentepolonia/)
* [Farley Rimon](https://www.linkedin.com/in/farley-rimon-54a57918b/)
* [João Matos](https://www.linkedin.com/in/farley-rimon-54a57918b/)
* [João Pereira](https://www.linkedin.com/in/joao-afonso-pereira/)
* [Patrícia Rocha](https://www.linkedin.com/in/patriciaferreirarocha/)

## 📢 Motivation
Every business is deeply intertwined with environmental, social, and governance (ESG) concerns, and it has become of paramount importance to evaluate the risks that the organization is taking on based on the ESG externalities it is generating.

This is key, not only for business growth and investment, as ESG-oriented investing has experienced a meteoric rise as global sustainable investment now tops $30 trillion ([Global News Wire, 2022](https://www.globenewswire.com/en/news-release/2022/04/13/2422237/0/en/Investments-in-Global-Sustainability-Now-Top-30-Trillion.html)), but also due to the growing impact it has on the public's perception. In fact, 83% of consumers think companies should be actively shaping ESG best practices ([PwC, ND](https://www.pwc.com/gx/en/services/sustainability/publications/cop26/how-much-does-the-public-care-about-esg-pwc-cop26.html)). Communication has a big influence on this - the way the company communicates can reflect how they percieve ESG and their strategy towards sustainability.

With this in mind, and using Expert.ai's ESG and Sentiment Analysis Knowledge Models, we set out to build an app to provide holistic insights, both to companies and the public, to raise transparency on companies' attitude towards ESG and compare their position among the industry and with public perception. 

The ultimate goal is two-folded:
1. Help companies navigate the ESG world and understand their current status, in order to improve their strategy regarding ESG.
2. Provide an easy and transparent way for consumers, employees, and the general public to assess any company's behavior towards ESG.

## 🔢 Data
This project uses social media  posts and comments (from LinkedIn) as main data sources. The raw text was processed with Expert.ai's Knowledge Models to create datasets with ESG and Sentiment scores. These are the 4 main created datasets:

* ***Posts*** contains 9450 posts' information, from a group of 165 selected companies.
* ***Comments*** contains a total of 2442 comments, retrieved from each post in the Posts dataset.
* ***Analysed Posts*** includes the ESG Knowledge Model predictions for the posts data.
* ***Analysed Comments*** includes the Sentiment Analysis Knowledge Model evaluation of comments' text sentiment.

Due to the characters limit on Expert.ai's API (<= 10M characters/month), we had to keep our datasets limited to the top 50 companies with the most posts. With unlimited access to the API, we could populate the dataset with more and more companies and posts to grow the app and amplify its impact.

Finally, we believe that these datasets can enable future research on NLP-related topics, providing relevant labelled data, which could be made public as open-source in a platform like [Kaggle](https://www.kaggle.com/).

## ⚙️ Methods and Tools
#### ***1. Creating the Base Datasets***
To select the companies, we created a subset of 165 from Fortune 1000 Companies list with social media information from [GitHub](https://gist.github.com/mbejda/45db05ea50e79bc42016). It was considered to be a meaningful subset, with some of the most important firms in the list of the 1000 largest American companies. 

Then, we resorted to the [LinkedIn API](https://linkedin-api.readthedocs.io) to build our own social media datasets.  Posts and Comments' data were scrapped from these companies' pages on LinkedIn.

#### ***2. Running ESG and Sentiment Analysis***
Posts' and comments' text from the base dataset were analysed using Expert.ai's knowledge models, updating the datasets to include the ESG categorization and subcategories scores (for posts) and the text sentiment (for comments).

#### ***3. Building Visualizations***
In order to provide deep and holistic insights, we focused on creating visualizations with *Matplotlib* and *Plotly* for ESG category counts, total subcategory scores, and sentiment dispersion, allowing the user to easily compare values.

#### ***4. Creating a Sentiment Predictor***

Using Expert.ai's pre-trained models to provide weak supervision, we trained a model to estimate the sentiment a given post will generate among people. First, we built a dataset consisting of raw LinkedIn posts and the predicted average sentiment score of their comments. Then, we fit a ***AutoKeras' TextRegressor*** using the latter as noisy labels. AutoKeras automatically searches for the best model and hyperparameters. 

#### ***5. Constructing the Web App***
By taking advantage of **Streamlit**'s open-source Python library to turn python scripts into shareable web apps, we built a single-page app, with two tabs:
1. *Company Scoring*, where users can review a single company's general post, ESG, and sentiment performance, as well as compare it with a selection of companies;
2. *New Post Scoring*, where users can write a new post, and receive feedback on its ESG rating, and an average sentiment prediction that the post will receive from the audience.


## 💻 Product
### Definition
A digital platform that raises transparency on companies' ESG actions, helping them enhance ESG strategy by analysing social media perception. SustainaMeter also empower more responsible investments, career decisions and purchases, by gathering and reviewing information on how companies communicate ESG accomplishments.

### Users
1. General audience who wants to review and evaluate a company's attitude towards ESG
2. Companies looking to assess their ESG positioning and communication, or test new communications

### Activities
SustainaMeter's solution:
- Scrapes LinkedIn's posts and respective comments for different companies;
- Scores posts in terms of ESG and detects the comments sentiment (using Expert.ai's API);
- Provides visualizations and metrics for assessing companies' communication in terms of ESG, individually and collectively, and how the audience reacts to it;
- Predicts the average sentiment a new post will generate, and provides insights on its ESG score;

The following diagram, exemplifies SustainaMeter's activities:

![Product Flowchart](https://i.imgur.com/o0LNQbo.jpg)

### How does the app work?
Users can input:
- **Company name**, from the list of available (pre-scraped companies);
- **Number of posts** to analyse, selected in order of highest number of likes;
- **Comparison group** for comparing the selected company's performance with the top 5 companies sorted by no. of likes, comments, posts or their ESG score

Users, will, then, be able to dive into individual analyis of the company and compare it with the average ratings of the top 5 companies selected.

![Screeshots of the App visualizations](https://i.imgur.com/l1Ptr7z.png)

![Screeshots of the App visualizations](https://i.imgur.com/PV7wc97.png)

![Screeshots of the App visualizations](https://i.imgur.com/6nPb2dR.png)

Besides, users are able to input text for a new post and analyse the ESG results as well as the predicted sentiment.

![Screenshots of the post results](https://i.imgur.com/8Fzp8LR.png)

![Acreenshots of the post results](https://i.imgur.com/veT1EMt.png)

### Repository Organization
***SustainaMeter***'s [GitHub repository](https://github.com/holistic-insights/Turn-Language-into-Action-2022) contains all the code built to support the app and, simultaneously, host the app integrated with Streamlit, that mainly uses the following scripts (in the root folder):
- **Home&#46;py** has all streamlit code, used to generate the visualizations;
- **ExpertaiAPI&#46;py** includes the class for handling Expert&#46;ai's API requests;
- **linkedin-api folder** has the scripts for all scraping done from LinkedIn;

Support scripts and datasets are organized in separate folders:
- **Data Scraping**, which includes the [linkedin-api](https://linkedin-api.readthedocs.io/en/latest/?badge=latest) package with our own modifications for better performance.
- **ESG Models**, where we stored all datasets (Data folder), scripts and tests for running Expert.ai's models on scraped posts (LinkedIn expert_AI scores folder) and training our text regressor (LinkedIn Post ESG predictor).

## 💥 Impact

The current generation, with people who are becoming employees, buyers, and investors, is taking note of corporations dedicated to sustainability and rewarding them with loyalty. 

***SustainaMeter*** will allow companies to better promote their ESG accomplishments on social media, and align their ESG strategy with their customer base, with transparency at its core.

On the other hand, the community will be able to access and assess reliable information about how each enterprise communicates its ESG, and make better decisions for investments, careers, purchases or partnerships. ***SustainaMeter*** is a centralized way to validate companies' ESG credibility, including *greenwashing* evaluations.

***SustainaMeter*** aims at leveraging Expert.ai's Knowledge Models to make communication and action transparent and accessible to everyone, building towards a more sustainable world and community.

## 🚀 Scalabity

***SustainaMeter*** is crafted for scalability. Even though in this proof-of-concept we are only looking at 50 companies from the Fortune 1000 list, SustainaMeter is ready to receive any companies' dataset. To make our insights as unbiased and complete as possible, companies of every type must come to play. It is easy to include:
- different markets across the globe;
- companies with different sizes (start-ups, SMEs or large international corporations), assessed in terms of revenue, age, number of employees, etc.;
- firms from diverse industries, to take meaningful conclusion about the sector's impact on ESG policy.


The source of the used data can also be easily scaled to new social media platforms. While LinkedIn provided relevant, ESG-orient content, the comments tend to yield positive sentiment. Twitter, on the other hand, provides more diversity in opinions, which comes with the cost of increased noise. Once again, ***SustainaMeter*** can be easily adapted to new data sources and, thanks to Expert.ai's API, further value can be taken from text in companies' social media. All one must do is to adapt the input databases.

Finally, using the tools we created (made available on GitHub), one can further leverage ***SustainaMeter*** to:
- produce rankings about companies' attitude towards ESG;
- assess a single new company and compare its performance against our large database;
- extrapolate these tool to evaluate public figures' profile.

**Let's raise transparency on companies' attitude towards ESG. The sky is the limit!**

