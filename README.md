# WB FBS Supply Splitter

Small Python-script. On startup splits all FBS orders into pre-created supplies. 

## Installation
1. Set ARTICLE_TO_SUPPLY_NAME dict in **_./constants.py_** to your values.
2. Paste your TOKEN from WB API into **_.env.example_** and rename it to just **_.env_**.
3.  ```bash
    docker build -t sup_former .
    ```

## Usage

```bash
docker run sup_former
```

## Contributing

(r u sure u want?) Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)