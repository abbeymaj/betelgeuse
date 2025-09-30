## Betegeuse (Alpha Orionis) - Load Data (ETL) Pipeline

The objective of this project is to collect and analyze photometric magnitude data of Betelgeuse (Alpha Orionis) over time, enabling insights into its pulsation cycles, dimming events, and pre-supernova behavior.

The project fetches and stores the Magnitude data for Betelgeuse from the Association of Variable Star Observers (AAVSO) website. 

The project defines an Extract Transform Load (ETL) pipeline that cleans, transforms and then loads the fetched data into a SQLite database.

The database is updated on a weekly basis (every Sunday) by a cron job that leverages GitHub Actions to trigger the job.
The project exposes the link to the database via an API, which was created using GitHub Pages. This enables the data to be used by other programs or for analysis.

The project has been created using Python and its associated libraries. 

### 🌟 About Betelgeuse (Alpha Orionis)

Betelgeuse is a captivating red supergiant star located in the constellation Orion, approximately **642 light-years** from Earth. As one of the brightest and most studied stars in the night sky, Betelgeuse marks the shoulder of Orion and has fascinated astronomers for centuries due to its dramatic variability and impending stellar fate.

Classified as a **semi-regular variable star**, Betelgeuse exhibits fluctuations in brightness caused by complex pulsations and convective activity in its vast outer layers. These changes make it an ideal candidate for long-term magnitude monitoring and astrophysical modeling.

![Betelgeuse (Alpha Orionis)](https://github.com/abbeymaj80/my-ml-datasets/blob/master/screenshots/betelgeuse/betelgeuse-in-orion.png)

Here are some fascinating facts that highlight Betelgeuse’s stellar drama:

- 🌌 **Colossal Size**: Estimated to be **764 times the radius of the Sun**. If placed at the center of our solar system, Betelgeuse would engulf Mercury, Venus, Earth, Mars, and possibly Jupiter.
- 🔭 **Variable Brightness**: Its apparent magnitude ranges from **+0.0 to +1.6**, making it one of the few stars whose brightness visibly changes to the naked eye.
- 💥 **Supernova Candidate**: Betelgeuse is nearing the end of its life and is expected to explode as a **Type II supernova** within the next 100,000 years—a cosmic blink of an eye.
- 🌬️ **Massive Mass Loss**: Continuously sheds material into space, forming a dusty envelope that obscures and dims its light during outbursts.
- 🧪 **Complex Chemistry**: Its extended atmosphere contains molecules like carbon monoxide and silicon monoxide, contributing to its infrared brightness.
- 🧊 **Cool Surface**: Despite its luminosity, Betelgeuse has a surface temperature of only **~3,500 K**, much cooler than the Sun’s **~5,778 K**.
- 🧭 **2020 Dimming Event**: In late 2019 and early 2020, Betelgeuse underwent an unprecedented dimming, sparking global speculation about an imminent supernova. It was later attributed to a combination of dust ejection and surface cooling.

> 🧠 Betelgeuse reminds us that even the most familiar stars can surprise us—and that cosmic change is always unfolding above our heads.

### 🚀 Project Installation

Install the project using pip. It is always recommended to use a virtual environment (for example, using anaconda) to do the installation.

This project was built using Python 3.9.

To install the project, use the following: 

```bash
  pip install -r requirements.txt
```
    
### 🧰 Tech Stack

**Language:** Python

**CI/CD:** GitHub Actions

**Database:** SQLite

**API:** GitHub Pages

### 🧭 High-Level Design Documentation

The high-level design diagram for the ETL pipeline of the project is depicted below:

![High-Level Design Diagram](https://github.com/abbeymaj80/my-ml-datasets/blob/master/screenshots/betelgeuse/High_Level_Design.png)

Detailed information on the project as well as the ETL process can be found in the project's high-level design document.

The link to the high-level design document is as follows:

- 📄 [High-Level Design Document](https://github.com/abbeymaj80/my-ml-datasets/raw/refs/heads/master/Design_Docs/Betelgeuse_Load_Data_HLD.docx): Overview of the data ingestion pipeline for Betelgeuse magnitude tracking.

### 📚 References

- 🌠 [**American Association of Variable Star Observers (AAVSO)**](https://www.aavso.org/): A global community of amateur and professional astronomers contributing to variable star observations.
- 📚 [**Betelgeuse – Wikipedia**](https://en.wikipedia.org/wiki/Betelgeuse): Comprehensive overview of Betelgeuse’s properties, variability, and historical significance.