from tweepy.streaming import StreamListener
from lib import fileController, kmeans, triads, interactiongraph, statistics, centrality, process, tries
from API import restController, twitterRest, restController, twitterStreamer
from database import mongoController
from threading import Thread
from multiprocessing import Process
from database import mongoController
import sys

# Runs both the twitter Stream API and REST APIs
def run():
    stream()
    api()

# Runs the twitter Streaming API
def stream():
    # initialize REST client & get trending topics
    twitter_client = twitterRest.twitterClient()
    trending_list = twitter_client.get_trending_list()

    # initialize Streaming client thread & start proccessing
    streamer = twitterStreamer.TwitterStreamer()
    Process(target=streamer.stream_tweets, args=([trending_list])).start()

# Runs the twitter REST API's
def api():
    twitter_client = twitterRest.twitterClient()
    rest_controller = restController.restController(twitter_client)
    Process(target=rest_controller.retweet_loop).start()
    Process(target=rest_controller.timeline_loop).start()
    Process(target=rest_controller.followers_loop).start()
    Process(target=rest_controller.friends_loop).start()

# Finds how many lines are in each API file and prints to screen
# Lets user know how many users still need properties processed
def status():
    file_controller = fileController.fileController()
    file_controller.write_data_to_file("data/status.txt", "Filename, lines\n")
    files = ["data/followers.txt", "data/friends.txt", "data/retweets.txt", "data/users.txt"]
    print("Current status of files \n\nFilename, \tlines to be processed")
    for file in files:
        length = file_controller.get_length_of_file(file)
        file_controller.append_one_line("data/status.txt", file + ", " + str(length))
        print(file + ", \t" + str(length))

# Processes all data - groups tweets then calculates basic statistics, centralities & triads
def process_results():
    file_controller = fileController.fileController()
    data_processor = process.process(file_controller)
    kmeans_processor = kmeans.kmeans()

    kmeans_processor.kmeans()
    print("This may take a few minutes...")
    data_processor.basics()
    data_processor.retweets()
    data_processor.quotes()
    data_processor.hashtags()

    triad_controller = triads.triads()
    triad_controller.calculate_triads()

    tries_controller = tries.tries()
    tries_controller.calculate_tries()

# Prints the manual to terminal
def manual():
    print("--------PYTHON TWITTER CRAWLER MANUAL-------\n")
    print("This application scrapes twitter data using official twitter API's then uses kmeans context analysis on the tweets to group them together.")
    print("\nThe STREAM is used with current trending topics as the keywords and will save all incoming tweets to the local database. It will also record the USER_ID to files to be processed by the REST APIs")
    print("\nREST APIs are used to retrieve more information about the users which were recorded from the streaming API.")
    print("\nStatistics are derived from the tweets as a whole and as groups")
    print("These statistics are recorded in the results folder")
    print("------- Statistics -------")
    print("Total tweets \n Total retweets \n Total quotes \n Total replies \n Total hashtags")
    print("------- ------- -------")
    print("\nCentrality measures are also recorded for the properties as a whole and as groups")
    print("\nThese statistics are recorded in the results folder")
    print("-------Centrality Measures-------")
    print("In Centrality \n Out Centrality \n Closeness Centrality \n Betweenness Centrality \n Eigenvector Centrality")
    print("------- ------- -------\n")
    print("\nThe application can be run with the following commands")
    print("------- COMMANDS -------")
    print("run : This runs both the Stream and REST APIs. All results are stored in a local mongodb table")
    print("run-stream : This runs only the streamer")
    print("run-api : This runs only the APIs")
    print("process : This creates the groupings and calculates all statistics which are then saved in the results folder")
    print("status : Outputs the quantity of lines of all files used by the APIs. This shows how many items still need to be processed by the APIs")
    print("manual : Outputs the manual to console")
    print("------- ------- -------")

# Main method determines which function to run
# Takes a single argument to select function
if __name__=="__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print("ERROR: Invalid Arguments supplied\nCheck the manual to for valid arguments\nRun this command : python crawler.py manual")
    if len(sys.argv) == 2:
        if(sys.argv[1]) == 'run':
            print("RUNNING STREAMER AND REST API")
            run()
        if(sys.argv[1]) == 'run-stream':
            print("RUNNING STREAMER")
            stream()
        if(sys.argv[1]) == 'run-api':
            print("RUNNING REST API")
            api()
        if(sys.argv[1]) == 'process':
            print("PROCESSING TWEETS")
            process_results()
            print("TWEETS PROCESSED")
        if(sys.argv[1]) == 'status':
            print("PRINTING STATUS")
            status()
        if(sys.argv[1] == 'purge'):
            print("PURGING DATABASE")
            database = mongoController.mongoController()
            database.users.remove_all_users()
            print(database.users.get_all_users())
            print("PURGED DATABASE")
        if(sys.argv[1] == "manual"):
            manual()

    ## Write to file for debug
    # file_controller = fileController.fileController()
    # file_controller.write_data_to_file("test.json", database.users.get_all_users())
