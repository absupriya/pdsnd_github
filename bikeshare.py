#Import libraries
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# define the cities, months and days_of_week
cities = ['chicago', 'new york', 'washington']
months = ['january','february','march','april','may','june','all']
days_of_week = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']

# Get the choice of the user and validate the input. If the input is incorrect, ask the user again to input a value from the given choices.
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nHello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nEnter a city name you want to explore data for: \nChicago, New York, Washington\n\nInput City: ").lower()
        if city in cities:
            break
        else:
            print('You have entered an invalid city. Please enter a valid city.')
            
    # TO DO: get user input for month (all, january, february, ... , june)       
    while True:   
        month = input("\nEnter a month name you want to explore data for. If you dont want to choose any of the given months, enter all: \nJanuary, February, March, April, May, June, All\n\nInput Month: ").lower()
        if month in months:
            break
        else:
            print('You have entered an invalid month name. Please enter a valid month.')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("\nEnter a day of the week you want to explore data for. If you dont want to choose any of the given day, enter all: \nSunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, All\n\nInput Day: ").lower()
        if day in days_of_week:
            break
        else:
            print('You have entered an invalid day. Please enter a valid day.')

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

    # convert the Start Time column to datetime and create 3 new columns - month, month name and day of week.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Month_Name'] = df['Start Time'].dt.month_name().str.lower()
    df['days_of_week'] = df['Start Time'].dt.weekday_name.str.lower()

    # filter by month and day and create a new dataframe
    if month != 'all':
        df = df[df['Month_Name'] == month]
    
    if day != 'all':
        df = df[df['days_of_week'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['Month_Name'].mode()[0]
    print('Most common month:', most_common_month.capitalize())

    # TO DO: display the most common day of week
    most_common_day = df['days_of_week'].mode()[0]
    print('Most common day:', most_common_day.capitalize())

    # TO DO: display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    if most_common_start_hour < 12:
        print('Most common start hour:', most_common_start_hour,'AM')
    elif most_common_start_hour > 12:
        print('Most common start hour:', most_common_start_hour-12,'PM')
    else:
        print('Most common start hour:', most_common_start_hour,'PM')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: ',most_common_start_station)

    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ',most_common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start End Station'] = df['Start Station'] + ' and ' + df['End Station']
    most_frequent_start_end_station = df['Start End Station'].mode()[0]
    print('Most frequent start end station: ',most_frequent_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time:", int(round(total_travel_time/3600)),'hours or',int(round(total_travel_time/86400)),'days')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    minutes, seconds = divmod(mean_travel_time, 60)
    hours, seconds = divmod(minutes, 60)
    print("Mean Travel Time: %02d hours %02d minutes %02d seconds" % (hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('Number of user types: \n', count_user_types)

    # TO DO: Display counts of gender
    try:
        df['Gender'] = df['Gender'].fillna('Unknown Gender')
        gender_type = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_type)        
    except:
        print('\nGender Types: Sorry, no gender data is available for {} city'.format(city.capitalize()))

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        most_common_yob = df['Birth Year'].mode()[0]
        
        print('\nEarliest Birth Year: ', int(earliest_birth_year))
        print('\nRecent Birth Year: ', int(recent_birth_year))
        print('\nMost Common Year of Birth:', int(most_common_yob))
    except:
        print('\nYear of Birth: Sorry, no birth year data is available for {} city'.format(city.capitalize()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Ask user if they want to see any number of lines of raw data (instead of only 5 lines as asked in the rubric)
# Below code will prompt the user to enter the number of lines of raw data to be displayed. 
# If the user enters 0 or doesn't enter any value, 5 rows will be displayed by default.
def request_raw_data(df):
    # Initialize the variables
    start_num = 0
    end_num = 0
    df_length = len(df.index)

    # Prompt user and iterate over the dataframe df to print the number of rows as requested by the user.
    while start_num < df_length:
        prompt = input('\nWould you like to see raw data? yes or no.\n')
        if prompt.lower() == 'yes':
            num_lines = input('\nPlease enter the number of lines of raw data you would like to see. If you input 0 or dont enter any number, 5 lines will be displayed by default.\n')
            #Check if the num_lines is 0 or is not a digit
            if (int(num_lines) == 0) or (not num_lines.isdigit()):
                num_lines = 5
            print("\nDisplaying only {} rows of data.\n".format(num_lines))
            if end_num > df_length:
                end_num = df_length
            end_num += int(num_lines)
            # displaying the raw data
            print(df.iloc[start_num:end_num])
            start_num += int(num_lines)
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if day == 'all':
            print('You have selected to analyze {} data for {} month(s) and {} days\n'.format(city.capitalize(), month.capitalize(), day.capitalize()))
        else:
            print('You have selected to analyze {} data for {} month(s) and on {}\n'.format(city.capitalize(), month.capitalize(), day.capitalize()))
        
        # Call the functions to analyze the data and print the statistics
        request_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
