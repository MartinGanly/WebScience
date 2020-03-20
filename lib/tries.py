from database import mongoController
from lib import interactiongraph, fileController

# Calculates tries for a given dataset
class tries():

    # Calculates tries and write to file
    def calculate_tries(self):
        file_controller = fileController.fileController()
        file_controller.append_one_line("results/tries.txt", "")
        file_controller.write_data_to_file("results/tries.txt", "")
        tries = self.all_tries()
        all_tries = "Total Tries : " + str(len(tries)) + "\n" + str(tries)
        file_controller.append_one_line("results/tries.txt", all_tries)

        for i in range(20):
            tries = self.all_tries_group(i)
            group_tries = "Tries for group " + str(i) + " - " + str(len(tries)) + "\n" + str(tries)
            file_controller.append_one_line("results/tries.txt", group_tries)

    # returns the amount of tries found overall
    def tries_length(self):
        tries = self.all_tries()
        if tries is None:
            return None
        else:
            return len(tries)

    # returns an list of tries where each element is a list of size 3. One for the user ID of each node in the trie
    def all_tries(self):
        interact_graph = interactiongraph.interactiongraph()

        quote_network = interact_graph.quotes()
        quote_tries = self.tries(quote_network)

        retweet_network = interact_graph.retweets()
        retweet_tries = self.tries(retweet_network)

        reply_network = interact_graph.replies()
        reply_tries = self.tries(reply_network)

        return self.build_tries(quote_tries, retweet_tries, reply_tries)

    # returns an list of tries where each element is a list of size 3. One for the user ID of each node in the trie
    def all_tries_group(self, group):
        interact_graph = interactiongraph.interactiongraph()

        quote_network = interact_graph.quotes_group(group)
        quote_tries = self.tries(quote_network)

        retweet_network = interact_graph.retweets_group(group)
        retweet_tries = self.tries(retweet_network)

        reply_network = interact_graph.replies_group(group)
        reply_tries = self.tries(reply_network)

        return self.build_tries(quote_tries, retweet_tries, reply_tries)

    # Takes individual triad groups and combines them into a single trie list
    def build_tries(self, quote_tries, retweet_tries, reply_tries):
        final_tries = []

        for quote_trie in quote_tries:
            if not quote_trie in final_tries:
                final_tries.append(quote_trie)
        for retweet_trie in retweet_tries:
            if not retweet_trie in final_tries:
                final_tries.append(retweet_trie)
        for reply_trie in reply_tries:
            if not reply_trie in final_tries:
                final_tries.append(reply_trie)

        return final_tries

    # Main computation for tries
    # Loops through each user, each user that is connected to the initial user and adds that user to a trie
    def tries(self, data):
        tries = []
        for key, first_value in data.items():
            for second_value in first_value:
                if second_value in data and not second_value == key:
                    tries.append([key, second_value])
        return tries
