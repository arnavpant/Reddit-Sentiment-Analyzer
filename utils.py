# utils.py

def get_sentiment_feeling(score):
    # Positive
    if 0.0 <= score < 0.1:
        return "Feels like stale chips, you couldn’t care less."
    elif 0.1 <= score < 0.2:
        return "It’s a shrug. Like when you see two clouds that kind of look like a dog."
    elif 0.2 <= score < 0.3:
        return "Not bad, like finding five bucks in your pocket."
    elif 0.3 <= score < 0.4:
        return "Feels like someone held the door open for you."
    elif 0.4 <= score < 0.5:
        return "Feels like you just got a text from your crush. Life’s alright."
    elif 0.5 <= score < 0.6:
        return "Feels like you got the last slice of pizza at the party."
    elif 0.6 <= score < 0.7:
        return "Feels like your favorite song just came on shuffle. Good vibes only."
    elif 0.7 <= score < 0.8:
        return "Feels like you aced the test you forgot to study for."
    elif 0.8 <= score < 0.9:
        return "Feels like you just won concert tickets on the radio."
    elif 0.9 <= score <= 1.0:
        return "Feels like you woke up and it’s Saturday. Forever. Pure joy."
    # Negative
    elif -0.1 <= score < 0.0:
        return "Comparable to you dropping your toast and it landing butter-side down."
    elif -0.2 <= score < -0.1:
        return "Feels like you stepped in a puddle wearing socks."
    elif -0.3 <= score < -0.2:
        return "Like you missed the bus by just two seconds."
    elif -0.4 <= score < -0.3:
        return "Feels like your phone died right before you could send that risky text."
    elif -0.5 <= score < -0.4:
        return "Feels like You spilled coffee on your only clean shirt."
    elif -0.6 <= score < -0.5:
        return "It’s raining, you forgot your umbrella, and you’re late."
    elif -0.7 <= score < -0.6:
        return "Your pet just knocked over your favorite mug."
    elif -0.8 <= score < -0.7:
        return "You lost your wallet on vacation."
    elif -0.9 <= score < -0.8:
        return "Your hard drive crashed and you never backed up your files."
    elif -1.0 <= score < -0.9:
        return "World War 3 just started and you got drafted. That’s how rough it feels."
    else:
        return "No mood detected."

def get_sentiment_emoji(score):
    if score > 0.1:
        return "😊"
    elif score < -0.1:
        return "😞"
    else:
        return "😐"

