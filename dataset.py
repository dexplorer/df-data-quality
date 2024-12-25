class Dataset:
    kind = "generic"

    def __init__(self, dataset_id: str, cataloged_ind: bool):
        self.dataset_id = dataset_id
        self.cataloged_ind = cataloged_ind
        self.dq_rule_ids = []

    def add_dq_rule(self, dq_rule_id: str):
        self.dq_rule_ids.append(dq_rule_id)


class DelimFileDataset(Dataset):
    kind = "delim file"

    def __init__(self, dataset_id: str, cataloged_ind: bool, file_delim: str):
        super().__init__(dataset_id, cataloged_ind)
        self.file_delim = file_delim


class LocalDelimFileDataset(DelimFileDataset):
    kind = "local delim file"

    def __init__(
        self, dataset_id: str, cataloged_ind: bool, file_delim: str, file_path: str
    ):
        super().__init__(dataset_id, cataloged_ind, file_delim)
        self.file_path = file_path


class AWSS3DelimFileDataset(DelimFileDataset):
    kind = "aws s3 delim file"

    def __init__(
        self, dataset_id: str, cataloged_ind: bool, file_delim: str, s3_uri: str
    ):
        super().__init__(dataset_id, cataloged_ind, file_delim)
        self.s3_uri = s3_uri


class AzureADLSDelimFileDataset(DelimFileDataset):
    kind = "azure adls delim file"

    def __init__(
        self, dataset_id: str, cataloged_ind: bool, file_delim: str, adls_uri: str
    ):
        super().__init__(dataset_id, cataloged_ind, file_delim)
        self.adls_uri = adls_uri
