import re
import pandas as pd

"07/11/21, 19:53 - "
def preprocess(data):
    pattern = r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s*[ap]m - (.*)'
    dates = re.findall(r'(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s*[ap]m)', data)
    messages = re.findall(pattern, data)
    """Creating a Panda DataFrame"""
    df = pd.DataFrame({'User Messages': messages, 'Date': dates})
    df['Date'] = df['Date'].str.replace('\u202f', ' ')

    # Parse the datetime using the updated format
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y, %I:%M %p')

    users = []
    messages = []
    for message in df['User Messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("Group Notification")
            messages.append(entry[0])

    df['User'] = users  # Creating Column User and Message
    df['Message'] = messages
    df.drop(columns=['User Messages'], inplace=True)  # Removing Column User Messages from our Dataframe
    df["only_date"] = df["Date"].dt.date
    df["day_name"] = df["Date"].dt.day_name()
    df["Year"] = df['Date'].dt.year
    df["num_month"] = df["Date"].dt.month_name()
    df["Month"] = df['Date'].dt.month_name()
    df["Day"] = df['Date'].dt.day
    df["Hour"] = df['Date'].dt.hour
    df["Minute"] = df['Date'].dt.minute

    period = []
    for hour in df[["day_name", "Hour"]]["Hour"]:
        if hour == 23:
            period.append(str(hour)+"-"+str('00'))
        elif hour == 0:
            period.append(str("00")+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))

    df["Period"] = period
    return df

