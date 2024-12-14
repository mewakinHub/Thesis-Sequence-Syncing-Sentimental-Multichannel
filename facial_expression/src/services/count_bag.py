import pandas as pd
from src.utils.custom_logger import get_custom_logger

logger = get_custom_logger(__name__)

class CountBag:
    def __init__(self, type_bag):
        self.type_bag = type_bag
        self.bag_counts = {type_name: 0 for type_name in set(type_bag.values())}
        self.all_bags = []

    def select_best_frame(self, interval_results): # public method: used in VideoProcessing
        if not interval_results:
            logger.warning("Interval results are empty.")
            return None
        
        try:
            best_frame = max(interval_results, key=lambda df: df['sum_conf'].iloc[0] if 'sum_conf' in df.columns and not df.empty else 0)
            logger.debug(f"Selected best_frame from interval results: \n{best_frame}")
            return best_frame
        except Exception as e:
            logger.error(f"Error selecting best frame: {e}")
            return None

    def update_count(self, df): # public method: used in VideoProcessing
        if df is not None:
            bag_type = df['result'].iloc[0] if 'result' in df.columns else 'empty'
            if bag_type in self.bag_counts:
                 self.bag_counts[bag_type] += 1
            else:
                # self.bag_counts[bag_type] = 0 # Optional: add new bag type
                logger.warning(f"Invalid bag type: {bag_type}. Skipping update.")
                return  # Exit the method to skip the update
            self.all_bags.append(df)
        logger.info(f"current bag_counts: \n{self.bag_counts}")

    def save_results(self): # public method: used in VideoProcessing
        if self.all_bags:
            all_bags_df = pd.concat(self.all_bags, ignore_index=True)
            all_bags_df.to_csv('outputs/all_bag.csv', index=False)
            bag_counts_df = pd.DataFrame(list(self.bag_counts.items()), columns=['Bag Type', 'Count'])
            bag_counts_df.to_csv('outputs/count_bag.csv', index=False)
            logger.info("Saved count bag results.")
        else:
            logger.warning("No bags to save.")