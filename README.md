# ✈️ Flight Telemetry Operational & Safety Analytics Platform

##  Project Overview

An **end-to-end data engineering pipeline** for real-time flight telemetry analytics, processing data from **9,000+ active flights** across **93 countries**. This project implements industry-standard **Medallion Architecture** (Bronze-Silver-Gold) with automated ETL pipelines, delivering actionable insights for aviation operations, safety compliance, and executive decision-making.

---

##  Architecture

<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/ae08b542-58b3-435a-8dbe-e19c9d0492a5" />


### **Data Flow:**
```
OpenSky Network API → Bronze Layer (S3) → Silver Layer (S3) → Gold Layer (PostgreSQL) → Power BI Dashboards
                ↓
         Apache Airflow Orchestration
```

### **Layer Breakdown:**

| Layer | Purpose | Storage | Format | Records |
|-------|---------|---------|--------|---------|
| **Bronze** | Raw data ingestion | AWS S3 | JSON | 9,097 |
| **Silver** | Cleaned & validated data | AWS S3 | Parquet/CSV | 8,268 |
| **Gold** | Business-ready analytics | PostgreSQL | Tables | 3 data marts |

---

## 📊 Key Results & Insights

### **Data Quality Metrics:**
- ✅ **90.9% retention rate** after quality validation
- ✅ **100% data completeness** in final dataset
- ✅ **97.5% overall quality score**
- ✅ **0 duplicate records** (idempotent pipeline)

### **Business Insights:**
- 🌍 **8,268 flights** tracked in real-time
- 🇺🇸 **US dominates** with 5,505 flights (66.6%)
- 🛫 **99.7% in-air utilization** (8,244 flying / 24 on ground)
- 📈 **93 countries** represented globally

---

## 📈 Visualizations

### Top Countries by Flight Volume
<img width="1385" height="786" alt="image" src="https://github.com/user-attachments/assets/7676a049-a09f-478b-9ab8-143e9c4070be" />


### Altitude Distribution Analysis
<img width="1587" height="615" alt="image" src="https://github.com/user-attachments/assets/d5c9edc7-a412-4184-af6c-4dc0ebf30e5d" />


### Velocity vs Altitude Correlation
<img width="1305" height="786" alt="image" src="https://github.com/user-attachments/assets/e01cd686-50d9-4994-a248-9a3522dd4205" />


### Operational & Quality Metrics
<img width="1384" height="689" alt="image" src="https://github.com/user-attachments/assets/86e55fef-4cd9-4ddd-82cb-4cfd5e2e7a5b" />


### Regional Flight Distribution
<img width="1387" height="786" alt="image" src="https://github.com/user-attachments/assets/d69c0068-c726-4875-845d-0ca2b2e124f9" />

---

## 🛠️ Technology Stack

### **Core Technologies:**
| Category | Technology | Purpose |
|----------|-----------|---------|
| **Orchestration** | Apache Airflow | DAG scheduling, task dependencies |
| **Processing** | PySpark, Pandas | Distributed & batch data processing |
| **Storage** | AWS S3 | Scalable data lake (Bronze/Silver layers) |
| **Database** | PostgreSQL | Data warehouse (Gold layer) |
| **Visualization** | Power BI | Interactive dashboards & KPIs |
| **APIs** | OpenSky Network REST API | Real-time flight telemetry |
| **Languages** | Python 3.10 | ETL scripts, data transformations |

### **Python Libraries:**
- `pandas` - Data manipulation & analysis
- `pyspark` - Distributed data processing
- `boto3` - AWS S3 integration
- `psycopg2` - PostgreSQL connectivity
- `requests` - API data ingestion
- `matplotlib`, `seaborn` - Data visualization

---

## 📁 Project Structure
```
flight-telemetry-project/
├── data/                           # Bronze layer (raw JSON)
│   └── raw_flights_20251021_183758.json
├── silver/                         # Silver layer (cleaned data)
│   └── flights_cleaned_20251021.csv
├── gold/                           # Gold layer (analytics)
│   ├── flight_summary_by_country.csv
│   ├── daily_flight_statistics.csv
│   └── top_active_flights.csv
├── scripts/                        # ETL pipeline scripts
│   ├── test_api.py                # API connectivity test
│   ├── save_flight_data.py        # Data extraction
│   ├── bronze_to_silver_etl.py    # Cleaning & validation
│   └── silver_to_gold_aggregate.py # Aggregations
├── results/                        # Visualizations & outputs
│   ├── top_countries_flights.png
│   ├── altitude_analysis.png
│   ├── velocity_altitude_correlation.png
│   ├── operational_quality_metrics.png
│   └── regional_flight_distribution.png
├── docs/                           # Documentation
│   └── architecture_diagram.png
└── README.md
```

---

## 🔄 Data Pipeline Workflow

### **Phase 1: Data Ingestion (Bronze Layer)**
```python
# Extract from OpenSky Network API
GET https://opensky-network.org/api/states/all
↓
Save to S3: s3://flight-data-bronze/year=2025/month=10/day=21/
```

**Output:** 9,097 raw flight records (JSON format)

---

### **Phase 2: Data Cleaning (Silver Layer)**

**Transformations Applied:**

| Step | Operation | Records Lost | Purpose |
|------|-----------|-------------|---------|
| 1 | Null coordinate removal | -71 | Cannot track flights without position |
| 2 | String normalization | 0 | Trim whitespace from callsigns |
| 3 | Altitude range validation | -758 | Remove invalid values (<0m or >50km) |
| 4 | Deduplication | 0 | Ensure unique records (icao24 + timestamp) |
| 5 | Quality flagging | 0 | Add completeness metadata |

**Data Quality Checks:**
- ✅ Completeness validation (non-null coordinates)
- ✅ Range validation (altitude: 0-50,000m)
- ✅ Uniqueness enforcement (composite key deduplication)
- ✅ Data enrichment (quality flags)

**Output:** 8,268 validated records (CSV format)

---

### **Phase 3: Analytics Aggregation (Gold Layer)**

**Data Marts Created:**

**1. Flight Summary by Country** (93 rows)
```sql
SELECT 
    origin_country,
    COUNT(*) as total_flights,
    AVG(baro_altitude) as avg_altitude_m,
    MAX(baro_altitude) as max_altitude_m,
    AVG(velocity) as avg_velocity_ms,
    MAX(velocity) as max_velocity_ms,
    SUM(CASE WHEN on_ground THEN 1 ELSE 0 END) as flights_on_ground
FROM silver_flights
GROUP BY origin_country
ORDER BY total_flights DESC;
```

**2. Daily Flight Statistics** (1 row)
- Total flights, in-air vs on-ground split
- Unique country count, geographic diversity
- Average/max altitude and velocity metrics
- Data quality completeness percentage

**3. Top Active Flights** (20 rows)
- Most frequently tracked callsigns
- Average performance metrics per flight
- Operational monitoring dataset

---

## 🎓 Data Engineering Concepts Demonstrated

### **Architecture & Design:**
- ✅ **Medallion Architecture** - Bronze/Silver/Gold layers
- ✅ **ETL Pipeline** - Extract, Transform, Load pattern
- ✅ **Data Lake** - Scalable storage on AWS S3
- ✅ **Star Schema Design** - Fact/dimension table modeling
- ✅ **Idempotency** - Safe re-execution without duplicates

### **Data Quality:**
- ✅ **Schema Validation** - Enforce structure and types
- ✅ **Completeness Checks** - Null value handling
- ✅ **Range Validation** - Business rule enforcement
- ✅ **Deduplication** - Composite key uniqueness
- ✅ **Data Enrichment** - Quality metadata addition

### **Processing Patterns:**
- ✅ **Batch Processing** - Daily scheduled runs
- ✅ **Incremental Loads** - CDC-ready design
- ✅ **Partitioning** - Date-based data organization
- ✅ **Aggregation** - Pre-computed metrics for BI
- ✅ **Dimensional Modeling** - OLAP optimization

### **Advanced Concepts:**
- ✅ **Orchestration** - Airflow DAG workflows
- ✅ **Cloud Storage** - S3 bucket management
- ✅ **Data Warehousing** - PostgreSQL for analytics
- ✅ **API Integration** - REST endpoint consumption
- ✅ **Data Lineage** - Source-to-gold tracking

---

## 🚀 Future Enhancements

### **Phase 2: Real-Time Streaming**
- [ ] Implement **Apache Kafka** for event streaming
- [ ] Deploy **Kafka Producers** for continuous API polling
- [ ] Build **Kafka Consumers** for real-time processing
- [ ] Add **Spark Structured Streaming** for micro-batch windows

### **Phase 3: Advanced Analytics**
- [ ] Integrate **US DOT/BTS** historical delay data
- [ ] Implement **Change Data Capture (CDC)** for incremental updates
- [ ] Build **ML models** for delay prediction
- [ ] Add **anomaly detection** algorithms for safety alerts

### **Phase 4: Production Deployment**
- [ ] Migrate to **AWS EMR** for PySpark clusters
- [ ] Implement **AWS Glue** for managed ETL
- [ ] Deploy **Amazon RDS PostgreSQL** for data warehouse
- [ ] Add **CloudWatch** monitoring and alerts
- [ ] Implement **CI/CD pipeline** with GitHub Actions

### **Phase 5: Scalability**
- [ ] Optimize for **millions of records** daily
- [ ] Implement **data retention policies**
- [ ] Add **compression** and **file optimization**
- [ ] Enable **query performance tuning**

---

## 👥 Business Value & Use Cases

### **For Operations Managers:**
📊 **Dashboard:** Flight volume by country, gate assignments, resource allocation

**Key Questions Answered:**
- Which regions require more operational staff?
- What's the current in-air vs ground ratio?
- Which airports have the highest congestion?

### **For Safety & Compliance Analysts:**
🔍 **Dashboard:** Deviation tracking, altitude anomalies, data quality metrics

**Key Questions Answered:**
- Are all flights operating within safe altitude ranges?
- Which flights exhibit unusual behavior patterns?
- What's the data completeness for safety audits?

### **For Executive Leadership:**
📈 **Dashboard:** Daily KPIs, trend analysis, geographic market coverage

**Key Questions Answered:**
- What's our global operational coverage?
- How does today's volume compare to historical trends?
- What's the average flight efficiency (speed/altitude)?

---

## 📊 Sample Analytics Queries

### Query 1: Top 10 Busiest Countries
```sql
SELECT origin_country, COUNT(*) as flight_count
FROM gold.flight_summary_by_country
ORDER BY flight_count DESC
LIMIT 10;
```

### Query 2: High-Altitude Flights
```sql
SELECT callsign, origin_country, baro_altitude
FROM silver.flights_cleaned
WHERE baro_altitude > 12000
ORDER BY baro_altitude DESC;
```

### Query 3: Average Speed by Region
```sql
SELECT region, AVG(velocity) as avg_speed_ms
FROM silver.flights_cleaned
GROUP BY region
ORDER BY avg_speed_ms DESC;
```

---

## 🔧 Setup & Installation

### **Prerequisites:**
- Python 3.9+
- AWS Account (Free Tier)
- PostgreSQL 12+
- Apache Airflow 2.0+

### **Installation Steps:**
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/flight-telemetry-project.git
cd flight-telemetry-project

# Install dependencies
pip install pandas pyspark boto3 psycopg2-binary requests matplotlib seaborn

# Configure AWS credentials
aws configure

# Set up PostgreSQL database
psql -U postgres -c "CREATE DATABASE flight_analytics;"

# Run Bronze to Silver ETL
python scripts/bronze_to_silver_etl.py

# Run Silver to Gold aggregation
python scripts/silver_to_gold_aggregate.py
```

---

## 📚 Data Sources

### **Primary Source: OpenSky Network**
- **API:** `https://opensky-network.org/api/states/all`
- **Format:** JSON
- **Update Frequency:** Real-time (1-10 second intervals)
- **Coverage:** Global flight tracking
- **Fields:** ICAO24, callsign, position, altitude, velocity, heading

### **Secondary Source (Future): US DOT Bureau of Transportation Statistics**
- **Data:** Historical flight delays, on-time performance
- **Format:** CSV
- **Purpose:** Enrichment for delay analysis and OTP calculations

---

## 📝 Key Learnings

### **Technical Skills Developed:**
- Designed and implemented end-to-end ETL pipelines
- Applied data quality frameworks and validation strategies
- Built dimensional data models (star schema)
- Optimized queries for OLAP workloads
- Integrated cloud storage (AWS S3) with local processing
- Orchestrated workflows with Apache Airflow

### **Business Skills Developed:**
- Translated business requirements into technical solutions
- Created self-service analytics for non-technical stakeholders
- Implemented KPI tracking and monitoring dashboards
- Applied domain knowledge (aviation) to data validation

---

## 📄 License

This project is licensed under the MIT License.

---

##  Author

Sravani Elavarthi
---

##  Acknowledgments

- **OpenSky Network** for providing free flight tracking API
- **Apache Software Foundation** for Airflow and Spark
- **AWS** for cloud infrastructure and free tier



---

**⭐ If you found this project helpful, please star the repository!**
