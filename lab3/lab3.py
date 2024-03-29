from spyre import server
import pandas as pd
import os

class StockExample(server.App):
    title = "NOAA data visualization"
    NOAA_OPTIONS = [
        {"label": "VCI", "value": "VCI"},
        {"label": "TCI", "value": "TCI"},
        {"label": "VHI", "value": "VHI"}
    ]

    AREA_OPTIONS = [
        {"label": "Cherkasy", "value": "Cherkasy"},
        {"label": "Chernihiv", "value": "Chernihiv"},
        {"label": "Chernivtsi", "value": "Chernivtsi"},
        {"label": "Crimea", "value": "Crimea"},
        {"label": "Dnipropetrovs'k", "value": "Dnipropetrovs'k"},
        {"label": "Donets'k", "value": "Donets'k"},
        {"label": "Ivano-Frankivs'k", "value": "Ivano-Frankivs'k"},
        {"label": "Kharkiv", "value": "Kharkiv"},
        {"label": "Kherson", "value": "Kherson"},
        {"label": "Khmel'nyts'kyy", "value": "Khmel'nyts'kyy"},
        {"label": "Kyiv", "value": "Kyiv"},
        {"label": "Kyiv City", "value": "Kyiv City"},
        {"label": "Kirovohrad", "value": "Kirovohrad"},
        {"label": "Luhans'k", "value": "Luhans'k"},
        {"label": "L'viv", "value": "L'viv"},
        {"label": "Mykolayiv", "value": "Mykolayiv"},
        {"label": "Odessa", "value": "Odessa"},
        {"label": "Poltava", "value": "Poltava"},
        {"label": "Rivne", "value": "Rivne"},
        {"label": "Sevastopol'", "value": "Sevastopol'"},
        {"label": "Sumy", "value": "Sumy"},
        {"label": "Ternopil'", "value": "Ternopil'"},
        {"label": "Transcarpathia", "value": "Transcarpathia"},
        {"label": "Vinnytsya", "value": "Vinnytsya"},
        {"label": "Volyn", "value": "Volyn"},
        {"label": "Zaporizhzhya", "value": "Zaporizhzhya"},
        {"label": "Zhytomyr", "value": "Zhytomyr"}
    ]

    YEAR_OPTIONS = [{"label": int(year), "value": int(year)} for year in range(1985, 2025)]

    inputs = [
        {
            "type": 'dropdown',
            "label": 'Select Data',
            "options": NOAA_OPTIONS,
            "key": 'ticker',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Select Area',
            "options": AREA_OPTIONS,
            "key": 'Area',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Select Year',
            "options": YEAR_OPTIONS,
            "key": 'Year',
            "action_id": "update_data"
        },
        {
            "type": 'text',
            "label": 'Enter Week Range (e.g., 5-10)',
            "key": 'week_range',
            "value": "",
            "action_id": "update_data"
        }
    ]

    controls = [{"type": "hidden",
                 "id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True

        }
    ]

    def getData(self, params):
        area = params['Area']
        year = int(params['Year'])
        start_week, end_week = map(int, params['week_range'].split('-'))

        plot_data = df[(df["area"] == area) &
                       (df["Year"] == year) &
                       (df["Week"].between(start_week, end_week))]

        return plot_data

    def getPlot(self, params):
        selected_column = params['ticker']
        plot_data = self.getData(params)

        plot = plot_data.plot(x='Week', y=selected_column, style='-o', grid=True, figsize=(10, 6), color="green")

        plot.set_title(f"Stock Data for {selected_column}")
        plot.set_xlabel("Week")
        plot.set_ylabel(selected_column)

        fig = plot.get_figure()
        return fig

directory = 'C:/Users/Arsen/Desktop/pythonANAL/lab2/csv_files'

def read(directory):
    files = os.listdir(directory)
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    main_df = pd.DataFrame()
    for i in range(len(files)):
        file_path = os.path.join(directory, files[i])
        df = pd.read_csv(file_path, header=1, names=headers)
        df = df.drop(df.loc[df['VHI'] == -1].index)
        df['area'] = i + 1
        df['Year'] = df['Year'].str.replace('<tt><pre>', '')
        df = df[~df['Year'].str.contains('</pre></tt>')]
        df.drop('empty', axis=1, inplace=True)
        df["Year"] = df["Year"].astype(int)
        df["Week"] = df["Week"].astype(int)
        main_df = pd.concat([main_df, df])
    return main_df


def changeID(df):
    cities = {1: "Cherkasy", 2: "Chernihiv", 3: "Chernivtsi", 4: "Crimea", 5: "Dnipropetrovs'k", 6: "Donets'k",
              7: "Ivano-Frankivs'k", 8: "Kharkiv", 9: "Kherson", 10: "Khmel'nyts'kyy", 11: "Kyiv", 12: "Kyiv City",
              13: "Kirovohrad", 14: "Luhans'k", 15: "L'viv", 16: "Mykolayiv", 17: "Odessa", 18: "Poltava", 19: "Rivne",
              20: "Sevastopol'", 21: "Sumy", 22: "Ternopil'", 23: "Transcarpathia", 24: "Vinnytsya", 25: "Volyn",
              26: "Zaporizhzhya", 27: "Zhytomyr"}
    df['area'] = df['area'].replace(cities)

    return df


df = changeID(read(directory))
print(df)
app = StockExample()
app.launch()
