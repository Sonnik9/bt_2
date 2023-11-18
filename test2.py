            # PreviousHeikenBody = abs(df['Heiken_Open'].iat[i-1] - df['Heiken_Close'].iat[i-1])

            # condition_up = (
            #     (df['Heiken_High'].iat[i-1] - max(df['Heiken_Open'].iat[i-1], df['Heiken_Close'].iat[i-1])) /
            #     PreviousHeikenBody > ratio and
            #     (min(df['Heiken_Open'].iat[i-1], df['Heiken_Close'].iat[i-1]) - df['Heiken_Low'].iat[i-1]) /
            #     PreviousHeikenBody > ratio and
            #     (df['Heiken_Open'].iat[i] < df['Heiken_Close'].iat[i] and
            #     df['Heiken_Low'].iat[i] >= df['Heiken_Open'].iat[i])
            #     signal1[i] = 2
            # )

            # condition_down = (
            #     (df['Heiken_High'].iat[i-1] - max(df['Heiken_Open'].iat[i-1], df['Heiken_Close'].iat[i-1])) /
            #     PreviousHeikenBody > ratio and
            #     (min(df['Heiken_Open'].iat[i-1], df['Heiken_Close'].iat[i-1]) - df['Heiken_Low'].iat[i-1]) /
            #     PreviousHeikenBody > ratio and
            #     (df['Heiken_Open'].iat[i] > df['Heiken_Close'].iat[i] and
            #     df['Heiken_High'].iat[i] <= df['Heiken_Open'].iat[i])
            #     signal1[i] = 1
            # )