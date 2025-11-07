### design patterns
- design patterns:
    - reflection
        - for preliminary eda, no need?
        - for further analysis, critic on the analysis method, results, with code output&error msg?
        - example on the chart creation use case:
            1) load dataset
            2) generate V1 code
            3) execute V1 → produce chart_v1.png
            4) reflect on V1 (image + original code) → feedback + refined code
            5) execute V2 → produce chart_v2.png
        - eg:
            - html code quality if outputing report and charts as html?
    - tool use
        - search the internet for the best analysis method for the specific use case
        - code exec
        - database access

    - planning
    - multiagent
        - for a data science agent use case, different roles like data analyst, BI, data engineer?



- decompose a task

    - what human usually do preliminary EDA:
    1. data agnostic:
        - Load data/sample safely
        - Data Overview - shape, columns, data types, memory, basic info
        - Data Quality Check - missing values, duplicates, inconsistencies
    2. depends on the data:
        - understand the data content
        - Clean and preprocess data 
            - fix data types, parse amounts, handle missing values, deduplication, 
            - Time column sanity (gaps, timezone, ordering).
            - Fix obvious quality issues;
        - candidate keys.
        - Descriptives for numeric/categorical; outliers.
        - Quick visuals; simple correlations/pivots (for agent or human?)
    3. prepare for further analysis
        - convert to Parquet.
        - Draft data dictionary + README of assumptions.
        - Plan/clarify next steps:
            - drop or keep highly null columns?
            - method of null filling or keep as is?
            - more data?
            - apply deeper cleaning?
            - further analysis

- custom xx agent?
    - andrew said in his work he ended up builting a few specialized custom research agents (legal docs for conflict legal copliance, healthcare, business product research, etc)
    - custom eda agent for industy/company/use case, etc

- degrees of automony
    - choose the degree of automony?
    - less autonomous:
        - All steps predetermined
        - All tool use hard coded
        - Autonomy is in text generation
        - eg:
            - preliminary EDA: 
            - read data/file, get column names, data quality, stats/summary
            - generate a data summary
    - Semi-autonomous
        - Agent can make some decisions, choose tools
        - All tools predefined
    - Highly autonomous
        - Agent makes many decisions autonomously
        - Can create new tools on the fly
        - eg:
            - second round of EDA
            - answer use questions

- eval
    - obj vs sub evals: 
        - obj evals: use code
            - data analysis results
        - sub evals: LLM as judge
            - grade with a rubic using a score of 1 or 0 for each aspect (LLM is not good at scoring 1-5, nor good at comparing A and B directly)
            - planning componnet?
    - e2e and component level evals
    - examine traces to perform error analysis
    - starting point: create a dataset of prompts and answers, with 10/15/more prompts, run each time the prompt is changed



### design choice
- simple EDA agent:
    - given a dataframe, write python code to profile the date and produce a human-readable report + chart bundle, using pandas and matplotlib libraries.

- preliminary eda always use python pandas, no matter the data source
    - load_data component for data sources, or
    - data reader subagent: write pandas code to read data based on file type 
    

### the agents
- EDA agent 
    - settings: use pandas, matplotlib, openai only.
    - user: tell me about the data and what are the interesting findings
    - architecture:
        1. read data
            - work on this later, simplify for now, already load data as a df
        2. data understanding
            - goal: understand the data, data agnostic, no change on df
            - input: df
            - output: data_overview.json
            - tasks: use tool to:
                - Data Overview: shape, columns, data types, memory, basic info
                - Data Quality Check: missing values, duplicates, inconsistencies
                - understand data: keys, etc
        3. data preproc
            - goal: prepare the data for analysis
            - input: df, data_overview.json
            - output: 
                - df_clean: with data cleaned, potentially more columns
                - updated data_overview.json
            - tasks: choose and/or write tool to:
                - fix data types, parse amounts, handle missing values, deduplication, 
                - Time column sanity (gaps, timezone, ordering).
                - Fix obvious quality issues;
        
        4. EDA
            - goal: analyze the data to find insights
            - input: df_clean, data_overview.json
            - output: 
                - plots (if appliable)
                - df_stats (if appliable)
                - updated data_overview.json
            - tasks: choose and/or write tool to:

        5. repeat:
            potentially repeat step 3 and 4
        6. synthesis
            - goal: present the insights, with a summary of the process, suggest next step

### product feature
- UI:
    - conversion tab
    - data overview tab: 
        - table/file/source, column name, meaning, stats, issues and process method
        - user can correct
        - updated as continuous analysis and understanding
    - analysis report tab
    - code/notebook tab
        - for inspect and reproduce
        - default on python, can choose R, SQL, etc.
            - because large group of medicine analyst using R
    - how to arrange these tabs?
        - different "modes": chat mode, notebook mode,
