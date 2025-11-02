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
    - preliminary EDA:
        1. Load sample safely (encoding/delimiter/NA values).
        2. Shape, dtypes, memory, date parsing.
        3. Missingness map; duplicates; candidate keys.
        4. Descriptives for numeric/categorical; outliers.
        5. Target presence, balance, and leakage scan.
        6. Time column sanity (gaps, timezone, ordering).
        7. Quick visuals; simple correlations/pivots.
        8. Fix obvious quality issues; convert to Parquet.
        9. Draft data dictionary + README of assumptions.
        10. Plan/clarify next steps:
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
- preliminary eda always use python pandas, no matter the data source
    - load_data component for data sources
    


