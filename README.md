
# Hierarchical Autonomous Agent Swarm

## Overview
The Hierarchical Autonomous Agent Swarm (HAAS) is an advanced system composed of three interconnected agents, 
each specialized to perform tasks related to querying SQL database and analytics. 
This system enables efficient handling of natural language prompts to execute and analyze data from SQL database.

![Diagram.PNG](assets%2FDiagram.PNG)
## Features
- **Model Tuning Agent**: Responsible for interpreting user feedback and refining the capabilities of both the SQL-Agent and Analytics Agent.
- **SQL Agent**: Specializes in understanding and interfacing with SQL databases, trained with a Data Dictionary, SQL Entity-Relationship Diagram (ERD), and various SQL query examples.
- **Analytics Agent**: Utilizes data science methodologies to analyze data. It can be powered by libraries like PandasAI or equivalent custom-built solutions.

## WorkFlow
1. Prompt Processing: The user submits a natural language prompt to the MT-Agent.
2. Feedback Utilization: The MT-Agent optimizes the SQL-Agent based on previous feedback.
3. Query Formulation: The SQL-Agent, now fine-tuned, formulates a SQL query using a Language Model to Interface (LLM) system.
4. Data Retrieval: The SQL-Agent executes the SQL query and retrieves the data.
5. Data Presentation: The results, either as a DataFrame or a single data point, are presented to the user.
6. Analytics Execution: If detailed analytics are required, the DataFrame is passed to the Analytics Agent.
7. Analysis Output: The Analytics Agent performs the analysis and delivers the insights to the user.

## Project Structure
```angular2html
Hierarchical-Autonomous-Agent-Swarm
├── .env
├── .gitignore
├── assets
│   ├── Capture.PNG
│   └── LLM-SQL.pptx
├── data
├── lib
├── LICENSE.txt
├── logs
│   └── Process.log
├── models
├── notebooks
│   ├── SQL_Agent.ipynb
│   └── tools.ipynb
├── parameters
│   ├── config.json
│   ├── config_template.json
│   └── logs.ini
├── README.md
├── requirements
├── setup.py
```

## Requirements
- streamlit
- langchain
- pandas
- dotenv

## Setup and Installation
1. Clone the repository:
   ```
   git clone https://github.com/SlavPetkovic/Hierarchical-Autonomous-Agent-Swarm
   ```
2. Navigate to the project directory:
   ```
   cd Hierarchical-Autonomous-Agent-Swarm
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Set up your `.env` file with the necessary environment variables, such as your OpenAI API key.

## Usage
1. Start the Streamlit app:
   ```
   streamlit run swarm.py
   ```
2. 
3. 
4. 
5. 

## Logging
Logs are written to a file as configured in `parameters/logs.ini`. You can review these logs for debugging and monitoring the application's performance.

## Contributing
Contributions to this project are welcome. Please follow the standard fork-pull request workflow.

# Upcoming:
- Adding Llama 2 70b lanaguage as an optional LLM within app

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
