#!/usr/bin/python3
from functions import *
if __name__ == "__main__":
    # Clear screen
    os.system('clear')

    # check config file
    check_config()

    # Fetch conversations
    get_conversations()

    # TODO: This nested loop is stupid.
    # Start main loop
    while True:
        os.system('clear')
        # Get convo list
        printed_conversations = list_conversations()
        # Get user input of conversations
        user_input = input("Please enter the name of a conversation (type 'q' to exit) : ")
        # Check if we need to break loop
        if user_input == "q":
            print("Exiting")
            break
        conversation = autocomplete(input_string=user_input,choose_from=list_conversations())
        # Start second infinite loop
        # HACK PLEASE THIS IS SO BAD
        while True:
            os.system('clear')
            # Fetch messages from the given conversation
            get_messages(conversation)
            # Ask for user input
            msg = input("Send message (type 'q' to go back, 'l' to reload the messages) : ")
            # if user typed q, go back to conversations list
            if msg == "q":
                break

            # if user typed l, refetch messages
            elif msg == "l":
                # Remove cache to force refetch
                os.remove(f"{jsondir}/{conversation}.json")
                continue
            # Else we send message and refetch them
        else:
            send_msg(conversation, msg)
            os.remove(f"{jsondir}/{conversation}.json")
            continue
