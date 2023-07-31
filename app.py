import random
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
import helper
import preprocessor

st.sidebar.title("Wassup Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # To get the data as a string we will use
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    # Fetch all the unique users from our dataframe
    user_list = df['User'].unique().tolist()
    if "Group Notification" in user_list:
        user_list.remove("Group Notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Analysis w.r.t User", user_list)  # Creating a select box in sidebar

    if st.sidebar.button("Start Analysis"):
        num_messages, tot_words, num_media_shared, url_shared = helper.show_stats(selected_user, df)

        st.title("Statistics Generated")
        col1, col2, col3, col4 = st.columns(4)  # Creating Columns to display messages
        with col1:
            st.header("Total Messages")
            st.title(num_messages[0])
        with col2:
            st.header("Total Words")
            st.title(tot_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_shared)
        with col4:
            st.header("Links Shared")
            st.title(url_shared)

        # Monthly Timeline
        st.title("Monthly Timeline Of Chats")

        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline["Time"],timeline["Message"], color = "Green")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        r = random.random()
        g = random.random()
        b = random.random()
        colors = (r, g, b)
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline["only_date"], daily_timeline["Message"], color=colors)
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        # Activity Map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most busy Day")
            r = random.random()
            g = random.random()
            b = random.random()
            colors = (r, g, b)
            busy_day = helper.week_activitymap(selected_user,df)
            fig, ax = plt.subplots()
            plt.xticks(rotation="vertical")
            ax.bar(busy_day.index, busy_day.values, color = "blue")
            st.pyplot(fig)

        with col2:
            st.header("Most busy Month")
            r = random.random()
            g = random.random()
            b = random.random()
            colors = (r, g, b)
            busy_month = helper.month_activitymap(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color=colors)
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)

        # Activity Heatmap
        st.title("Weekly Activity Heatmap")
        user_heatmap = helper.heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, new_df = helper.busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Generate word cloud
        st.title("Word cloud of " + selected_user)
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common words
        r = random.random()
        g = random.random()
        b = random.random()
        colors = (r, g, b)
        st.title("Most Common words Used by " + selected_user)
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1], color=colors)
        st.pyplot(fig)

        # Emoji Analysis
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        emoji_df = helper.emoji_helper(selected_user, df)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

        #Sentiment Analysis
        st.title("Sentiment Analysis")
        pos_count, neg_count, overall = helper.get_sentiments(selected_user, df)
        st.header(f"Positive Messages : {pos_count}")
        st.header(f"Negative Messages: {neg_count}")
        st.header(f"Overall Sentiment: {overall}")
        st.success("Analysis Done ✅")