import sqlite3
import re

import pandas as pd

class Message:
    def getMergedMessage(self):
        # connect with chat.db
        conn = sqlite3.connect("/Users/wuzewei.wzw/Library/Messages/chat.db")
        # get message and sender's info
        messages = pd.read_sql_query("select * from message order by ROWID desc limit 1", conn)
        handles = pd.read_sql_query("select * from handle order by ROWID desc limit 1", conn)

        # merge message and sender's info
        messages.rename(columns={'ROWID': 'message_id'}, inplace=True)
        handles.rename(columns={'id': 'phone_number', 'ROWID': 'handle_id'}, inplace=True)
        imessage_df = pd.merge(messages[['text', 'handle_id', 'date', 'is_sent', 'message_id']],
                               handles[['handle_id', 'phone_number']], on='handle_id', how='left')
        return imessage_df

    def get_sms_message(self):
        imessage_df = self.getMergedMessage()
        # print message text we expected
        re_code_pattern = re.compile(r'您的短信验证码为【(\d{6})】')
        for index, row in imessage_df.iterrows():
            if row['handle_id'] == 5:
                match_code = re.search(re_code_pattern, row['text'], flags=0)
                print("Msg Code: ", match_code.group(1))
                return match_code
            else:
                imessage_df = self.getMergedMessage()

