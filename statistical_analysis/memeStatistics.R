#The following R code has several functions that are documented before
#it's corresponding code. The functions all utilize data from the given
#meme file, which is read in during the first line of the code. The script
#is structured such that all the function calls are at the end of the code.

#Read in Meme file
meme <- read.csv(file="obama.csv",header=TRUE, sep =",");

#Convert given UTC to years
original_data_years <- meme$created_utc <- ((meme$created_utc/(60*60*24*365.25)+1970));

#Function to truncate years by a certain amount
truncate_years <- function(creation_date, truncate_amount){
  for(i in 1:length(creation_date)){
    year = creation_date[i];
    creation_date[i] = round(year,truncate_amount);
  }
  return (creation_date);
}

#Function to Truncate Years into Months
years_to_months <- function(creation_date){
 for(i in 1:length(creation_date)){
   year = creation_date[i];
   year_decimal = round(year,2)-floor(year);
   creation_date[i] = floor(year) + (8*floor(year_decimal*12)/100);
 }
 return(creation_date);
}

#Function to create a plot of usage of the meme
meme_usage <- function(original_data_years){
  creation_date <- table(truncate_years(original_data_years, 0));
  creation_date_precision <- table(truncate_years(original_data_years,2));
  x_values <- names(creation_date_precision);
  y_values <- as.vector(creation_date_precision);
  plot(x_values, y_values, main="Precise meme", ty="l");
  lines(barplot(creation_date));
}


#Function to create a Pie Chart of Ten Most Common Subbredits - Overall
ten_most_common <- function(original_data_years){
  subreddit_info <- sort(table(meme$subreddit),decreasing=TRUE)[1:10]
  slices <- as.vector(subreddit_info);
  labels <- names(subreddit_info);
  pie(slices, labels, main="Pie Chart of Most Common Appearences - Overall");
}


#Function to create a Pie Chart of Ten Most Common Subreddits - One for Each Year
ten_most_common_years <- function(original_data_years){
  meme$created_utc <- truncate_years(original_data_years, 0);
  for(i in 1:length(table(meme$created_utc))){
    subreddit_info_years <- sort(table(meme[meme$created_utc==2007+i, ]$subreddit),
                                 decreasing=TRUE)[1:10];
    slices<- as.vector(subreddit_info_years);
    labels <- names(subreddit_info_years);
    pie(slices, labels, main= paste("Pie Chart of Most Common Appearences in", toString(2007+i), sep=" "));
  }
}

#Function to create a Pie Chart of Ten Most Common Subreddits - any given year
most_common_in_year <- function(original_data_years, year){
  meme$created_utc <- truncate_years(original_data_years, 0);
  subreddit_info_years <- sort(table(meme[meme$created_utc==year, ]$subreddit),
                                 decreasing=TRUE)[1:10];
  slices<- as.vector(subreddit_info_years);
  labels <- names(subreddit_info_years);
  pie(slices, labels, main= paste("Switcharoo in", toString(year), sep=" "));
}

#Function to Track Mean Score per Month
track_mean_score <- function(original_data_years){
  meme$created_utc <- years_to_months(original_data_years);
  x_values <- names(table(meme$created_utc));
  y_values = seq(length(x_values));
  for(i in 1:length(x_values)){
    y_values[i] = mean(meme[which(meme$created_utc == x_values[i]), ]$score);
  }
  plot(x_values, y_values, type = "l", main = "Mean Score of Obama Memes",
       xlab="Year", ylab="Mean Score", col = "blue");
}

#Function to Track Mean Polarity per Month
track_mean_polarity <- function(original_data_years){
  meme$created_utc <- years_to_months(original_data_years);
  x_values <- names(table(meme$created_utc));
  y_values = seq(length(x_values));
  for(i in 1:length(x_values)){
    y_values[i] = mean(meme[which(meme$created_utc == x_values[i]), ]$polarity);
  }
  plot(x_values, y_values, type = "l", main = "Mean Polarity of Obama Memes",
       xlab="Year", ylab="Mean Polarity", col = "blue");
}

#Function to Track Mean Polarity per Month excluding
track_mean_polarity_precision <- function(original_data_years, absolute_value){
  meme$created_utc <- years_to_months(original_data_years);
  x_values <- names(table(meme$created_utc));
  y_values <- seq(length(x_values));
  neg_absolute_value <- (-1*absolute_value);
  for(i in 1:length(x_values)){
    y_values[i] = mean(meme[which(meme$created_utc == x_values[i]
                                  & meme$polarity >= absolute_value
                                   ), ]$polarity);
  }
  plot(x_values, y_values, type = "l", main = "Mean Polarity of Ratings Memes with |0.5| <= polarity",
       xlab="Year", ylab="Mean Polarity", col = "blue");
}


#Function to Track Median Score per Month Overall
track_median_score <- function(original_data_years){
  meme$created_utc <- years_to_months(original_data_years);
  x_values <- names(table(meme$created_utc));
  y_values = seq(length(x_values));
  for(i in 1:length(x_values)){
    y_values[i] = median(meme[which(meme$created_utc == x_values[i]), ]$score);
  }
  plot(x_values, y_values, type = "l", xlab="Year",
       ylab="Score", main = "Median Score of Switcharoo Memes", col = "blue");
}

#Function to Track Median Score per Month and Specify what not to include
track_median_score_precision <- function(original_data_years, greaterThan){
  meme$created_utc <- years_to_months(original_data_years);
  x_values <- names(table(meme$created_utc));
  y_values = seq(length(x_values));
  for(i in 1:length(x_values)){
    y_values[i] = median(meme[which(meme$created_utc == x_values[i] &
                                      meme$score >= greaterThan), ]$score);
  }
  plot(x_values, y_values, type = "l", xlab="Year", ylab = "Score",
       main=paste("Median Score of Switcharoo Memes that are at least", toString(greaterThan),
                  sep = " "), col = "blue");
}


#Function to Track Correlation in Score
score_vs_comment <- function(original_data_years, last_months){
  meme$created_utc <- years_to_months(original_data_years);
  comments_and_months <- table(meme$created_utc);
  comments <- as.vector(comments_and_months);
  months <- names(comments_and_months);
  if(last_months != 0){
    months <- tail(months, last_months);
    comments <- tail(comments, last_months);
  }
  scores <- seq(length(months));
  for(i in 1:length(months)){
    scores[i] = mean(meme[which(meme$created_utc == months[i]), ]$score);
  }
  plot(months, comments/50,
       main = paste("Switcharoo Comments and Mean Score in last", toString(last_months), "months", sep = " "),
       xlab = "Year", ylab = "Volume", type = "l", col = "red");
  lines(months, scores, type = "l", col = "blue");

  months;
  print(cor(scores, comments/200));
}

#Function to Track Correlation of Polarity
score_vs_polarity <- function(original_data_years, last_months){
  meme$created_utc <- years_to_months(original_data_years);
  comments_and_months <- table(meme$created_utc);
  comments <- as.vector(comments_and_months);
  months <- names(comments_and_months);
  if(last_months != 0){
    months <- tail(months, last_months);
    comments <- tail(comments, last_months);
  }
  polarity <- seq(length(months));
  for(i in 1:length(months)){
    scores[i] = mean(meme[which(meme$created_utc == months[i]), ]$score);
  }
  plot(months, comments/50,
       main = paste("Switcharoo Comments and Mean Score in last", toString(last_months), "months", sep = " "),
       xlab = "Year", ylab = "Volume", type = "l", col = "red");
  lines(months, scores, type = "l", col = "blue");

  months;
  print(cor(scores, comments/200));
}


#Function Call
meme_usage(original_data_years);
ten_most_common(original_data_years);
ten_most_common_years(original_data_years);
most_common_in_year(original_data_years, 2009);
track_mean_score(original_data_years);
track_mean_polarity(original_data_years);
track_mean_polarity_precision(original_data_years, 0.3);
track_median_score(original_data_years);
track_median_score_precision(original_data_years, 5);
score_vs_comment(original_data_years, 36)
