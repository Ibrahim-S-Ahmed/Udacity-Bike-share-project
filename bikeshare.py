import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # hema -- try this while with every input

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
            city = input("which city do you like to choose from chicago, new york city, washington: ").lower()
            if city in ['chicago','new york city','washington']:
                break
            else:
                print("please choose a correct city name")
        


    # get user input for month (all, january, february, ... , june)
    while True:
            month = input("which month do you like to choose (you can choose all or a month from january to june) ").lower()
            if month in ['january','february','march','april','may','june','all']:
                break
            else:
                print("please choose a correct month name")
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
            day = input("which day do you like to choose (you can choose all or specific day) ").lower()
            if day in ['monday','tuesday','wendesday','thursday','friday','saturday','sunday','all']:
                break
            else:    
                print("please choose a correct day name")
        
    

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
   # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() 
    # I usedbpandas.Series.dt.day_name(), since pandas.Timestamp.weekday_name has been deprecated since version 0.23.0

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df

def display_raw_data(df):
    """ 
    Raw data is displayed upon request by the user
    Arg:
    df - df - Pandas DataFrame containing city data filtered by month and day
    """
    i = 1
    answer = input("Would you like to dispaly the first 5 raws of data? yes or no: ").lower()
    pd.set_option('display.max_columns',None) 

    while True:
        if answer not in ['yes', 'no']:
            print ('enter yes or no only ')
            display_raw_data(df)
            break
        elif answer == 'yes':
            print(df[i:i+5])
            answer = input('would you like to display the next 5 rows of data? yes or no: ').lower()
            i += 5   
        else:
            break
        



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("Most common month is : ", common_month)

    # display the most common day of week
    # common_day = df['day_of_week'].mode()[0]
    print("Most common day is : ", df['day_of_week'].mode()[0])

    # display the most common start hourime
    df['hour'] = df['Start Time'].dt.hour

    common_hour = df['hour'].mode()[0]
    print("Most common start hour is : ", common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("Most commonly used start station: ", common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("Most commonly used end station: ", common_end)

    # display most frequent combination of start station and end station trip
    common_start_end = (df['Start Station']+ ' / ' + df['End Station']).mode()[0]
    print("Most frequent combination of start station and end station trip:\n", common_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time is: " , total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Average travel time is: " , mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print('Counts of user types: ', user_type)

    

    if city in ['chicago','new york city']:
        # Display counts of gender
        print("count of gender: ", df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth

        print("earliest year of birth: " , int(df['Birth Year'].min()))
        print("Most recent year of birth: " , int(df['Birth Year'].max()))
        print("Most common year of birth: " , int(df['Birth Year'].mode()[0]))
        
    else:
        print("Washington city do not contain gender or birth year data")
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()