from lib import interactiongraph, centrality, statistics, triads

# Generates all statistics and measurements.
class process():

    def __init__(self, file_controller):
        self.file_controller = file_controller
        self.stat_process = statistics.statistics()

    # Retrieves basic statistics such as how many of each property (tweets, retweets, replies, followers)
    # Also notes which group has the max and min of each
    # Writes to file for analysis
    def basics(self):
        print("PROCESSING BASIC STATISTICS - OUTPUT = results/basicstats.txt")
        total_tweets = "Total Tweets : " + str(self.stat_process.total_tweets())
        self.file_controller.append_one_line("results/basicstats.txt", total_tweets)

        tweets_min, group_min = self.stat_process.smallest_tweets_group()
        group_least_tweets = "Group with the least tweets : " + str(group_min) + ". Quantity : " + str(tweets_min)
        self.file_controller.append_one_line("results/basicstats.txt", group_least_tweets)

        tweets_max, group_max = self.stat_process.largest_tweets_group()
        group_most_tweets = "Group with the most tweets : " + str(group_max) + ". Quantity : " + str(tweets_max)
        self.file_controller.append_one_line("results/basicstats.txt", group_most_tweets)

        total_retweets = "Total Retweets : " + str(self.stat_process.total_retweets())
        self.file_controller.append_one_line("results/basicstats.txt", "\n" + total_retweets)

        tweets_min, group_min = self.stat_process.smallest_retweets_group()
        group_least_retweets = "Group with least retweets : " + str(group_min) + ". Quantity : " + str(tweets_min)
        self.file_controller.append_one_line("results/basicstats.txt", group_least_retweets)

        tweets_max, group_max = self.stat_process.largest_retweets_group()
        group_most_retweets = "Group with most retweets : " + str(group_max) + ". Quantity : " + str(tweets_max)
        self.file_controller.append_one_line("results/basicstats.txt", group_most_retweets)

        total_quotes = "Total Quotes : " + str(self.stat_process.total_quotes())
        self.file_controller.append_one_line("results/basicstats.txt", "\n" + total_quotes)

        tweets_min, group_min = self.stat_process.smallest_quote_group()
        group_least_quotes = "Group with least quotes : " + str(group_min) + ". Quantity : " + str(tweets_min)
        self.file_controller.append_one_line("results/basicstats.txt", group_least_quotes)

        tweets_max, group_max = self.stat_process.largest_quote_group()
        group_least_quotes = "Group with most quotes : " + str(group_max) + ". Quantity : " + str(tweets_max)
        self.file_controller.append_one_line("results/basicstats.txt", group_least_quotes)

        total_replies = "Total Replies : " + str(self.stat_process.total_replies())
        self.file_controller.append_one_line("results/basicstats.txt", "\n" + total_replies)

        tweets_min, group_min = self.stat_process.smallest_reply_group()
        group_least_replies = "Group with least replies : " + str(group_min) + ". Quantity : " + str(tweets_min)
        self.file_controller.append_one_line("results/basicstats.txt", group_least_replies)

        tweets_max, group_max = self.stat_process.largest_reply_group()
        group_least_replies = "Group with most replies : " + str(group_max) + ". Quantity : " + str(tweets_max)
        self.file_controller.append_one_line("results/basicstats.txt", group_least_replies)

    # Creates quotes network interaction map and processes centrality measures
    # Writes all data to a CSV file for further analysis
    # Writes user reable statistics to .txt file
    def quotes(self):
        print("PROCESSING QUOTE STATISTICS\nBasic Statistics output = results/quotesstats.txt\nAll statistics output = results/quotes.csv")
        network_process = interactiongraph.interactiongraph()
        self.file_controller.append_one_line("results/quotes.csv", "type, group, results")
        for i in range(20+1):
            print("Processing quotes for group " + str(i))
            if i == 0:
                retweets = network_process.quotes()
                group = "All"
                total_quotes = "Total Quotes : " + str(self.stat_process.total_quotes())
            else:
                retweets = network_process.quotes_group(i-1)
                group = i-1
                total_quotes = "Total Quotes : " + str(self.stat_process.total_quote_group(group))

            self.file_controller.append_one_line("results/quotesstats.txt", "STATS FOR GROUP " + str(group))
            self.file_controller.append_one_line("results/quotesstats.txt", total_quotes)
            self.processing(retweets, group, "quotes")

    # Creates retweets network interaction map and processes centrality measures
    # Writes all data to a CSV file for further analysis
    # Writes user reable statistics to .txt file
    def retweets(self):
        print("PROCESSING RETWEETS STATISTICS\nBasic Statistics output = results/retweetsstats.txt\nAll statistics output = results/retweets.csv")
        network_process = interactiongraph.interactiongraph()
        self.file_controller.append_one_line("results/retweets.csv", "type, group, results")
        for i in range(20+1):
            print("Processing retweets for group " + str(i))
            if i == 0:
                retweets = network_process.retweets()
                group = "All"
                total_quotes = "Total Retweets : " + str(self.stat_process.total_retweets())
            else:
                retweets = network_process.retweets_group(i-1)
                group = i-1
                total_quotes = "Total Retweets : " + str(self.stat_process.total_retweets_group(group))
            self.file_controller.append_one_line("results/retweetsstats.txt", "STATS FOR GROUP " + str(group))
            self.file_controller.append_one_line("results/quotesstats.txt", total_quotes)
            self.processing(retweets, group, "retweets")

    # Creates hashtags network interaction map and processes centrality measures
    # Writes all data to a CSV file for further analysis
    # Writes user reable statistics to .txt file
    def hashtags(self):
        print("PROCESSING HASHTAG STATISTICS\nBasic Statistics output = results/hashtagsstats.txt\nAll statistics output = results/hashtags.csv")
        network_process = interactiongraph.interactiongraph()
        self.file_controller.append_one_line("results/hashtags.csv", "type, group, results")
        for i in range(20+1):
            print("Processing hashtags for group " + str(i))
            if i == 0:
                retweets = network_process.hashtags_user('all')
                group = "All"
            else:
                retweets = network_process.retweets_group(i-1)
                group = i-1
                self.processing(retweets, group, "hashtags")

    # Calculates all centrality measures for the given group (or all) and finds the groups which have the max and min of each
    def processing(self, retweets, group, name):
        centrality_process = centrality.centrality()

        in_degree_retweets, out_degree_retweets = centrality_process.in_out_centrality(retweets)
        in_degree_results = "IN DEGREE, " + str(group) + ", " + str(in_degree_retweets)
        self.file_controller.append_one_line("results/" + name + ".csv", in_degree_results)
        out_degree_results = "OUT DEGREE, " + str(group) + ", " + str(out_degree_retweets)
        self.file_controller.append_one_line("results/" + name + ".csv", out_degree_results)
        if not in_degree_retweets == None:
            in_degree_max = "In degree maximum for " + name + " from group " + str(group) + " is " + str(max(in_degree_retweets.values()))
            self.file_controller.append_one_line("results/" + name + "stats.txt", in_degree_max)

            out_degree_max = "Out degree maximum for " + name + " from group " + str(group) + " is " + str(max(out_degree_retweets.values()))
            self.file_controller.append_one_line("results/" + name + "stats.txt", out_degree_max)

            in_degree_min = "In degree minimum for " + name + " from group " + str(group) + " is " + str(min(in_degree_retweets.values()))
            self.file_controller.append_one_line("results/" + name + "stats.txt", in_degree_min)

            out_degree_min = "Out degree minimum for " + name + " from group " + str(group) + " is " + str(min(out_degree_retweets.values()))
            self.file_controller.append_one_line("results/" + name + "stats.txt", out_degree_min)

        betweenness = centrality_process.betweenness(retweets)
        betweenness_results = "BETWEENNESS," + str(group) + ", " + str(betweenness)
        self.file_controller.append_one_line("results/" + name + ".csv", betweenness_results)
        if not len(betweenness) == 0:
            betweenness_max = "Betweenness degree maximum for " + name + " from group " + str(group) + " is " + str(max(betweenness.values()))
            self.file_controller.append_one_line("results/" + name + "stats.txt", betweenness_max)

            betweenness_min = "Betweenness degree minimum for " + name + " from group " + str(group) + " is " + str(min(betweenness.values()))
            self.file_controller.append_one_line("results/" + name + "stats.txt", betweenness_min)

        closeness = centrality_process.closeness(retweets)
        closeness_results = "CLOSENESS, " + str(group) + ", " + str(closeness)
        self.file_controller.append_one_line("results/" + name + ".csv", closeness_results)
        if not len(closeness) == 0:
            closeness_max = "Closeness degree maximum for " + name + " from group " + str(group) + " is " + str(max(closeness.values()))
            self.file_controller.append_one_line("results/" + name + "stats.txt", closeness_max)

            closeness_min = "Closeness degree minimum for " + name + " from group " + str(group) + " is " + str(min(closeness.values()))
            self.file_controller.append_one_line("results/" + name + "stats.txt", closeness_min)

        eigenvector = centrality_process.eigenvector(retweets)
        eigenvector_results = "EIGENVECTOR, " + str(group) + ", " + str(eigenvector)
        self.file_controller.append_one_line("results/" + name + ".csv", eigenvector_results)
        if eigenvector:
            eigen_max = "Eigenvector degree maximum for " + name + " from group " + str(group) + " is " + str(max(eigenvector.values()))
            self.file_controller.append_one_line("results/" + name + "stats.txt", eigen_max)

            eigen_min = "Eigenvector degree minimum for " + name + " from group " + str(group) + " is " + str(min(eigenvector.values()))
            self.file_controller.append_one_line("results/" + name + "stats.txt", eigen_min)

        self.file_controller.append_one_line("results/" + name + "stats.txt", tie_results)
