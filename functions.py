#!/usr/bin/env python3

from variables import *
import requests

try: # IMPORTING CONFIG AS MODULE
    from config import *
except:
    pass

def check_config(debug="False"):
    """CHECKS IF CONFIG FILE IS PRESENT... IF NOT CREATE
    The values in the file are
    url: url of the nextcloud server
    user: username for the nextcloud server
    password: password of the nextcloud server

    Passing debug="True" returns whether config file was found"""

    # Check for config
    try:
        open("config.py",'r')
        if debug == "True":
            return 'Found Config'
        # Else we create it
    except:
        print("No config file found, creating now!")
        # Get paramaters
        url = input('Enter your nextcloud url: ')
        user = input('Enter your username: ')
        password = input('Enter your password: ')
        # Write to file
        with open ("config.py", 'a') as f:
            f.write(f"#!/usr/bin/python3\n \
                    url = \"{url}/ocs/v2.php/app/spreed/api/v4\"\n \
                    user = \"{user}\"\n \
                    password = \"{password}\"")
            print("App need to be restarted.. rerun")
            if debug == "True":
                return 'Needed to create config'
            exit(0)

def get_conversations(debug="False"):
    """
    Get the users conversations.

    Tries to load the conversations list from a json file (cached).
    If file can't be found they are fetched through the api and dumped to a file
    Alco check for dictionary dict_token_participant stored in a json file.
    This dictionary contains tokens of conversations as keys and display name as value.
    If file doesn't exist. Dictionary is created and dumped to a file

    debug="True" returns conversation in json format"""

    # Check for cache
    try:
        with open(f"{jsondir}/conversations.json", 'r') as lf:
            m_conversations = json.load(lf)
    # Else fetch conversations and create chche
    except:
        print("Fetching conversations...")
        r_conversations = requests.get(f"{url}/room", \
                                       headers=headers, \
                                       auth=(user,password))
        m_conversations= (r_conversations.json())
        with open(f"{jsondir}/conversations,json", 'w') as df:
            json.dump(m_conversations, df)

    # Check if the dictionary was populated
    # Else we create it

    if bool(dict_token_participant) == False:
        print("Creating dictionary")
        # Get count of conversations
        number_of_conversations = range(len(m_conversations["ocs"]["data"]))
        for i in number_of_conversations:
            token_i = (m_conversations["ocs"]["data"][i]["lastMessage"]["token"])
            # TODO: read participants instead of making new requests
            # TODO: group chats
            r_participants = requests.get(f"{url}/room/{token_i}/participants",\
                                         headers=headers,\
                                         auth=(user,password))
            m_participants = (r_participants.json())
            # TODO: Catch public convo otherwise "Index out of range"
            try:
                participant_i = (m_participants["ocs"]["data"][1]["displayName"])
            except:
                participant_i = f"Public Conversation {i}"
            dict_token_participant.update({token_i : participant_i})
            # Write dictionary to json file
            with open(f"{jsondir}/dictionary.json",'w') as df:
                json.dump(dict_token_participant, df)

    if debug == "True":
        return m_conversations

def list_conversations():
        """
        List the users conversations
        Creates an empty list called list_of_conversations and then populates it with tokens and participants from the dict_token_participant dictionary
        Function returns the list
        """
        # TODO: Sort conversation by date of last message

        list_of_conversations = []
        for k, v in dict_token_participant.items():
            print(v)
            list_of_conversations.append(v)
        print("\n")
        return list_of_conversations

def get_messages(conversation):
        """
        Get the messages of a specific conversation.

        The function takes the displayname as an argument
        It then looks up the corresponding token
        It checks whether a file containing the messages already exists, else fetch through api.
        Printed in reverse order.
        """

        chat_url = url[:-1]+"1"
        # Find token in dictionary
        for key, value in dict_token_participant.items():
            if value == conversation:
                token = key
                break
        try:
            with open(f"{jsondir}/{conversation}.json",'r') as lf:
               m_messages=json.load(lf)
            # If no cache file, fetch messages and create
        except:
            print(f"Fetching new messages for {conversation}")
            r_messages = requests.get( f"{chat_url}/chat/{token}", \
                                       headers=headers, \
                                       auth=(user, password), \
                                       params=data_chat)
            m_messages = (r_messages.json())
            with open(f"{jsondir}/{conversation}.json",'w') as df:
                json.dump(m_messages, df)

        # Get the number of messages
        number_of_messages = range(len(m_messages["ocs"]["data"]))
        for i in reversed(number_of_messages):

            print(m_messages["ocs"]["data"][i]["actorDisplayName"] + ": ")
            print(m_messages["ocs"]["data"][i]["message"])
            print("\n")


def send_msg(conversation, msg):
    """
    Send a message to a chat

    The function takes conversation and message as arguments
    Looks up token for conversation in dictionary and sends message through api
    """

    # Get the token from the dictionary
    for key, value in dict_token_participant.item():
        if value == conversation:
            token = key
            break
    # Send the message
    send = requests.post(f"{url}/chat/{token}",
                         headers=headers,\
                         auth=(user,password),\
                         params={'message':msg})

def autocomplete(input_string, choose_from):
    """
    Auto completes a string

    This function autocompletes a given string with a list of options.
    Paramaters:
        input_string: input to autocomplete
        choose_from: list of options
    """
    filter_input = list(filter(lambda x: x.startswith(input_string), choose_from))
    return filter_input[0]

# TODO: FIX
def autofetch_messages():
    """
    Autofetch periodically

    Function will automatically refetch messages in the background - NOT WORKING
    """
    for key, value in dict_token_participant.items():
        print(f"Polling token {key} conversation {value}")
        r_autofetch = requests.get( f"{url}/chage/{key}", \
                                    headers=headers, \
                                    auth=(user, password), \
                                    params=data_chat)
        m_autofetch = (r_autofetch.json())
        with open(f"{jsondir}/{value}.json",'w') as df:
            json.dump(m_autofetch, df)
