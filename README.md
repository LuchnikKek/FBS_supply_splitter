# WB FBS Supply Splitter

Small Python-script. On startup splits all FBS orders by supplies with same names.
Creates supplies if needed.

## Installation
1. Paste your TOKEN from WB API into **_.env.example_** and rename it to just **_.env_**.
2. ```bash
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