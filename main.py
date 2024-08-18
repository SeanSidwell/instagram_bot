import os
import logging
import time
from instabot import Bot
from dotenv import load_dotenv

load_dotenv()

#Please Edit these with your login credentials and your desired message
ig_username = "YourUsernameHere"
ig_password = "YourPasswordHere"

dm_message = "Thank you for your comment!"
post_url = "YourLinkHere"


# Setup logging to console
logger = logging.getLogger()
logger.setLevel(logging.WARNING)

# Initialize the bot
bot = Bot()

# Path to the session file
session_file = f"config/{ig_username}_uuid_and_cookie.json"

# Delete the cookie file if it exists
if os.path.exists(session_file):
    print(f"Deleting existing session file: {session_file}")
    os.remove(session_file)

# Login to Instagram
print("Logging in...")
bot.login(username=ig_username, password=ig_password)

# Function to send DM to each unique commenter
def send_dm_to_unique_commenters(post_url):
    try:
        post_id = bot.get_media_id_from_link(post_url)
        
        # Optional: Add a delay to avoid hitting rate limits
        time.sleep(2)
        
        # Retrieve the list of commenters
        commenters = bot.get_media_commenters(post_id)
        
        if not commenters:
            print("No commenters found or failed to retrieve commenters.")
            logger.info("No commenters found or failed to retrieve commenters.")
            return
        
        # Remove duplicates by converting to a set
        unique_commenters = set(commenters)
        
        print(f"Found {len(unique_commenters)} unique commenters. Sending DMs...")
        logger.info(f"Found {len(unique_commenters)} unique commenters. Sending DMs...")
        
        for commenter in unique_commenters:
            try:
                bot.send_message(dm_message, [commenter])
                print(f"Sent DM to {commenter}")
                logger.info(f"Successfully sent DM to {commenter}")

                # Optional: Add a delay between DMs to avoid rate limits
                time.sleep(3)
            except Exception as e:
                print(f"Failed to send DM to {commenter}: {e}")
                logger.error(f"Failed to send DM to {commenter}: {e}")

                
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")


# Function Call
send_dm_to_unique_commenters(post_url)
