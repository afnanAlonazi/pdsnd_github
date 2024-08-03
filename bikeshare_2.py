import time
import numpy as np
import pandas as pd
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
filter_type = "" 


def get_city():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    global city

    print('Hello! Let\'s explore some US bikeshare data!')
      # Get user input for city (chicago, new york city, washington)
    while True:
            city = input(" Which city Would you like for Chicago, New York, or Washington? ")
            city = city.strip().lower()
            if city in ['chicago', 'new york', 'washington']:
                return city
            print("You've made a mistake ! Try again")
            
    #  Get user input for filter type (month, day, both, none)
def get_filter_type():
    global filter_type 
    while True:
            filter_type = input("Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter: ")
            filter_type = filter_type.strip().lower()
            if filter_type in ['month', 'day', 'both', 'none']:
                return filter_type
            print("You've made a mistake ! Try again")
      
    # Get user input for month if needed
def get_month():
    if filter_type in ['month', 'both']:
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        while True:
                month = input("Which month? January, February, March, April, May, June, or all? ")
                month=month.strip().lower()
                if month in months:
                    return month
                print("You've made a mistake ! Try again")
    
    # Get user input for day if needed
def get_day():
    if filter_type in ['day', 'both']:
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        while True:
                day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all? ")
                day=day.strip().lower()
                if day in days:
                      return day
                print("You've made a mistake ! Try again")



def load_data(city, month="all", day="all"):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # note that load function is derived from Practice Solution #3 but I  add try except 
    try:
        # load data file into a dataframe
        df = pd.read_csv(CITY_DATA[city])
        
        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        
        # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.day_name()
        
        
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
    
    except FileNotFoundError:
        print("The file for", city, "does not exist.")
    except Exception as e:
        print(e)
def display_stats(caluc, value, filter_type, count):
    print("Most Popular", caluc , ":", value ," Filter type:", filter_type ,"  Count: " , count)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    if df is None:
        print(" data for time  are not loading for " , city )
        return
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Most common month
    if 'month' in df.columns: # check if df column exists  or not 
        popular_month = df['month'].mode()[0]
        display_stats("Month", popular_month, filter_type, df['month'].value_counts()[popular_month])
        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print(" month data not available.")
    # Most common day of week
    if 'day_of_week' in df.columns:
        popular_day = df['day_of_week'].mode()[0]
        display_stats("Day of Week", popular_day, filter_type, df['day_of_week'].value_counts()[popular_day])
        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print(" day data not available.")
    # Most common start hour
    if 'Start Time' in df.columns:
        df['hour'] = df['Start Time'].dt.hour
        popular_hour = df['hour'].mode()[0]
        display_stats("Start Hour", popular_hour, filter_type, df['hour'].value_counts()[popular_hour])
        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print("Start Time data not available.")
    print('-'*40)




def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    if df is None:
        print("data station are not loading for " , city )
        return
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

        # Most commonly used start station
    if 'Start Station' in df.columns:
        popular_start_station = df['Start Station'].mode()[0]
        display_stats("Start Station", popular_start_station, filter_type, df['Start Station'].value_counts()[popular_start_station])
        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print("Start Station data not available.")
    # Most commonly used end station
    if 'End Station' in df.columns:
        popular_end_station = df['End Station'].mode()[0]
        display_stats("End Station", popular_end_station, filter_type, df['End Station'].value_counts()[popular_end_station])
        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print("End Station data not available.")
    # Most frequent combination of start station and end station trip
    if 'Start Station' in df.columns and 'End Station' in df.columns:
        df['popular trip'] = df['Start Station'] + " to " + df['End Station']
        popular_trip = df['popular trip'].mode()[0]
        display_stats("Trip", popular_trip, filter_type, df['popular trip'].value_counts()[popular_trip])
        print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print("Popular trip data not available.")


    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    if df is None:
        print("data for trip duration  are not loading for " , city )
        return
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    if 'Trip Duration' in df.columns:
      total_travel_time = df['Trip Duration'].sum()
      print("Total Travel Time:", total_travel_time ," seconds  filter type: ", filter_type )
      print("\nThis took %s seconds." % (time.time() - start_time))
      # display mean travel time
      mean_travel_time = df['Trip Duration'].mean()
      print("Mean Travel Time: ", mean_travel_time ," seconds filter type: ", filter_type )
      print("\nThis took %s seconds." % (time.time() - start_time))
    else:
        print("Trip Duration data not available.")  
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    if df is None:
        print("data users are not loading for " , city )
        return
    print('\nCalculating User Stats...\n')
    start_time = time.time()

     #  Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Types:" ,user_types )
    
    #Display counts of gender
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("Gender:" , gender_counts )
    else:
        print("Gender data not available ")
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_popular_year = int(df['Birth Year'].mode()[0])
        print("Earliest Year of Birth:" , earliest_year )
        print("Most Recent Year of Birth:" ,  most_recent_year)
        print("Most Popular Year of Birth:" , most_popular_year)
    else:
        print("\nBirth Year data not available ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_trip(df):
    """Displays raw data upon request by the user in chunks of 5 rows."""
    if df is None or len(df) == 0:
        print(" no data to display for  " , city )
        return
    data_row = [df.iloc[i:i + 5] for i in range(0, len(df), 5)]  # source https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html
    
    for i, row in enumerate(data_row): # use enumerate to help us know the index along with row 
        print(row)
        
        # Check for the last row 
        if i == len(data_row) - 1:
            print("No more individual trip data to show.")

        
        show_data = input("\nWould you like to view 5 more individual trip data ? Enter yes or no.\n")
        if show_data.strip().lower() != 'yes':
            break

def main():
    while True:
        city = get_city()
        filter_type = get_filter_type()

        if filter_type in ['month', 'both']:
            month = get_month()

        if filter_type in ['day', 'both']:
            day = get_day()
        df = load_data(city, month, day)
      
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_trip(df)  # for display 5 trip

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
