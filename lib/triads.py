from database import mongoController
from lib import interactiongraph, fileController

# Calculates triads for a given dataset
class triads():

    # Calculates triads and write to file
    def calculate_triads(self):
        file_controller = fileController.fileController()
        file_controller.append_one_line("results/triads.txt", "")
        file_controller.write_data_to_file("results/triads.txt", "")
        triads = self.all_triads()
        all_triads = "Total Triads : " + str(len(triads)) + "\n" + str(triads)
        file_controller.append_one_line("results/triads.txt", all_triads)

        for i in range(20):
            triads = self.all_triads_group(i)
            group_triads = "Triads for group " + str(i) + " - " + str(len(triads)) + "\n" + str(triads)
            file_controller.append_one_line("results/triads.txt", group_triads)

    # returns the amount of triads found overall
    def triads_length(self):
        triads = self.all_triads()
        if triads is None:
            return None
        else:
            return len(triads)

    # returns an list of triads where each element is a list of size 3. One for the user ID of each node in the triad
    def all_triads(self):
        interact_graph = interactiongraph.interactiongraph()

        quote_network = interact_graph.quotes()
        quote_triads = self.triads(quote_network)

        retweet_network = interact_graph.retweets()
        retweet_triads = self.triads(retweet_network)

        reply_network = interact_graph.replies()
        reply_triads = self.triads(reply_network)

        return self.build_triads(quote_triads, retweet_triads, reply_triads)

    # returns amount of triads in a given ground
    def triads_length_group(self, group):
        triads = self.all_triads_group(group)
        if triads is None:
            return None
        else:
            return len(triads)

    # returns an list of triads where each element is a list of size 3. One for the user ID of each node in the triad
    def all_triads_group(self, group):
        interact_graph = interactiongraph.interactiongraph()

        quote_network = interact_graph.quotes_group(group)
        quote_triads = self.triads(quote_network)

        retweet_network = interact_graph.retweets_group(group)
        retweet_triads = self.triads(retweet_network)

        reply_network = interact_graph.replies_group(group)
        reply_triads = self.triads(reply_network)

        return self.build_triads(quote_triads, retweet_triads, reply_triads)

    # Takes individual triad groups and combines them into a single triad list
    def build_triads(self, quote_triads, retweet_triads, reply_triads):
        final_triads = []

        for quote_triad in quote_triads:
            if not quote_triad in final_triads:
                final_triads.append(quote_triad)
        for retweet_triad in retweet_triads:
            if not retweet_triad in final_triads:
                final_triads.append(retweet_triad)
        for reply_triad in reply_triads:
            if not reply_triad in final_triads:
                final_triads.append(reply_triad)

        return final_triads

    # Main computation for triads
    # Loops through each user, each user that is connected to the initial user, and all the users connected to secondary user
    # Looks for the first users id at this level. If the ID is found we know there is a triad
    def triads(self, data):
        triads = []
        for key, first_value in data.items():
            for second_value in first_value:
                if second_value in data and not second_value == key:
                    for third_value in data[second_value]:
                        if third_value in data and key in data[third_value].keys() and not third_value == key and not third_value == second_value:
                            triads.append([key, second_value, third_value])

        return triads
