# Quiz Analyzer

The Quiz Analyzer is a Python based script designed to analyze quiz performance, detect weak areas, and generate recommendations for improvement. It works by processing data from quiz submissions, API endpoints, and quiz endpoints.

The script loads JSON data from three files, preprocesses it, and performs analysis based on various performance metrics like topic and difficulty. The script also provides insights into weak areas and generates learning recommendations.

## Features:
- Analyzes performance by topic and difficulty.
- Detects insights such as weak areas and performance gaps.
- Generates learning recommendations for targeted improvement.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/Jadhavsakshi7887/quiz-analyzer.git
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Place the following JSON data files in the project directory:
   - `QuizEndpoint.json`: Contains quiz endpoint data.
   - `APIendpoint.json`: Contains API endpoint data.
   - `QuizSubmissiondata.json`: Contains quiz submission data.

4. Run the script:
   ```bash
   python quiz_analyzer.py
   ```

## Approach

The script follows these steps:

1. **Load Data**: Loads JSON data from three input files (QuizEndpoint, APIEndpoint, QuizSubmissiondata).
2. **Preprocess Data**: Combines quiz data and historical responses to form a unified dataset.
3. **Performance Analysis**: Analyzes quiz performance based on topics, difficulty, and response accuracy.
4. **Insights Generation**: Detects weak areas and performance gaps based on analysis.
5. **Recommendations**: Generates actionable learning recommendations based on the detected insights.


