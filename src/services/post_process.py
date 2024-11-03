import statistics
import pandas as pd
import numpy as np
from src.utils.custom_logger import get_custom_logger

logger = get_custom_logger(__name__)

class PostProcess:
    def __init__(self, type_bag):
        self.type_bag = type_bag

    def perform_voting(self, df):
        res_bag_type = []
        bag_df = df[df['class'] == 0]
        if bag_df.empty:
            df['result'] = ["empty"] * len(df)
            df['sum_conf'] = 0
            return df

        for val_df_bag in bag_df.bdbox:
            voted = []
            for val_df_sign, val_type_bag in zip(df[df['class'] != 0].bdbox, df[df['class'] != 0].type_bag):
                if self.__calculate_intersection(val_df_sign, val_df_bag):
                    voted.append(val_type_bag)
            try: # voting
                res_bag_type.append(statistics.mode(voted))
            except statistics.StatisticsError:
                res_bag_type.append("empty")
        df.loc[df['class'] == 0, 'result'] = res_bag_type
        df.loc[df['class'] == 0, 'sum_conf'] = df[df['class'] != 0]['conf'].sum() if not df[df['class'] != 0].empty else 0
        return df

    # for checking if label box inside bag or not before voting
    def __calculate_intersection(self, box1, box2):
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])
        intersection_area = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
        smaller_box_area = min((box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1), (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1))
        intersection_percentage = (intersection_area / smaller_box_area)
        return intersection_percentage > 0.6
