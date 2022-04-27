""" 
COMP 593 - Final Project

Description: 
  Downloads NASA's Astronomy Picture of the Day (APOD) from a specified date
  and sets it as the desktop background image.

Usage:
  python apod_desktop.py image_dir_path [apod_date]

Parameters:
  image_dir_path = Full path of directory in which APOD image is stored
  apod_date = APOD image date (format: YYYY-MM-DD)

History:
  Date        Author    Description
  2022-03-11  J.Dalby   Initial creation
  2022-03-27  J.Murphy  Started work
  2022-04-27  J.Murphy  Completion (and hopefully perfection)
"""
from select import select
from sys import argv, exit
from datetime import datetime, date
from hashlib import sha256
from os import path, mkdir
import sqlite3
import requests

def main():

    # Determine the paths where files are stored
    image_dir_path = get_image_dir_path()
    db_path = path.join(image_dir_path, 'apod_images.db')

    # Get the APOD date, if specified as a parameter
    apod_date = get_apod_date()

    # Create the images database if it does not already exist
    create_image_db(db_path)

    # Get info for the APOD
    apod_info_dict = get_apod_info(apod_date)
    
    # Download today's APOD
    image_url = 'https://apod.nasa.gov/apod/astropix.html'
    image_msg = download_apod_image(image_url)
    image_sha256 = sha256(image_msg)
    image_size = len(image_msg)
    image_path = get_image_path(image_url, image_dir_path)

    # Print APOD image information
    print_apod_info(image_url, image_path, image_size, image_sha256)

    # Add image to cache if not already present
    if not image_already_in_db(db_path, image_sha256):
        save_image_file(image_msg, image_path)
        add_image_to_db(db_path, image_path, image_size, image_sha256)

    # Set the desktop background image to the selected APOD
    set_desktop_background_image(image_path)

def get_image_dir_path():
    """
    Validates the command line parameter that specifies the path
    in which all downloaded images are saved locally.

    :returns: Path of directory in which images are saved locally
    """
    if len(argv) >= 2:
        dir_path = argv[1]
        if path.isdir(dir_path):
            print("Images directory:", dir_path)
            return dir_path
        else:
            print('Error: Non-existent directory', dir_path)
            exit('Script execution aborted')
    else:
        print('Error: Missing path parameter.')
        exit('Script execution aborted')

def get_apod_date():
    """
    Validates the command line parameter that specifies the APOD date.
    Aborts script execution if date format is invalid.

    :returns: APOD date as a string in 'YYYY-MM-DD' format
    """    
    if len(argv) >= 3:
        # Date parameter has been provided, so get it
        apod_date = argv[2]

        # Validate the date parameter format
        try:
            datetime.strptime(apod_date, '%Y-%m-%d')
        except ValueError:
            print('Error: Incorrect date format; Should be YYYY-MM-DD')
            exit('Script execution aborted')
    else:
        # No date parameter has been provided, so use today's date
        apod_date = date.today().isoformat()
    
    print("APOD date:", apod_date)
    return apod_date

def get_image_path(image_url, dir_path):
    """
    Determines the path at which an image downloaded from
    a specified URL is saved locally.

    :param image_url: URL of image
    :param dir_path: Path of directory in which image is saved locally
    :returns: Path at which image is saved locally
    """
    
    image_link = image_url.split('/')[-1]

    img_dir = path.join(dir_path, image_link)
    if not path.isdir(img_dir):
        mkdir(img_dir)
    
    return img_dir



def get_apod_info(date):
    """
    Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    :param date: APOD date formatted as YYYY-MM-DD
    :returns: Dictionary of APOD info
    """    
    URL = "https://api.nasa.gov/planetary/apod"
    api_key = "5V5z2c322vMg4bcKiiIZrMPkPWMCKqxHRNcRqngO"
    params = {
      'api_key':api_key,
      'date':date,
      'thumbs':'True'
    }
    URL = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(URL, params=params)

    if response.status_code == 200:
        print ('success!')
        return(params)
    else:
        print ('failed. Error code', response.status_code)

def print_apod_info(image_url, image_path, image_size, image_sha256):
    """
    Prints information about the APOD

    :param image_url: URL of image
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """    
    print("Saved from:", image_url)
    print("Saved at:", image_path)
    print("Size:", image_size, "bytes")
    print("SHA-256:", image_sha256)
    return

def download_apod_image(image_url):
    """
    Downloads an image from a specified URL.

    :param image_url: URL of image
    :returns: Response message that contains image data
    """
    print('Downloading image from URL...')
    response = requests.get(image_url)

    if response.status_code == 200:
        print("success!")
        return response.content
    else:
        print("failed. Response code", response.status_code)
        return

def save_image_file(image_msg, image_path):
    """
    Extracts an image file from an HTTP response message
    and saves the image file to disk.

    :param image_msg: HTTP response message
    :param image_path: Path to save image file
    :returns: None
    """
    return #TODO

def create_image_db(db_path):
    """
    Creates an image database if it doesn't already exist.

    :param db_path: Path of .db file
    :returns: None
    """

    myConnection = sqlite3.connect(db_path)
    myCursor = myConnection.cursor()

    apodTable = """CREATE TABLE IF NOT EXISTS apod_images (
            date text NOT NULL,
            size integer NOT NULL,
            sha256 text NOT NULL,
            downloaded_at datetime NOT NULL
    );"""
    
    myCursor.execute(apodTable)
    #myCursor.commit()
    #myCursor.close()

def add_image_to_db(db_path, image_path, image_size, image_sha256):
    """
    Adds a specified APOD image to the DB.

    :param db_path: Path of .db file
    :param image_path: Path of the image file saved locally
    :param image_size: Size of image in bytes
    :param image_sha256: SHA-256 of image
    :returns: None
    """
    return #TODO

def image_already_in_db(db_path, image_sha256):
    """
    Determines whether the image in a response message is already present
    in the DB by comparing its SHA-256 to those in the DB.

    :param db_path: Path of .db file
    :param image_sha256: SHA-256 of image
    :returns: True if image is already in DB; False otherwise
    """ 
    myConnection = sqlite3.connect(db_path)
    myCursor = myConnection.cursor()

    selectStatement = """SELECT date FROM apod_images
    WHERE sha256 = image_sha256"""

    myCursor.execute(selectStatement)
    if selectStatement:
        return True
    else:
        return False

def set_desktop_background_image(image_path):
    """
    Changes the desktop wallpaper to a specific image.

    :param image_path: Path of image file
    :returns: None
    """
    return #TODO

main()