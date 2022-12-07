# Hati.my Webscraper

Webscraper for [Hati.my](https://www.hati.my/)

2nd Version of webscraper (1st version died with laptop D:)

# How to run:

Make sure "main.py" and the .bat/.sh files are in the same folder.

HEADSUP- A couple of pip modules will be installed onto your machine

**If you're on Windows, run the .bat file**

**If you're on MAC/Linux,**

1. Open this directory in your terminal (right click in the folder and click 'open in terminal'

2. Copy paste the command below into the terminal

3. `chmod +x runMAC.sh`

4. Press enter

5. You should now be able to run the file as an executable by double clicking on the .sh file

6. If it still only brings up the text editor, run this command in your terminal

7. `./runMAC.sh`

# Dependencies
Requests: `pip install requests`

Beautiful Soup: `pip install beautifulsoup4`

# End
IF the program still does not run properly, do contact me

After executing the program, a terminal should appear counting through records.

It should also output a CSV file named "Hati NGOs"

The CSV file will have a maximum of 1000 records.

If the records scraped exceed that, the file will split into another CSV file
