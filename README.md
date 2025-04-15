# Penn State Web Scrapers: OrgCentral, Bulletins, and Undergraduate Majors

This project contains Python scripts to scrape information from the following Penn State websites:

*   **OrgCentral:** [https://orgcentral.psu.edu/organizations](https://orgcentral.psu.edu/organizations)
*   **Bulletins (Undergraduate Course Descriptions):** [https://bulletins.psu.edu/university-course-descriptions/undergraduate/](https://bulletins.psu.edu/university-course-descriptions/undergraduate/)
*   **Undergraduate Majors:** [https://www.psu.edu/academics/undergraduate/majors](https://www.psu.edu/academics/undergraduate/majors)

## Setup

Follow these steps to set up your environment and install dependencies.

### 1. Create a Python Environment

Choose **one** of the following methods:

**Using `conda` (Recommended if you use Anaconda/Miniconda):**

Replace `myenv` with your desired environment name.

```bash
conda create --name myenv python=3.12
conda activate myenv
```

**Using Python's built-in `venv`:**

Replace `venv` with your desired environment directory name.

*   On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
*   On Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

### 2. Install Dependencies

Once your environment is activated, install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the desired scraper script from your activated environment:

*   **OrgCentral:**
    ```bash
    python main.py
    ```
*   **Bulletins:**
    ```bash
    python bulletins.py
    ```
*   **Undergraduate Majors:**
    ```bash
    python ugradmajors.py
    ```
