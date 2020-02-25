import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Enter city name from (chicago, new york city, washington):')
            city = city.lower()
            if city not in CITY_DATA :
                print("Invalid City")
                continue
            break
        except:
            print("Invalid input.")
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Enter month from (all, january, february, ... , june):')
            month = month.lower()
            if month not in MONTHS and month != 'all':
                print('Invalid month. Please enter correct month.')
                continue
            break
        except:
            print("Invalid input")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Enter day of week (all, monday, tuesday, ... sunday):')
            day = day.lower()
            if day not in ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):
                print('Invalid date. Please enter correct day.')
                continue
            break
        except:
            print("Invalid input")
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month =  df['month'].mode()[0]
    print("\nMost Common Month: %s" % common_month)
    common_day_of_week = df['day_of_week'].mode()[0]
    print("\nMost Common Day of week: %s" % common_day_of_week)
    df["hour"] = df['Start Time'].dt.hour
    common_hour = df["hour"].mode()[0]
    print("\nMost Common start hour: %s" % common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    most_common_start_station = df["Start Station"].mode()[0]
    most_common_end_station = df["End Station"].mode()[0]
    
    # TO DO: display most frequent combination of start station and end station trip
    df["Start and End"] =  df["Start Station"].str.cat(df["End Station"], sep=' - ')
    most_common_start_end = df["Start and End"].mode()[0]
    print("\nMost popular start Station: %s" % most_common_start_station)
    print("\nMost popular End Station: %s" % most_common_end_station)
    print("\nMost popular Trip: %s" % most_common_start_end)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df["Trip Duration"].sum()
    print("Total Travel Time: %s hours" % (total_time/3600.0))

    # TO DO: display mean travel time
    mean_time = df["Trip Duration"].mean()
    print("Mean Trip Time: %s min" % (mean_time/60.0))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    
    if city == 'washington':
        print(" Washigton don't have Gender and Birth year info, so skipping user stats")
        return
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("\n Users types stats \n")
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    print("\n Gender stats \n")
    
    print(df['Gender'].value_counts())

    # TO DO: Display earliest, most recent, and most common year of birth
    earliest = df["Birth Year"].nsmallest(1);
    most_recent = df["Birth Year"].nlargest(1);
    most_common = df["Birth Year"].mode()[0]
    print("\nOldest rider Birth year Info \n")
    print(earliest)
    print("\nYoungest rider Birth year \n ")
    print(most_recent)
    print("\nMost common birth year of rider: %d " % most_common)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
