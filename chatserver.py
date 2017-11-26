from fbchat import Client
from fbchat.models import *
import threading
from queue import *
import traceback
import sentence_tokenizer

print("Loading data...")
import dataloading
import dataprocessing
import pickle
from random import *
import time

message_queue = Queue()
send_queue = Queue()

with open('greetings', 'r') as file:
    greetings = file.read().strip().split('\n')

responseDict = pickle.load(open('data/man.karl','rb'))

with open('friends', 'r') as file:
    friends = file.read().strip().split('\n')

# Logs in
with open('creds', 'r') as file:
    user, passw = file.read().strip().split('\n')[0:2]

# Receives messages off FB
class Receiver(Client):

    # Function called when message received
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        try:
            if author_id not in friends:
                friends.append(author_id)
                with open('friends', 'w') as file:
                    for line in friends:
                        file.write(line + '\n')

            # Ensures person sending message is not self
            if author_id != self.uid:
                message_queue.put([message_object.text, thread_id, thread_type, int(time.time()) + randint(2, 7)])

                self.setTypingStatus(TypingStatus.TYPING, thread_id=thread_id, thread_type=thread_type)

            # Marks message as read
            self.markAsDelivered(author_id, thread_id)
            self.markAsRead(author_id)
        except:
            print("Error")
            print(traceback.print_exc())

# Send messages to FB
class Sender(Client):
    def onLoggedIn(self, email=None):

        # Sends from queue
        while True:
            try:
                print("Trying to get from Queue")
                s = send_queue.get()

                self.send(*s)

            except:
                print("Error")
                print(traceback.print_exc())

# Starts threads
def message_listener():
    get_client = Receiver(user, passw)
    get_client.listen()

def message_sender():
    send_client = Sender(user, passw)
    send_client.listen()

def processor():
    while True:
        try:
            thing = message_queue.get()

            if thing[3] <= int(time.time()):
                for _ in range(choice([1, 1, 1, 1, 2, 3, 4, 5])):
                    breakdown = sentence_tokenizer.sorting_pos(thing[0])

                    out = ' '.join(dataprocessing.findResponse(responseDict, breakdown))
                    print(thing)
                    send_queue.put((Message(out), thing[1],thing[2]))

                    thing[0] = ' '.join(breakdown)
            else:
                message_queue.put(thing)

        except:
            print("Error")
            print(traceback.print_exc())

def hello():
    while True:
        if randint(0, 3000) == 0:
            send_queue.put((Message(choice(greetings)), choice(friends), ThreadType.USER))

        time.sleep(1)

message_receiver = threading.Thread(target=message_listener)
message_receiver.start()

message_sender = threading.Thread(target=message_sender)
message_sender.start()

message_processor = threading.Thread(target=processor)
message_processor.start()

hello_thread = threading.Thread(target=hello)
hello_thread.start()
