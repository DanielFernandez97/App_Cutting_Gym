import pandas as pd

dataset = pd.read_csv(r"D:\LLM gym dataset\archive\megaGymDataset.csv").Desc.to_list()




class GymLLM:

    def __init__(self, dataset):
        self.dataset = dataset


    def tokenizer(self):
        pass

    def embedding(self):
        pass

    def generate_text(self):
        pass
