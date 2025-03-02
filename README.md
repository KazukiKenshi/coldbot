# Project Setup

## Prerequisites
Ensure you have Python installed on your system. Additionally, you can use either Conda or Pip to install dependencies.

## Installation

### Using Conda (Recommended)
If you have Conda installed, create and activate the environment using the `environment.yml` file:

```sh
conda env create -f environment.yml
conda activate your_env_name
```

Replace `your_env_name` with the actual environment name defined in `environment.yml`.

### Using Pip
If you do not have Conda, install the dependencies using Pip:

```sh
pip install -r requirements.txt
```

## Running the Code
To execute the script, use the following command:

```sh
python main.py -d 0
```

### Flags and Their Usage
The script supports four flags to specify the context:

- `-d` → ERP Demo
- `-i` → Interview
- `-p` → Payment Follow-up
- `-o` → Request for Order Placement

Each flag should be followed by an integer that represents the index of the customer being addressed.

### Example Usage:
```sh
python main.py -i 2  # Start an interview with customer at index 2
python main.py -p 1  # Follow up on payment for customer at index 1
```

Ensure that the required dependencies are installed before running the script.

## Notes
- Make sure your data files and configurations are correctly set up.
- If using environment variables, configure them properly before execution.

For any issues, check the project documentation or reach out for support.

