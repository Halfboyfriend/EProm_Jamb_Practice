import time


def countdown_timer(duration):
    
    for x in range(duration, 0, -1):
        seconds = x % 60
        minutes = int(x / 60) % 60
        hour = int(x / 3600)
        
        return f"{hour}:{minutes:02}:{seconds:02} + {time.sleep(1)}"

    

# Set the duration to 1 hour (3600 seconds)


print(countdown_timer(30))
