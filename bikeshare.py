 
import time
import pandas as pd
import numpy as np

# import data
CITY_DATA = { 'chicago': r'C:\Users\nhnah\OneDrive\Desktop\bikeshare\data\chicago.csv',
              'new york city': r'C:\Users\nhnah\OneDrive\Desktop\bikeshare\data\new_york_city.csv',
              'washington': r'C:\Users\nhnah\OneDrive\Desktop\bikeshare\data\washington.csv'}

# filters for city, month, and day
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nWhich city would you like to filter by? New York City, Chicago or Washington?\n').lower()

    # while loop to handle invalid inputs
    while (city not in CITY_DATA.keys()):
        city = input("\nplease enter a correct city name from the following: \nNew York City, Chicago or Washington\n").lower()

    # get user input for month (all, january, february, ... , june)
    
    months = ['All','January', 'February', 'March', 'April', 'May', 'June']
    month = input("\nWhich month would you like to filter by? January, February, March, April, May, June or type 'all' if you do not have any preference?\n").title()
    #while loop to make sure that the user entered the correct name of month
    while (month not in months):
        month = input('Please enter a correct month from the folloiwng to filter by\njanuary, february, march, april, may, june\ntype "all" for no month filtering\n').title()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    days = ['All' , 'Monday' , 'Tuesday' , 'Wednesday' , 'Thursday' , 'Friday' , 'Saturday' , 'Sunday']
    day = input("\nAre you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n").title()
    #while loop to make sure that the user entered the day name in the correct way
    while (day not in days):
        day = input('\nPlease enter a correct day of the week to filter by\ntype "all" for no day filtering\n').title()

   
    print('-'*40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # creating df by reading csv file
    df = pd.read_csv(CITY_DATA[city], index_col=[0])

    # converting Start Time column into datetime data type
    df['Start Time']=pd.to_datetime(df['Start Time'])

    # extracting month and week day from 'Start Time' column
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # filter by month
    if month != 'All':
        df = df[df['Month'] == month]

    # filter by day
    if day != 'All':
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('\nMost common month is: ',df['Month'].mode()[0])

    # display the most common day of week
    print('\nMost common day is: ',df['Day of Week'].mode()[0])

    # display the most common start hour

    # extracting Hour column from 'Start Time' column
    df['Hour'] = df['Start Time'].dt.hour
    hr = df['Hour'].mode()[0]

    #to convert 24 hour format into 12 hour format
    if hr <= 12:
        print('\nMost common start hour is: {} AM'.format(hr))
    else:
        print('\nMost common start hour is: {} PM'.format(hr%12))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nMost commonly used start station is: ',df['Start Station'].mode()[0])

    # display most commonly used end station
    print('\nMost commonly end station is: ',df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['Start & End'] = df['Start Station'].str.cat(df['End Station'], sep=' --> ')

    print('\nMost frequent combination of start station and end station trip is: ',df['Start & End'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    print('\nTotal travel duration is: ',df['Trip Duration'].sum())

    # display mean travel time

    print('\nAverage travel duration is: ',df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    print('\nCount of user types: \n',df['User Type'].value_counts())

    # Display counts of gender
    
    # handling any error for any city's csv file having no Gender column
    try:
        print('\nCounts of gender: \n',df['Gender'].value_counts())
    except:
        print('\nSorry, Washington has no "Gender" data available')

    # Display earliest, most recent, and most common year of birth
    # handling any error for any city's csv file having no Birth Year column
    
    try:
      earliest_birth_year = int(df['Birth Year'].min())
      print('\nEarliest Year:', earliest_birth_year)
    
      most_recent_birth_year = int(df['Birth Year'].max())
      print('\nMost Recent Year:', most_recent_birth_year)
   
      most_common_birth_year = int(df['Birth Year'].mode())
      print('\nMost Common Year:', most_common_birth_year)
    except Exception as ex:
      print('\nSorry, Washington has no "year of birth" data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
