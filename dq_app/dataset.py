from dataclasses import dataclass
import json
from utils import file_io as uff

import logging


@dataclass
class Dataset:
    kind: str
    dataset_id: str
    catalog_ind: str
    dq_rule_ids: list[str]

    def __init__(self, dataset_id: str, catalog_ind: bool):
        self.kind = "generic"
        self.dataset_id = dataset_id
        self.catalog_ind = catalog_ind
        self.dq_rule_ids = []

    @classmethod
    def from_json(self, json_file, json_key, dataset_id):
        # with open(json_file, 'r') as f:
        with uff.uf_open_file(file_path=json_file, open_mode="r") as f:
            datasets = json.load(f)[json_key]
            # print(datasets)

        try:
            if datasets:
                for dataset in datasets:
                    # print(dataset)
                    if dataset["dataset_id"] == dataset_id:
                        return self(**dataset)
            else:
                raise ValueError("Dataset data is invalid.")
        except ValueError as error:
            logging.error(error)
            raise

    def add_dq_rule(self, dq_rule_id: str):
        self.dq_rule_ids.append(dq_rule_id)


@dataclass
class DelimFileDataset(Dataset):
    file_delim: str

    def __init__(self, dataset_id: str, catalog_ind: bool, file_delim: str):
        super().__init__(dataset_id, catalog_ind)
        self.kind = "delim file"
        self.file_delim = file_delim


@dataclass
class LocalDelimFileDataset(DelimFileDataset):
    file_path: str

    def __init__(
        self, dataset_id: str, catalog_ind: bool, file_delim: str, file_path: str
    ):
        super().__init__(dataset_id, catalog_ind, file_delim)
        self.kind = "local delim file"
        self.file_path = file_path


@dataclass
class AWSS3DelimFileDataset(DelimFileDataset):
    s3_uri: str

    def __init__(
        self, dataset_id: str, catalog_ind: bool, file_delim: str, s3_uri: str
    ):
        super().__init__(dataset_id, catalog_ind, file_delim)
        self.kind = "aws s3 delim file"
        self.s3_uri = s3_uri


@dataclass
class AzureADLSDelimFileDataset(DelimFileDataset):
    adls_uri: str

    def __init__(
        self, dataset_id: str, catalog_ind: bool, file_delim: str, adls_uri: str
    ):
        super().__init__(dataset_id, catalog_ind, file_delim)
        self.kind = "azure adls delim file"
        self.adls_uri = adls_uri
