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
