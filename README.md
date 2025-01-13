# df-data-quality

### Install

- **Install via setuptools**:
  ```sh
    python setup.py install
  ```


### Usage Examples

- **Apply DQ rules on a dataset via CLI**:
  ```sh
    dq_app apply-rules --dataset_id "1" --env "dev"
  ```

  ##### If not installed
  ```sh
    python dq_app apply-rules --dataset_id "1" --env "dev"
  ```

- **Apply DQ rules on a dataset via API**:
  ##### Start the API server
  ```sh
    python dq_app/dq_app_api.py
  ```
  ##### Invoke the API endpoint
  ```sh
    https://<host name with port number>/apply-rules/{dataset_id}
    https://<host name with port number>/apply-rules/2
  ```
  ##### Invoke the API from Swagger Docs interface
  ```sh
    https://<host name with port number>/docs

    /apply-rules/{dataset_id}
    /apply-rules/2
  ```

### Sample Input

  ##### Dataset (source_data1.csv)
```
asset_id,asset_type,asset_name
1,equity,HCL Tech
2,mutual fund, Tata Digital Fund
```

### API Data (simulated)
These are metadata that would be captured via the DQ application UI and stored in a database.

  ##### datasets 
```
{
    "datasets": [
      {
        "dataset_id": "1",
        "catalog_ind": true,
        "file_delim": ",",
        "file_path": "APP_ROOT_DIR/data/source_data1.csv"
      },
      {
        "dataset_id": "2",
        "catalog_ind": true,
        "file_delim": ",",
        "file_path": "APP_ROOT_DIR/data/source_data2.csv"
      }
    ]
}
```

  ##### dq_expectations 
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

  ##### dq_rules 
```
{
    "dq_rules": [
      {
        "rule_id": "1",
        "dataset_id": "1",
        "exp_id": "1",
        "rule_fail_action": "abort",
        "column": "asset_id"
      },
      {
        "rule_id": "2",
        "dataset_id": "1",
        "exp_id": "2",
        "rule_fail_action": "abort",
        "column": "asset_type",
        "value_set": [
          "equity",
          "mutual fund"
        ]
      },
      {
        "rule_id": "3",
        "dataset_id": "1",
        "exp_id": "3",
        "rule_fail_action": "proceed",
        "column": "asset_id",
        "min_value": 5,
        "max_value": 50
      },
    ]
}
  
```

### Sample Output 

```
DQ check results for dataset 1
[
  {'rule_id': '1', 'result': True}, 
  {'rule_id': '2', 'result': True}, 
  {'rule_id': '3', 'result': False}
]
```
