## UK Work Visa Dashboard

This Streamlit application is deployed and accessible at: [https://uk-work-visa-dashboard.streamlit.app](https://uk-work-visa-dashboard.streamlit.app)

**Description**

This Streamlit application allows users to explore data on UK work visa sponsors. Users can search for organisations by name, filter data by location, visa route, and sponsor type, and view charts that provide an overview of the data.

If you have any ideas for improvement, bug fixes, or new features, feel free to fork the repository, make your changes, and submit a pull request.

**Data Source**

The application fetches data from daily published CSVs hosted on the UK Government's Publishing Service. You can find more information about the Register of Licensed Sponsors: Workers on [https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers). The script iterates over the past 15 days to find the most recent data file.

**Code Structure**

The code is divided into following sections:

1. **Page configuration:** Sets the page title, icon, layout, and theme.
2. **Function definitions:**
    - `clean_strings`: Cleans text data by removing leading symbols, brackets, commas, and extra spaces.
    - `fetch_data`: Iterates over the past 15 days to find the most recent data file and returns the cleaned DataFrame and last updated date.
3. **Data retrieval:**
    - Iterates over the past 15 days to find the most recent data file.
    - Reads the CSV data from the URL and cleans the column values.
4. **App layout:**
    - Sets the app title and displays the last updated date.
    - Creates a sidebar for searching organisations and filtering data.
    - Displays an overview section with key metrics about the data.
    - Shows a table of the filtered data.
    - Creates bar charts to visualise the distribution of organisations by town/city and visa route.

**Running the application**

1. Clone the repository:
    ```sh
    git clone https://github.com/adarshsaji/UK-Work-Visa-Dashboard.git
    ```
2. Ensure you have Python 3 installed and install the required libraries using:
    ```sh
    pip install -r requirements.txt
    ```
3. Run the application from your terminal using:
    ```sh
    streamlit run src/app.py
    ```

**Note:**

This application retrieves data from an external source. The availability and format of the data may change over time.
