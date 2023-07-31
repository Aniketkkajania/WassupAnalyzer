from collections import Counter
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji


def show_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    # Fetch the number of messages
    num_messages = df.shape
    words = []
    # Fetch the total number of words a user has sent
    for message in df["Message"]:
        words.extend(message.split())

    # Fetch the number of media a user has sent
    num_media_shared = df[df["Message"] == "<Media omitted>"].shape[0]

    # Fetch Number of Links shared
    extractor = URLExtract()
    urls = []
    for message in df["Message"]:
        urls.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_shared, len(urls)



def busy_user(df):
    x = df["User"].value_counts().head()
    df = round(df["User"].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'index': "Name", "User": "Percentage"})
    return x, df


# Word cloud
def create_wordcloud(selected_user, df):
    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]
    temp = df[df["User"] != "group_notification"]
    temp = temp[temp["Message"] != "<Media omitted>\n"]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color="White")
    temp["Message"] = temp["Message"].apply(remove_stop_words)
    df_wc = wc.generate(temp["Message"].str.cat(sep=" "))
    return df_wc


# most common words
def most_common_words(selected_user, df):
    f = open("stop_hinglish.txt", "r")
    stop_words = f.read()
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    temp = df[df["User"] != "group_notification"]
    temp = df[df["Message"] != "<Media omitted>\n"]

    words = []
    for message in temp["Message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    emojis = []
    for message in df["Message"]:
        emojis.extend([c for c in message if emoji.is_emoji(c) == True])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    timeline = df.groupby(["Year", "num_month", "Month"]).count()["Message"].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["Month"][i]+"-"+str(timeline["Year"][i]))
    timeline["Time"] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    daily_timeline = df.groupby('only_date').count()["Message"].reset_index()

    return daily_timeline

def week_activitymap(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    return df["day_name"].value_counts()


def month_activitymap(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    return df["Month"].value_counts()

def heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df["User"] == selected_user]

    user_heatmap = df.pivot_table(index="day_name", columns="Period", values="Message", aggfunc="count").fillna(0)
    return user_heatmap


def get_sentiments(selected_user, df):
    if selected_user!= "Overall":
        df = df[df['User'] == selected_user]
    Overall = df['Sentiment'].value_counts(sort = True, ascending= False).keys()[0]
    positive_count = df['Sentiment'].value_counts(sort = True, ascending= False).values[0]
    negative_count = df['Sentiment'].value_counts(sort = True, ascending= False).values[1]
    return positive_count, negative_count, Overall
