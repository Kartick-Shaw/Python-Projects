import helper
import seaborn as sns
import streamlit as st
import preprocessor as ppr
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="WhatsApp Chat Analyser",
    page_icon="https://static.vecteezy.com/system/resources/previews/023/986/631/non_2x/whatsapp-logo-whatsapp-logo-transparent-whatsapp-icon-transparent-free-free-png.png",
    layout="wide"
)

st.sidebar.markdown('<img src="https://static.vecteezy.com/system/resources/previews/023/986/631/non_2x/whatsapp-logo-whatsapp-logo-transparent-whatsapp-icon-transparent-free-free-png.png" width=100px height=100px>', unsafe_allow_html=True)
st.sidebar.title(":violet[Whatsapp Chat Analyser]")
upload_file = st.sidebar.file_uploader(":green[Choose a file:] ")
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode('utf-8')
    # st.text(data)
    df = ppr.preprocess(data)
    # st.dataframe(df)

    # fetch unique User
    user_list = df['users'].unique().tolist()
    if 'System_notification' in user_list:
        user_list.remove('System_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox('Show Analysis wrt', user_list)
    if st.sidebar.button("Show Analysis"):
        # Stats Area
        num_msg, words, num_media, link = helper.fetch_stats(selected_user, df)
        st.markdown("<h1 style='text-align:center;';>Whatsapp Statistics📊</h1>",unsafe_allow_html=True)
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns(5)
        if selected_user == 'Overall':
            with col1:
                st.header("Total Persons")
                st.title(len(user_list) - 1)
        with col2:
            st.header("Total Messages")
            st.title(num_msg)
        with col3:
            st.header("Total Words")
            st.title(len(words))
        with col4:
            st.header("Media Shared ")
            st.title(num_media)
        with col5:
            st.header("Link Shared ")
            st.title(link)
        st.markdown("---")
        
        # Monthly Timeline
        # st.title('Monthly Timeline')
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Monthly Timeline</h1>",unsafe_allow_html=True)
        st.markdown("---")
        timeline = helper.monthly_timeline(selected_user, df)
        # fig, ax = plt.subplots()
        # ax.plot(timeline['time'], timeline['message'], color='green')
        # plt.xticks(rotation='vertical')
        fig = px.line(data_frame=timeline, x='time', y='message', height=600)
        st.plotly_chart(fig, use_container_width=True)

        # Daily Timeline
        # st.title('Daily Timeline')
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Daily Timeline</h1>",unsafe_allow_html=True)
        st.markdown("---")
        daily_timeline = helper.daily_timeline(selected_user, df)
        # fig, ax = plt.subplots()
        # ax.plot(daily_timeline['date_timeline'], daily_timeline['message'], color='black')
        # plt.xticks(rotation='vertical')
        # st.pyplot(fig)
        fig = px.line(data_frame=daily_timeline, x='date_timeline', y='message', height=600)
        st.plotly_chart(fig, use_container_width=True)

        # Activity map
        # st.title('Activity Map')
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Activity Map</h1>",unsafe_allow_html=True)
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            # st.header("Most Texted Day")
            st.markdown("---")
            st.markdown("<h1 style='text-align:center';>Most Texted Day</h1>",unsafe_allow_html=True)
            st.markdown("---")
            busy_day = helper.week_activity_map(selected_user, df)
            # fig, ax = plt.subplots() 
            # ax.bar(busy_day.index, busy_day.values)
            # plt.xticks(rotation='vertical')
            # st.pyplot(fig)
            fig = px.bar(x=busy_day.index, y=busy_day.values, color=busy_day.values)
            fig.update_layout(xaxis_title='Days', yaxis_title='Number of Messages')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # st.header("Most Texted Month")
            st.markdown("---")
            st.markdown("<h1 style='text-align:center';>Most Texted Month</h1>",unsafe_allow_html=True)
            st.markdown("---")
            busy_month = helper.month_activity_map(selected_user, df)
            # fig, ax = plt.subplots() 
            # ax.bar(busy_month.index, busy_month.values, color='cyan')
            # plt.xticks(rotation='vertical')
            # st.pyplot(fig)
            fig = px.bar(x=busy_month.index, y=busy_month.values, color=busy_month.values)
            fig.update_layout(xaxis_title='Months', yaxis_title='Number of Messages')
            st.plotly_chart(fig, use_container_width=True)
        
        # Activity Heatmap
        st.title('Weekly Activity Map')
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Weekly Activity Map</h1>",unsafe_allow_html=True)
        st.markdown("---")
        # plt.figure(figsize=(20, 8))
        fig, ax = plt.subplots(figsize=(20, 8))
        user_heatmap = helper.activity_heatmap(selected_user, df)
        ax = sns.heatmap(user_heatmap, annot=True, cmap=sns.cubehelix_palette(as_cmap=True))
        st.pyplot(fig)

        
        # Finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            # st.title('Most Busy User')
            st.markdown("---")
            st.markdown("<h1 style='text-align:center';>Most Busy User</h1>",unsafe_allow_html=True)
            st.markdown("---")
            x, new_df = helper.fetch_most_busy_user(df)
            # fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                # ax.bar(x.index, x.values, color='red')
                # plt.xticks(rotation='vertical')
                # st.pyplot(fig)
                x_label = x.index
                y_label = x.values
                fig = px.bar(data_frame=x, x=x_label, y=y_label, color=y_label)
                fig.update_layout(xaxis_title='Users', yaxis_title='Number of Messages')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(new_df)

        # WordCloud
        # st.title("Wordcloud")
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Wordcloud</h1>",unsafe_allow_html=True)
        st.markdown("---")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        most_common_word_df = helper.most_common_word(selected_user, df)
        # fig, ax = plt.subplots()
        # ax.barh(most_common_word_df[0], most_common_word_df[1])
        # plt.xticks(rotation='vertical')
        # st.title('Most Common Words')
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Most Common Words</h1>",unsafe_allow_html=True)
        st.markdown("---")
        # st.pyplot(fig)
        fig = px.bar(x=most_common_word_df[1], y=most_common_word_df[0], orientation='h', height=600, color=most_common_word_df[0])
        fig.update_layout(xaxis_title='Count', yaxis_title='Common Words')
        # st.dataframe(most_common_word_df)
        st.plotly_chart(fig, use_container_width=True)

        # Emoji Analysis
        # st.title('Emoji Analysis')
        st.markdown("---")
        st.markdown("<h1 style='text-align:center';>Emoji Analysis</h1>",unsafe_allow_html=True)
        st.markdown("---")
        emoji_df = helper.emoji_helper(selected_user, df)
        if len(emoji_df) != 0:
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(emoji_df.head())
            
            with col2:
                # plt.rcParams['font.family'] = 'EmojiOne Color'
                plt.rcParams['font.family'] = 'Segoe UI Emoji'
                # fig, ax = plt.subplots()
                # ax.pie(emoji_df['Count'].head(), labels = emoji_df['Emoji'].head(), autopct="%0.1f%%")
                # st.pyplot(fig)
                # fig = px.pie(data_frame=emoji_df.head(), names='Emoji', values='Count', color='Emoji', color_discrete_map={'Thur':'lightcyan', 'Fri':'cyan', 'Sat':'royalblue', 'Sun':'darkblue'})
                fig = px.pie(data_frame=emoji_df.head(), names='Emoji', values='Count', color='Emoji', color_discrete_sequence=px.colors.sequential.matter, hole=0.5)
                fig.update_traces(hoverinfo='percent+label', textinfo='percent+label', textfont_size=15, marker=dict(line=dict(color='Black', width=2)))
                fig.update_layout(autosize=False, height=600)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.write(f"{selected_user} have not send any emoji right now...")