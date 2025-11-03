## EDA agent
### design patterns
- understand the data and user question (if any), make an EDA plan, perform analysis and iterate if needed, present answers and insights
- multiagent, reflection, tool use, planning
- different degrees of automony for different subagent

### settings
- simple use case: user ask "tell me about the data?", or user gives the data without a question
- use sample data eleme.xlsx for dev, but the agent should be data agnostic.
- agent can only write python code using the following package (will add more when necessary):
    - pandas, matplotlib
- use openai model for now

### architecture&flow:
1. data_loader_agent
    - simplify for now, already load data as a df; work on this later
2. data_overview_agent
    - goal: provide an overview of the data; data agnostic; no change on df
    - input: df
    - output: data_overview.json
    - tasks: use tool to:
        - Data Overview: shape, columns, data types, memory, basic info
        - Data Quality Check: missing values, duplicates, inconsistencies
        - understand data: keys, etc
3. eda_planning_agent
    - goal: given data overview and user question, make a plan for subagents
4. data_preproc_agent
    - goal: prepare the data for analysis
    - input: df, data_overview.json
    - output: 
        - df_clean: with data cleaned, potentially more columns
        - updated data_overview.json
    - tasks: choose and/or write tool to:
        - fix data types, parse amounts, handle missing values, deduplication, 
        - Time column sanity (gaps, timezone, ordering).
        - Fix obvious quality issues;

5. analyst_agent
    - goal: analyze the data to find insights
    - input: df_clean, data_overview.json
    - output: 
        - plots (if appliable)
        - df_stats (if appliable)
        - updated data_overview.json
    - tasks: choose and/or write tool to:

6. report_agent:
    - goal: present the insights, with a summary of the process, suggest next step



