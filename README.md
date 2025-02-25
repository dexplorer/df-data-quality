# df-data-quality

### Install

- **Install via Makefile and pip**:
  ```sh
    make install
  ```

### Usage Examples

- **Apply DQ rules on a dataset via CLI**:
  ```sh
    dq-app-cli apply-rules --dataset_id "dataset_1" --env "dev"
  ```

- **Apply DQ rules on a dataset via CLI with cycle date override**:
  ```sh
    dq-app-cli apply-rules --dataset_id "dataset_1" --env "dev" --cycle_date "2024-12-26"
  ```

- **Apply DQ rules on a dataset via API**:
  ##### Start the API server
  ```sh
    dq-app-api --env "dev"
  ```
  ##### Invoke the API endpoint
  ```sh
    https://<host name with port number>/apply-rules/?dataset_id=<value>
    https://<host name with port number>/apply-rules/?dataset_id=<value>&cycle_date=<value>

    /apply-rules/?dataset_id=dataset_1
    /apply-rules/?dataset_id=dataset_1&cycle_date=2024-12-26
  ```
  ##### Invoke the API from Swagger Docs interface
  ```sh
    https://<host name with port number>/docs

  ```

### Sample Input

  ##### Dataset (assets_20241226.csv)
```
effective_date,asset_id,asset_type,asset_name
2024-12-26,1,equity,HCL Tech
2024-12-26,2,mutual fund, Tata Digital Fund
```

### API Data (simulated)
These are metadata that would be captured via the DQ application UI and stored in a database.

  ##### Datasets 
```
{
  "datasets": [
    {
      "dataset_id": "dataset_1",
      "dataset_type": "local delim file",
      "file_delim": ",",
      "file_path": "APP_DATA_IN_DIR/assets_yyyymmdd.csv",
      "schedule_id": "schedule_2",
      "recon_file_delim": "|",
      "recon_file_path": "APP_DATA_IN_DIR/assets_yyyymmdd.recon"
    }
  ]
}
```

  ##### DQ Expectations 
```
{
    "dq_expectations": [
      {
        "exp_id": "1",
        "exp_name": "ExpectColumnValuesToBeUnique",
        "ge_method": "ExpectColumnValuesToBeUnique"
      },
      {
        "exp_id": "2",
        "exp_name": "ExpectColumnValuesToBeInSet",
        "ge_method": "ExpectColumnValuesToBeInSet"
      },
      {
        "exp_id": "3",
        "exp_name": "ExpectColumnValuesToBeBetween",
        "ge_method": "ExpectColumnValuesToBeBetween"
      },
      {
        "exp_id": "4",
        "exp_name": "ExpectColumnValuesToNotBeNull",
        "ge_method": "ExpectColumnValuesToNotBeNull"
      }
    ]
  }
  
```

  ##### Dataset DQ Rules 
```
{
    "dq_rules": [
      {
        "dataset_id": "dataset_1",
        "rule_id": "1",
        "exp_id": "1",
        "rule_fail_action": "abort",
        "column": "asset_id"
      },
      {
        "dataset_id": "dataset_1",
        "rule_id": "2",
        "exp_id": "2",
        "rule_fail_action": "abort",
        "column": "asset_type",
        "value_set": [
          "equity",
          "mutual fund"
        ]
      },
      {
        "dataset_id": "dataset_1",
        "rule_id": "3",
        "exp_id": "3",
        "rule_fail_action": "proceed",
        "column": "asset_id",
        "min_value": 5,
        "max_value": 50
      }
    ]
  }
  
```

### Sample Output 

```
DQ check results for dataset 1

[
  {'rule_id': '1', 'result': 'Pass', 'expectation': 'ExpectColumnValuesToBeUnique'}, 
  {'rule_id': '2', 'result': 'Pass', 'expectation': 'ExpectColumnValuesToBeInSet'}, 
  {'rule_id': '3', 'result': 'Fail', 'expectation': 'ExpectColumnValuesToBeBetween'}
]
```
