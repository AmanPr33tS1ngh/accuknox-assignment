##### TOPIC : DJANGO SIGNALS #####

'''
Question 1:
By default are django signals executed synchronously or asynchronously? support your answer with a code snippet that
conclusively proves your stance.
'''

'''
Answer:
By default, Django signals are executed synchronously. When we emit a signal using signal.send(), the receivers are called in the
same thread of execution
In the below code snippet, the user_created function is connected to the post_save signal of the User model. When a new user is created
the user_created function is called synchronously as it is being executed in the same thread
'''

# Code Snippet:

# Imports
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        print("User created:", instance.username)

# user created function will be called while creating a user
user = User.objects.create(username='test_user', password='password')


'''
Question 2:
Do django signals run in the same thread as the caller? Please support your answer with a code snippet that conclusively proves your
stance
'''

'''
Answer:
Yes, Django signals run synchronously in the same thread as the caller.
In the below code snippet, the user_created function is connected to the post_save signal of the User model like above and nside the 
function we print the name of the current thread using threading.current_thread().name
'''

# Code Snippet:
#Imports
import threading

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    thread_name = threading.current_thread().name
    print(f"User created in thread: {thread_name}")

user = User.objects.create(username='test_user', password='password')


'''
Querstion: 
By default do djsngo signals run in the same database transaction as the caller? Please support your answer with a code snippet that conclusively proves your stance
'''
'''Answer: 
Yes, by default django signals run in the same database transaction as the caller. It ensures that any actions performed
within the signal handlers are part of the same transaction as the original operation that triggered the signal

In the below code snippet we define a signal handler (user_created like above) which is connected to the post_save signal of the User
model.
Inside the signal handler, we are printing the count of User objects before and after the commit.
We create a user within a transaction using transaction.atomic().
After creating the user, we are printing the count of User objects again (both within and outside the transaction).
'''

from django.db import transaction

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    print("Inside signal handler - Before commit:", User.objects.count())

    # database operation inside the signal handler
    if created:
        print("Creating a new user inside signal handler")
        User.objects.create(username='new_user', password='password')

    print("Inside signal handler - After commit:", User.objects.count())

# creating a user within a transaction
with transaction.atomic():
    user = User.objects.create(username='test_user', password='password')
    print("User created synchronously within a transaction:", User.objects.count())


##### TOPIC : CUSTOM CLASSES IN PYTHON #####

# Creating reactangle class
class Rectangle:
    def __init__(self, length: int, width: int): #intialization
        self.length = length
        self.width = width

    def __iter__(self): #iterator
        return RectangleIterator(self)

class RectangleIterator:#iterator class
    def __init__(self, rectangle: Rectangle):
        self.rectangle = rectangle
        self.iterated = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self.iterated:
            self.iterated = 'width' # we can customize this value to change the behaviour
            return {'length': self.rectangle.length}
        elif self.iterated == 'width':
            self.iterated = 'end'
            return {'width': self.rectangle.width}
        else:
            raise StopIteration

rec = Rectangle(width=100, length=100)
for item in rec:
    print(item)
    
# DONE