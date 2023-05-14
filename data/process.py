import pandas as pd

DIR_INCOME = "personal_income_sa2_2011_2018.csv"
DIR_AGE_FEMALE = "work_travel_method_by_age_by_female_2016.csv"
DIR_AGE_MALE = "work_travel_method_by_age_by_male_2016.csv"

INCOME_COLS = {" sa2_code": "sa2_code",
               " sa2_name": "sa2_name",
               " median_aud_2016_17": "median_income",
               " mean_aud_2016_17": "mean_income",
               " earners_persons_2016_17": "num_earners"}

AGE_SEX_FEMALE_COLS = {" sa2_main16": "sa2_code",
                       " sa2_name16": "sa2_name",

                       " f_m1_bus_15_24": "female_bus_15_24",
                       " f_m1_bus_25_34": "female_bus_25_34",
                       " f_m1_bus_35_44": "female_bus_35_44",
                       " f_m1_bus_45_54": "female_bus_45_54",
                       " f_m1_bus_55_64": "female_bus_55_64",
                       " f_m1_bus_65_74": "female_bus_65_74",
                       " f_m1_bus_75ov": "female_bus_over_75",
                       " f_m1_bus_tot": "female_bus_total",

                       " f_m1_carasdriv_15_24": "female_car_driver_15_24",
                       " f_m1_carasdriv_25_34": "female_car_driver_25_34",
                       " f_m1_carasdriv_35_44": "female_car_driver_35_44",
                       " f_m1_carasdriv_45_54": "female_car_driver_45_54",
                       " f_m1_carasdriv_55_64": "female_car_driver_55_64",
                       " f_m1_carasdriv_65_74": "female_car_driver_65_74",
                       " f_m1_carasdriv_75ov": "female_car_driver_over_75",
                       " f_m1_carasdriv_tot": "female_car_driver_total",

                       " f_m1_caraspas_15_24": "female_car_passenger_15_24",
                       " f_m1_caraspas_25_34": "female_car_passenger_25_34",
                       " f_m1_caraspas_35_44": "female_car_passenger_35_44",
                       " f_m1_caraspas_45_54": "female_car_passenger_45_54",
                       " f_m1_caraspas_55_64": "female_car_passenger_55_64",
                       " f_m1_caraspas_65_74": "female_car_passenger_65_74",
                       " f_m1_caraspas_75ov": "female_car_passenger_over_75",
                       " f_m1_caraspas_tot": "female_car_passenger_total",

                       " f_m1_train_15_24": "female_train_15_24",
                       " f_m1_train_25_34": "female_train_25_24",
                       " f_m1_train_35_44": "female_train_35_24",
                       " f_m1_train_45_54": "female_train_45_24",
                       " f_m1_train_55_64": "female_train_55_24",
                       " f_m1_train_65_74": "female_train_65_24",
                       " f_m1_train_75ov": "female_train_over_75",
                       " f_m1_train_tot": "female_train_total",

                       " f_m1_tram_inc_lr_15_24": "female_tram_15_24",
                       " f_m1_tram_inc_lr_25_34": "female_tram_25_34",
                       " f_m1_tram_inc_lr_35_44": "female_tram_35_44",
                       " f_m1_tram_inc_lr_45_54": "female_tram_45_54",
                       " f_m1_tram_inc_lr_55_64": "female_tram_55_64",
                       " f_m1_tram_inc_lr_65_74": "female_tram_65_74",
                       " f_m1_tram_inc_lr_75ov": "female_tram_over_75",
                       " f_m1_tram_inc_lr_tot": "female_tram_total"}

AGE_SEX_MALE_COLS = {" sa2_main16": "sa2_code",
                     " sa2_name16": "sa2_name",

                     " m_m1_bus_15_24": "male_bus_15_24",
                     " m_m1_bus_25_34": "male_bus_25_34",
                     " m_m1_bus_35_44": "male_bus_35_44",
                     " m_m1_bus_45_54": "male_bus_45_54",
                     " m_m1_bus_55_64": "male_bus_55_64",
                     " m_m1_bus_65_74": "male_bus_65_74",
                     " m_m1_bus_75ov": "male_bus_over_75",
                     " m_m1_bus_tot": "male_bus_total",

                     " m_m1_carasdriv_15_24": "male_car_driver_15_24",
                     " m_m1_carasdriv_25_34": "male_car_driver_25_34",
                     " m_m1_carasdriv_35_44": "male_car_driver_35_44",
                     " m_m1_carasdriv_45_54": "male_car_driver_45_54",
                     " m_m1_carasdriv_55_64": "male_car_driver_55_64",
                     " m_m1_carasdriv_65_74": "male_car_driver_65_74",
                     " m_m1_carasdriv_75ov": "male_car_driver_over_75",
                     " m_m1_carasdriv_tot": "male_car_driver_total",

                     " m_m1_caraspas_15_24": "male_car_passenger_15_24",
                     " m_m1_caraspas_25_34": "male_car_passenger_25_34",
                     " m_m1_caraspas_35_44": "male_car_passenger_35_44",
                     " m_m1_caraspas_45_54": "male_car_passenger_45_54",
                     " m_m1_caraspas_55_64": "male_car_passenger_55_64",
                     " m_m1_caraspas_65_74": "male_car_passenger_65_74",
                     " m_m1_caraspas_75ov": "male_car_passenger_over_75",
                     " m_m1_caraspas_tot": "male_car_passenger_total",

                     " m_m1_train_15_24": "male_train_15_24",
                     " m_m1_train_25_34": "male_train_25_24",
                     " m_m1_train_35_44": "male_train_35_24",
                     " m_m1_train_45_54": "male_train_45_24",
                     " m_m1_train_55_64": "male_train_55_24",
                     " m_m1_train_65_74": "male_train_65_24",
                     " m_m1_train_75ov": "male_train_over_75",
                     " m_m1_train_tot": "male_train_total",

                     " m_m1_tram_inc_lr_15_24": "male_tram_15_24",
                     " m_m1_tram_inc_lr_25_34": "male_tram_25_34",
                     " m_m1_tram_inc_lr_35_44": "male_tram_35_44",
                     " m_m1_tram_inc_lr_45_54": "male_tram_45_54",
                     " m_m1_tram_inc_lr_55_64": "male_tram_55_64",
                     " m_m1_tram_inc_lr_65_74": "male_tram_65_74",
                     " m_m1_tram_inc_lr_75ov": "male_tram_over_75",
                     " m_m1_tram_inc_lr_tot": "male_tram_total"}


def filter_cols(dir, cols):
    # collect and rename columns
    df = pd.read_csv(dir)
    df = df[cols.keys()]
    df.rename(columns=cols, inplace=True)

    # drop any row with no SA2 code/anem
    df = df[df["sa2_code"].notna()]
    return df[df["sa2_name"].notna()]



# collect datasets - with columns needed
df_income = filter_cols(DIR_INCOME, INCOME_COLS)
df_age_female = filter_cols(DIR_AGE_FEMALE, AGE_SEX_FEMALE_COLS)
df_age_male = filter_cols(DIR_AGE_MALE, AGE_SEX_MALE_COLS)

# join by SA2
df = pd.merge(df_income, df_age_female, on="sa2_code", how="inner")
df = pd.merge(df, df_age_male, on="sa2_code", how="inner")
df.drop(columns=["sa2_name_x", "sa2_name_y"], inplace=True)

df.to_csv("sudo_data.csv")
