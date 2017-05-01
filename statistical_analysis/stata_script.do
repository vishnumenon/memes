#the following is a script containing a selection of commands i ran on my data
#files.  running this script would not be a great idea, as it would produce
#a ton of unnecessary graphics, and is not meant to be run as presented
#unfortunately, there isn't a good way to present STATA commands and visualizations
#if you're interested in running this, there's a ton you'll need to comment out
#further, this is not nearly the extent of the number of commands I tried, as
#most were unsuccessful, but would cause this script to break
#treat this less as a runnable script and more as a summary of my more successful
#statistical investigations

#create proper year variable out of created_utc
gen yrs = created_utc / (60*60*24*365.25)
gen yr = 1970 + yrs

#create a bunch of score variables consisting exclusively of comments with
#higher scores
tabulate score
tabstat score, statistics(mean range sd variance skewness kurtosis median)
gen score_2 = score if score>=2
summarize score_2, detail
gen score_4 = score if score>=4
summarize score_4, detail
gen score_10 = score if score>=10
summarize score_10, detail
gen score_50 = score if score>=50
summarize score_50, detail
histogram score_50, discrete
gen score_100 = score if score>=100
summarize score_100, detail
twoway (scatter score_50 yr, sort)
gen score_250 = score if score>=250
summarize score_250, detail
tabstat score_250, statistics(mean range sd variance skewness kurtosis median)
gen score_500 = score if score>=500
summarize score_500, detail

#investigate score variables
twoway (scatter score_250 yr, sort)
twoway (scatter score yr, sort) (scatter score_50 yr, sort)
twoway (scatter score_100 yr, sort)
twoway (scatter score yr, sort) (scatter score_100 yr, sort) (scatter 250 yr, sort)

#install egenmore package to work parse comments for word count
ssc install egenmore
egen wordcount = nwords(body)

summarize wordcount, detail
tabulate wordcount
scatter wordcount score
scatter wordcount controversiality
histogram wordcount, discrete
scatter wordcount score_250
scatter wordcount score_10
tabstat wordcount, statistics(mean range sd variance skewness kurtosis median)


#the above is very interesting, it's clear that more highly related comments
#exclusively contain the meme, while lower rated comments have more text

#generate variables for a few important subreddits to compare their distributions
#of top-rated comments
tabulate subreddit
gen askreddit = 1 if subreddit =="AskReddit"
gen thanksobama = 2 if subreddit == "ThanksObama"
gen adviceanimals = 3 if subreddit == "AdviceAnimals"
gen politics = 4 if subreddit == "politics"
gen worldnews = 5 if subreddit == "worldnews"
gen videos = 6 if subreddit == "videos"

scatter askreddit thanksobama adviceanimals politics worldnews videos score_500
scatter askreddit thanksobama adviceanimals politics worldnews videos score_250
scatter askreddit thanksobama adviceanimals politics worldnews videos score_100

#generate categorical (dummy) variables to eek out the effect of a given subreddit
#on score, example here is for thanksobama, though this process is applicable
#to any meme
gen Askreddit = 0
replace Askreddit = 1 if subreddit == "Askreddit"
reg score Askreddit
gen Thanksobama = 0
replace Thanksobama = 1 if subreddit == "ThanksObama"
reg score Thanksobama
gen Adviceanimals = 0
replace Adviceanimals = 1 if subreddit == "AdviceAnimals"
reg score Adviceanimals
gen Politics = 0
replace Politics = 1 if subreddit == "politics"
reg score Politics
gen Worldnews = 0
replace Worldnews = 1 if subreddit == "worldnews"
reg score Worldnews
gen Economics = 0
replace Economics = 1 if subreddit == "economics"
reg score Economics
gen fourchan = 0
replace fourchan = 1 if subreddit == "4chan"
reg score fourchan
gen Showerthoughts = 0
replace Showerthoughts = 1 if subreddit == "Showerthoughts"
reg score Showerthoughts
gen Aww = 0
replace Aww = 1 if subreddit == "Aww"
reg score Aww
gen Europe = 0
replace Europe = 1 if subreddit == "Europe"
reg score Europe
gen Conservative = 0
replace Conservative = 1 if subreddit == "Conservative"
reg score Conservative
gen "Democrats" = 0
replace Democrats = 1 if subreddit == "Democrats"
reg score Democrats
#I then created an Excel graph based on the regression coefficents observed

#exploration of controversiality, was not very interesting
tabstat controversiality
gen contra = subreddit if controversiality == 1
tabulate contra
reg score contra

#time of day approach
gen seconds = mod(created_utc,86400)
gen hour = seconds / 3600
histogram hour, bin(24)

#log log regression approach
gen logscore = log(score)
gen logwordcount = log(wordcount)
gen logscore_250 = log(score_250)
scatter logscore logwordcount
twoway (scatter logscore logwordcount, msize(vtiny))
twoway(scatter logscore_250 logwordcount, msize(vtiny))



