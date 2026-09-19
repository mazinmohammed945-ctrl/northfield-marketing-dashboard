# Northfield & Co. — E-commerce Marketing Analytics Dashboard

An interactive **E-commerce Marketing Analytics Dashboard** built using Python, Pandas, Plotly, and Streamlit to analyze revenue performance, new-customer acquisition, marketing expenditure, promotions, and marketing efficiency.

## 📌 Project Overview

This project analyzes daily e-commerce data for **Northfield & Co.** and transforms the raw dataset into an interactive business analytics dashboard.

The analysis focuses on understanding:

* Overall revenue performance
* New-customer revenue and acquisition
* Paid media expenditure
* Marketing efficiency and ROAS
* Promotional and mailing activity
* Relationships between marketing spend and revenue
* Revenue patterns over time

The final dashboard allows users to interactively filter the data and explore business performance from different perspectives.

## 📊 Dataset

The dataset was provided as an Excel workbook:

**`Northfield_Co_Case_Study.xlsx`**

The analysis uses the **Master data** sheet.

### Dataset characteristics

* **Rows:** 852
* **Variables:** 23
* **Period:** 1 April 2024 – 31 July 2026
* **Frequency:** Daily
* **Domain:** US E-commerce

### Main categories of variables

**Revenue**

* Total Revenue
* New-Customer Revenue

**Paid Media Spend**

* Google
* Meta
* Microsoft
* Criteo
* Outbrain
* Awin
* Influencer

**Marketing & Promotional Activities**

* Site-wide promotions
* UWG mailings
* Offline promotions
* Holidays
* BFCM promotional activity

## 🧹 Data Preprocessing

The dataset was validated and prepared before analysis.

The preprocessing included:

1. Checking the dataset structure and data types
2. Checking for missing values
3. Checking for duplicate observations
4. Converting the `Date` variable into a date format
5. Creating time-based variables
6. Aggregating marketing expenditure
7. Creating business-oriented analytical metrics

## ⚙️ Feature Engineering

Several derived variables were created to support the analysis.

### Total Media Spend

Total paid media expenditure was calculated by combining spending across the available marketing channels.

**Total Media Spend = Google + Meta + Microsoft + Criteo + Outbrain + Awin + Influencer Spend**

### New-Customer Share

Measures the proportion of total revenue generated from new customers.

**New-Customer Share = New-Customer Revenue / Total Revenue**

### ROAS

A descriptive marketing-efficiency metric was calculated as:

**ROAS = Total Revenue / Total Media Spend**

It represents the amount of revenue generated relative to paid media expenditure.

### Time Variables

The following variables were derived from the date:

* Month
* Year
* Month Name
* Day of Week

These variables were used for time-based analysis and visualizations.

## 📈 Dashboard Features

### 1. Executive Overview

The dashboard provides an overview of business performance through key performance indicators (KPIs):

* Total Revenue
* New-Customer Revenue
* New-Customer Share
* Paid Media Spend
* Revenue-to-Media-Spend Ratio

The full dataset generates approximately **$52.9 million in total revenue**.

### 2. Revenue Analysis

The dashboard includes:

* Daily revenue trend
* Total Revenue vs New-Customer Revenue
* Monthly revenue analysis
* Monthly revenue-to-media-spend analysis

These visualizations help identify revenue patterns, peaks, declines, and changes over time.

### 3. Marketing & Promotion Analysis

Marketing and promotional activities are compared using event and non-event periods.

The dashboard allows analysis of:

* Site-wide promotions
* UWG mailings
* Offline promotions
* Holidays
* BFCM promotional periods

Performance is compared using measures such as:

* Average daily revenue
* Average new-customer revenue
* Average media spend

### 4. Acquisition & Efficiency

The acquisition section focuses on new-customer performance and relationships between marketing expenditure and revenue.

Visualizations include:

* Total Revenue vs Total Paid Media Spend
* New-Customer Revenue vs Meta Spend
* Channel-level revenue correlations

### 5. Data Quality

The dashboard includes checks for:

* Number of rows
* Missing values
* Duplicate records
* Unique dates

This provides transparency about the quality of the data used for analysis.

## 🎛️ Interactive Filters

Users can interact with the dashboard using:

* Date range
* Site-wide promotion status
* UWG mailing status

These filters allow users to investigate specific periods and marketing conditions.

## 🔎 Analytical Approach

The project follows an end-to-end analytics workflow:

```text
Raw Excel Dataset
       ↓
Data Validation
       ↓
Data Preprocessing
       ↓
Feature Engineering
       ↓
Exploratory Data Analysis
       ↓
Business Metrics
       ↓
Interactive Visualizations
       ↓
Streamlit Dashboard
       ↓
Business Insights
```

## ⚠️ Analytical Considerations

The analysis is primarily **descriptive and observational**.

Correlation between marketing spend and revenue does not establish causation. Revenue may also be influenced by factors such as:

* Promotions
* Holidays
* Seasonality
* Mailings
* Other marketing activities

Similarly, ROAS in this project is based on **revenue relative to media spend** and should not be interpreted as a measure of profitability.

## 🛠️ Technologies Used

* **Python**
* **Pandas** — Data manipulation and preprocessing
* **Plotly** — Interactive visualizations
* **Streamlit** — Interactive dashboard development
* **Excel** — Source dataset
* **GitHub** — Version control and project hosting

## 📁 Project Structure

```text
Northfield-Marketing-Dashboard/
│
├── dashboard.py
├── Northfield_Co_Case_Study.xlsx
├── requirements.txt
└── README.md
```

## 🚀 How to Run Locally

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_NAME>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser.

## 🌐 Live Dashboard

**Streamlit App:**
https://northfield-marketing-dashboard-9kqbundabwelbsf6sshcqh.streamlit.app/

## 💡 Key Learning Outcomes

Through this project, I worked through an end-to-end data analytics workflow involving:

* Data cleaning and validation
* Exploratory data analysis
* Feature engineering
* Business KPI development
* Marketing analytics
* Customer acquisition analysis
* Data visualization
* Interactive dashboard development
* GitHub project management
* Streamlit deployment

## 👤 Author

**Mazin Mohammed**

This project was developed as an e-commerce marketing analytics case study to demonstrate practical skills in **data analysis, visualization, dashboard development, and business reporting**.
