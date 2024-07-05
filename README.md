# Lets_Build_Market_Analysis_Team_w_AI_Agents
Let's Build Market Analysis Team w/ AI Agents

## Introduction

This project demonstrates how AI enables one-person businesses, allowing anyone to become an entrepreneur or solopreneur. By leveraging AI tools, we can now handle complex tasks that previously required multiple experts. This README guides you through setting up and running an AI-powered real estate business that uses AI for property classification and management.

## What's This Project About?

This project is a practical implementation of a one-person startup powered entirely by AI. It includes:

1. A Streamlit-based frontend for a real estate management website
2. A Flask backend server that communicates with an AI model
3. AI-powered property classification for categorizing listings
4. A simple database system for storing property information

The project demonstrates how AI can automate tasks like property categorization, enabling efficient management of a real estate business by a single person.

## Why Use This Project?

- Learn how to integrate AI into a real-world business application
- Understand the potential of AI in streamlining business operations
- Gain insights into building scalable, AI-powered web applications
- Explore how tasks typically requiring teams can be handled efficiently by AI

## Architecture

The project consists of the following components:

1. Frontend: Streamlit Web Application
2. Backend: Flask Web Server with RESTful API
3. Services: LLM Service for property classification, Database Service for data management
4. External Components: Groq API for LLM model access
5. Data Storage: JSON file (company_db.json)

**Prerequisites:**
- Python installed on your system.
- A basic understanding of virtual environments and command-line tools.

**Steps:**
1. **Virtual Environment Setup:**
   - Create a dedicated virtual environment for our project:
   
     ```bash
     python -m venv Build_Market_Analysis_Team_w_AI_Agents
     ```
   - Activate the environment:
   
     - Windows:
       ```bash
       Build_Market_Analysis_Team_w_AI_Agents\Scripts\activate
       ```
     - Unix/macOS:
       ```bash
       source Build_Market_Analysis_Team_w_AI_Agents/bin/activate
       ```
2. **Install Project Dependencies:**

   - Navigate to your project directory and install required packages using `pip`:
   
     ```bash
     cd path/to/your/project
     pip install -r requirements.txt
     ```

3. **Setup Sqlite Database**
    - cd to <proj_root>/database
    - Open database
      ```sql
      sqlite3 housing.db
      ```
    - list all tables
    ```sql
       .tables
       .schema
    ```
    - execute few operations
     ```sql
       select * from housing;
   
      test load data
    curl -X POST -F "file=@C:\tmp\housing.csv" http://localhost:5000/process_client_onboard
    {
      "message": "Table 'customer' created successfully"
    }

     ```

4. **Setup Groq Key:**

   - Obtain your Groq API key from [Groq Console](https://console.groq.com/keys).
   - Set your key in the `.env` file as follows:
   
     ```plaintext
     GROQ_API_KEY=<YOUR_KEY>
     ```

5. **Run the Real Estate AI Application**

   Finally, execute the following command to start the Real Estate AI application:

   ```bash
   # Run Batch Job service
   python ~/PycharmProjects/Build_Market_Analysis_Team_w_AI_Agents/Batch_Job.py
   # Run UI
   streamlit run main.py  

