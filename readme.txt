/**********************************************************************
 *  PollEV Bot
 **********************************************************************/
//Copyright (C) 2021 Sal Sicari
Name:Sal Sicari
Time spent: Worked on throughout a 2 week period
/**********************************************************************
 *  IMPORTANT
 **********************************************************************/
Due to a recent update the xpath changed, I have updated them on my own personal code, but not here. 
/**********************************************************************
 *  What the program does
 **********************************************************************/
This program will open up pollev and sign in to an account and join a specific presentation and run for a set amount of time, based on the user input data. It is also running in the background in headless mode. 
It could also be hard coded in if you would like. It uses selenium in a while loop witha try catch block, to check if a question is being asked based on the page HTML. When a question is asked and the HTML changes 
and can't be found it throws an exception and will pick a question using a selenium feature. It picks the answers either A or B based off a random number generator. After this, in another while loop with a try catch block, 
it updates the page about ever 30 seconds and using another selenium feature it checks to see if the orginal HTML from the webpage where no question being asked is found. If it is not found it throws an exception and refreshes the page
and starts the loop again, until it is found or the program ends. When it is found this will mean it's put back into the orginal loop of no question being asked and it will wait for another question. I use the
time.perf_counter() feature to keep track of the time and check a conditional in the main loop to see if it should break the loop when reaching the given time. After the main loop hits the total run time and stops
my program goes to the pollEV response history page and clicks the export data button, then it closes the program entirely. The export data feature from PollEV will send the email from the account your response data
in an organized spreadsheet. I experimented with setting this up on google cloud but could not get it running on a set schedule.


/**********************************************************************
 * Problems Encountered
 **********************************************************************/
I wrote this entire thing and realised I would run into problems later down the line, so I rewrote it adding new features and I used a completely different implementation.
I ran into many problems as this was my first time coding in python and using selenium. I worked through a lot of it easily after learning some fundemental concepts of web pages and interacting with them. As well as using 
Beautiful Soup to print webpage values to compare certain aspects and help locate and debug a few problems.Although I do not use BeautifulSoup for any other parsing as I am not scraping data. One problem I ran into that caused 
me the most trouble was sometimes the webpage wouldn't update when a question was deactivated, to fix this I made a feature that could refresh the webpage, but this also affected the process that came after answering a question. 
After answering a question if it wasn't deactivated fast enough the checker that was suppose to check if the webpage got stuck would kick in when it shouldn't have. To fix this I combined the features but this led to another problem.
When I used driver.refresh() it woul break out of my while loop and screw up the cycle the program should follow. To fix this I had to refresh the webpage in a different manner. 
action = webdriver.ActionChains(driver) 
action.key_down(Keys.CONTROL).send_keys(Keys.F5).perform()
This would regresh the page without breaking out of the loop and derailing my program.
Lastly when testing the time of my program it closes the driver at the correct time, but for the program to completley stop and end, it normally runs between 10-30 extra seconds. I have been unable to find the exact reasoning and
a few solutions I have tried seemed to screw up the time worse, and could lead to possibly ending the program to early. I just left it as is for now assuming the problem might be based off my own machine specs. 



/**********************************************************************
 * Experienced Gained
 **********************************************************************/
Overall I would say I gained a lot of experience. Of course I learned a lot of basic python and learned some fundamentals of how webpages work and how to interact with them autonomously and even basic scraping. I used selenium
and Beautiful soup and learned a lot about these as well. I also gained invaluable experience of working through problems on my own and finding resources to learn and help. Unlike in school there is no teacher to ask or tutors to 
go to. Having to find solutions on my own and using online resources to figure out my problems has taught me a lot over this project. 

EDIT*
PollEV updated their website causing the xpaths to change, requiring me to update them all in my code. In the future if I could minimize use of web elements subject to change I would, as a way to try to prevent the need for long changes to your code if a website updates.


/**********************************************************************
 * What to add in the future
 **********************************************************************/
A few ideas I would like to add to this in the future would be to make the time more accurate. I would also like for PollEV to add a clear buttopn on response history, so the data you get are from your last poll only. I would like 
to see if I can get it up and running on a schedule using google cloud. 

/**********************************************************************
 * Disclaimer
 **********************************************************************/
I do not promote or condone the usage of this script for any kind of academic misconduct or dishonesty. I wrote this script solely to educate myself on web automation and exposing myself to coding in python and using 
such features as Selenium and Beautifulsoup, and cannot be held liable for any indirect, incidental, consequential, special, or exemplary damages arising out of or in connection with the usage of this script. 

