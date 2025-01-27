'''Dependencies'''
import googlemaps as gm
from datetime import datetime
from dev_only import gmap_api, choose_location
from dev_only import twilio_envestor_sid, twilio_envestor_token, twilio_phone_number, my_num
import time
from datetime import datetime, time as dt_time
from twilio.rest import Client #Twilio Module
#import smtplib #email notification module
#from email.mime.text import MIMEText

#Initialise your text messaging client with right credentials
twilio_client = Client(twilio_envestor_sid, twilio_envestor_token)

#Initialise your google maps client with your API key
gmaps = gm.Client(key=gmap_api)

#if address use format("Stretford, Manchester, UK", "Stamford Bridge, London, Uk")
#if postcode use format("E1 6AN, UK", "EC1A 1BB, UK")
#start_loc = str(input("What is the starting location?: " ))
#end_loc = str(input("What is the final destination?: " ))

start_loc = choose_location[0]
end_loc = 'Crescent Road, Brentwood'

print('getting route')
def get_route_info(start_loc, end_loc):
    '''Get the start and ending locations'''
    time_now = datetime.now()

    our_route = gmaps.directions(
        start_loc,
        end_loc,
        mode="driving",
        departure_time=time_now,
        traffic_model="best_guess")
    
    return our_route

route_info = get_route_info(start_loc, end_loc)

time_in_traffic_seconds = route_info[0]['legs'][0]['duration_in_traffic']['value']

time_in_minutes = int(time_in_traffic_seconds / 60)

def time_checker():
    '''Function to return journey time message'''
    journey_time = f"{time_in_minutes} minutes to get to {end_loc}, please drive safely."
    print("Checking... ")  # Print for console output
    return journey_time  # Return the string instead of the print result

route_time = time_checker()
minutes = 1
max_time = (minutes * 60)

to_number = my_num

def send_sms(to_number, message):
    ''''Function to send SMS using Twilio'''
    try: 
        message = twilio_client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=to_number
        )
        print(f"Msg sent successfully to {to_number}")
    except Exception as e:
        print(f"Failed to send msg: {e}")

def timed_printer(r_time=0, max_time=max_time, phone_number=to_number):
    ''' Function to return journey_time a finite number of times and send to my phone'''
    minutes = 1
    max_time = (minutes * 60)

    while r_time < max_time:
        send_sms(phone_number, route_time)
        time.sleep(300)
        r_time += 300


def time_printer(phone_number=to_number):
     ''' Function to return journey_time within specific time periods and send to my phone'''
     #Allowed days (Mon=0, Tues=1, Wed=2, Thurs=3, Fri=4, Sat=5, Sun=6)
     allowed_days = [0, 2, 3, 4]
    #Time window for running (07:40am to (08:15am) on a 24hr clock
     start_time = dt_time(7, 40)
     end_time = dt_time(8, 15)


    
    #use the datetime module to find where in time we are
     now = datetime.now()
     currnet_day = now.weekday() #find the day
     current_time = now.time() #find the time in that day

    #Handle time window that crosses midnight
     if (currnet_day in allowed_days and (
         (start_time <= current_time) or (current_time <= end_time)
         if start_time > end_time #Time Window crosses midnight
         else start_time <= current_time <= end_time
         )
     ):
        send_sms(phone_number, route_time)
        time.sleep(300)
        print("Message sent!")
     else:
        print("Not within the allowed time window. Waiting...")
        time.sleep(60)



def run_continously():
    '''Main Loop to run continuously'''

    while True:
        try:
            time_printer()
        except KeyboardInterrupt:
            print("Program stopped by user")
            break
        except Exception as e:
            print(f"An error occurred as {e}")
            time.sleep(60)


run_continously()













   