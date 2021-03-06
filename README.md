# WebScience
Twitter Scraping &amp; Analysing

University Of Glasgow

Computer Science 2020

## How To Use

To run the application use the following command 'python crawler.py xxxx' where xxx is one of the following properties.
```
run  -- This runs the application with both the Twitter REST & Stream API's.

run-stream  -- This runs the applcation with only the Twitter Stream API.

run-api  -- This runs the application with only the Twitter REST API's.

process  -- This generates data from the current dataset and stores all statistics, centrality measures, tries & triad data in the results folder in both .txt and .csv files for further analysis.

status  -- Shows how many ID's of each type which are yet to be processed by the REST API's

purge  -- Removes all data from the database

manual  -- Prints usage information to the console
```
When using this application it should be noted that when the REST API's are used they make queries based on data that has been recieved from the streamer. The relevant Tweet ID's and User ID's are kept in files locally to be processed later. The REST API will not process anything that was added to the file less than one day ago. This is mainly due to the streamer processing brand new tweets where statistics like retweets, replies and quotes will not be relevant untill the tweet has been live for some time.
If you would prefer to not use this feature the setting can be changed in code, or timestamps can be manipulated in the relevant files directly.

## Required Credentials

As this application uses official Twitter API's you will need to input your twitter credentials into the /API/credentials.py file. 

```
ACCESS_TOKEN = 
ACCESS_TOKEN_SECRET =
CONSUMER_KEY =
CONSUMER_SECRET =
```

## Required Dependencies

The following libraries must be installed to make use of this application. These can be installed by using pip.

pip install ...

```
tweepy
pymongo
matplotlib
networkx
filelock
```


## Importing The Example Data

There is example data provided with this application that can be imported to a local mongoDB instance with the following command from the applications root directory.

`sudo mongoimport --db twitter --collection users --file exampledata.json`

## Further Use

All statistics and data generated from this application will be stored in the results folder where CSV files are generated for further analysis.
