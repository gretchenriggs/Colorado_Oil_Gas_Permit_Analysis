import pandas as pd

def cleanup(df):
    # Splitting facility_name_num into 2 columns for facility_name &
    #    facility_num.  Stripping spaces from start/end of facility_num
    df['facility_name'], df['facility_num'] = df['facility_name_num']\
                                                 .str.split("    ", 1)\
                                                 .str
    df['facility_num'] = df['facility_num'].str.strip()

    # Splitting field_name_num into 2 columns for field_name &
    #    field_num.  Stripping spaces from start/end of field_num
    df['field_name'], df['field_num'] = df['field_name_num']\
                                           .str.split("    ", 1)\
                                           .str
    df['field_num'] = df['field_num'].str.strip()

    # Splitting location into 2 columns for county &
    #    coord.  Stripping spaces from start/end of coord
    df['county'], df['coord'] = df['location']\
                                   .str.split("    ", 1)\
                                   .str
    df['coord'] = df['coord'].str.strip()

    # Splitting operator_name_num into 2 columns for operator_name &
    #    operator_num.  Stripping spaces from start/end of field_num
    df['operator_name'], df['operator_num'] = df['operator_name_num']\
                                                 .str.split("    ", 1)\
                                                 .str
    df['operator_num'] = df['operator_num'].str.strip()

    # Splitting well status from the permit date in the status column
    df['well_status'] = df['status'].apply(lambda x: x[0:2])
    df.loc[df['well_status'] == "N/", "status"] = "N/A"

    # Creating permit_date column by removing leading facility status code
    #    letters and any "N/A" values from the permit status date, and
    #    converting from a string to utf-8 format
    df['permit_date'] = df['status'].apply(lambda x: x.decode('utf-8'))\
                                    .str.replace("AB","")\
                                    .str.replace("AC","")\
                                    .str.replace("AL","")\
                                    .str.replace("CL","")\
                                    .str.replace("CM","")\
                                    .str.replace("DA","")\
                                    .str.replace("DG","")\
                                    .str.replace("DM","")\
                                    .str.replace("IJ","")\
                                    .str.replace("PA","")\
                                    .str.replace("pa","")\
                                    .str.replace("PD","")\
                                    .str.replace("PR","")\
                                    .str.replace("RC","")\
                                    .str.replace("SI","")\
                                    .str.replace("SU","")\
                                    .str.replace("TA","")\
                                    .str.replace("WO","")\
                                    .str.replace("XX","")\
                                    .str.replace("N/A","")\
                                    .str.replace(u"\xa0", u"")
    # Saving N/A status data value (was replaced with "") to NaT
    df.loc[df['permit_date'] == u"", "permit_date"] = pd.NaT
    df['permit_date'] = pd.to_datetime(df['permit_date'])

    # Dropping the original combined columns from the DataFrame & unneeded
    #    columns
    df.drop(['facility_name_num', 'field_name_num', 'operator_name_num', \
             'location', 'status'],\
             axis=1, inplace=True)
    df.drop(['Unnamed: 0', 'related_facilities'], axis=1, inplace=True)

    # Drop any duplicate rows
    df.drop_duplicates()

    return df


if __name__ == '__main__':
    df = pd.read_csv("data/older_well_permits.csv")
    df = cleanup(df)
    df.to_csv("data/older_well_permits_clean.csv")
