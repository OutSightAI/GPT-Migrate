# GPT-Migrate

## AI Powered Legacy Code Migration 🪄

<details>
  <summary> Getting Started</summary>

### Step 1: Install Poetry

If Poetry is not already installed, you can install it using pip:

```sh
pip install poetry
```

For more installation options, visit the [Poetry documentation](https://python-poetry.org/docs/#installation).

### Step 2: Install Python 3.11

We use the deadsnakes PPA to install Python 3.11 on Ubuntu. Follow these commands:

```sh
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

### Step 3: Configure Poetry to Use Python 3.11

Ensure you're in your project directory, then run:

```sh
poetry env use python3.11
```

### Step 4: Install Project Dependencies

Install the necessary project dependencies by running:

```sh
poetry install
```

### Step 5: Activate the Poetry-Managed Virtual Environment

Activate the virtual environment managed by Poetry:

```sh
poetry shell
```

</details>
