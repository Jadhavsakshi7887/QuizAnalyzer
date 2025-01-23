import json
import pandas as pd
import numpy as np

class QuizAnalyzer:
    def __init__(self, quiz_endpoint_path, api_endpoint_path, quiz_submission_path):
        self.quiz_endpoint_path = quiz_endpoint_path
        self.api_endpoint_path = api_endpoint_path
        self.quiz_submission_path = quiz_submission_path

    def load_json_data(self):
        try:
            with open(self.quiz_endpoint_path, 'r') as f:
                quiz_endpoint_data = json.load(f)
            with open(self.api_endpoint_path, 'r') as f:
                api_endpoint_data = json.load(f)
            with open(self.quiz_submission_path, 'r') as f:
                quiz_submission_data = json.load(f)

            return {
                'quiz_endpoint': quiz_endpoint_data,
                'api_endpoint': api_endpoint_data,
                'quiz_submission': quiz_submission_data
            }
        except Exception as e:
            raise ValueError(f"Data loading error: {e}")

    def preprocess_data(self, data):
      
        quiz_data = data['quiz_endpoint']
        api_data = data['api_endpoint']
        quiz_df = pd.DataFrame(quiz_data if isinstance(quiz_data, list) else [])

        historical_responses = []
        for quiz in api_data:
            response_map = quiz.get('response_map', {})
            for question_id, selected_option in response_map.items():
                historical_responses.append({
                    'quiz_id': quiz.get('quiz_id', 'unknown'),
                    'user_id': quiz.get('user_id', 'unknown'),
                    'question_id': question_id,
                    'selected_option': selected_option,
                    'topic': quiz.get('topics', ['Unknown'])[0],
                    'difficulty': quiz.get('difficulty', 'Medium'),
                    'score': quiz.get('score', 0)
                })

        historical_df = pd.DataFrame(historical_responses)
        return pd.concat([quiz_df, historical_df], ignore_index=True)

    def analyze_performance(self, df):
    
        topic_performance = df.groupby('topic')['score'].agg(['mean', 'count']).reset_index()

        difficulty_performance = df.groupby('difficulty')['score'].agg(['mean', 'count']).reset_index()

        accuracy_by_topic = df.groupby('topic').apply(
            lambda x: np.mean(x['selected_option'] == x.get('correct_option', None))
        ).reset_index(name='accuracy')

        return {
            'topic_performance': topic_performance,
            'difficulty_performance': difficulty_performance,
            'accuracy_by_topic': accuracy_by_topic
        }

    def detect_insights(self, performance):
        topic_performance = performance['topic_performance']
        accuracy_by_topic = performance['accuracy_by_topic']
        overall_mean = topic_performance['mean'].mean()
        weak_areas = topic_performance[topic_performance['mean'] < overall_mean]

        performance_gaps = accuracy_by_topic[accuracy_by_topic['accuracy'] < 0.5]

        return {
            'weak_areas': weak_areas,
            'improvement_trends': "Focus on topics with consistent low performance.",
            'performance_gaps': performance_gaps
        }

    def generate_recommendations(self, insights):
        """Create targeted learning recommendations"""
        weak_areas = insights['weak_areas']
        performance_gaps = insights['performance_gaps']

        recommendations = []
        if not weak_areas.empty:
            recommendations.append("Focus on the following weak topics:")
            for _, row in weak_areas.iterrows():
                recommendations.append(f"- {row['topic']} (Avg Score: {row['mean']:.2f})")

        if not performance_gaps.empty:
            recommendations.append("\nAddress performance gaps in these topics:")
            for _, row in performance_gaps.iterrows():
                recommendations.append(f"- {row['topic']} (Accuracy: {row['accuracy']:.2f})")

        recommendations.extend([
            "\nStudy Strategies:",
            "- Practice more questions in weak areas.",
            "- Review past incorrect answers.",
            "- Attempt quizzes with varied difficulty levels."
        ])

        return recommendations

    def run_analysis(self):
      
        data = self.load_json_data()
        combined_df = self.preprocess_data(data)
        performance = self.analyze_performance(combined_df)
        insights = self.detect_insights(performance)
        recommendations = self.generate_recommendations(insights)

        return {
            'performance': performance,
            'insights': insights,
            'recommendations': recommendations
        }

def main():
    QUIZ_ENDPOINT_PATH = "/content/QuizEndpoint.json"
    API_ENDPOINT_PATH = "/content/APIendpoint.json"
    QUIZ_SUBMISSION_PATH = "/content/QuizSubmissiondata.json"

    analyzer = QuizAnalyzer(
        QUIZ_ENDPOINT_PATH,
        API_ENDPOINT_PATH,
        QUIZ_SUBMISSION_PATH
    )

    try:
        results = analyzer.run_analysis()

        print("\nPerformance by Topic:")
        print(results['performance']['topic_performance'])

        print("\nPerformance by Difficulty:")
        print(results['performance']['difficulty_performance'])

        print("\nAccuracy by Topic:")
        print(results['performance']['accuracy_by_topic'])

        print("\nInsights:")
        for key, value in results['insights'].items():
            print(f"{key}: {value}")

        print("\nRecommendations:")
        for rec in results['recommendations']:
            print(rec)

    except Exception as e:
        print(f"Analysis Error: {e}")

if __name__ == "__main__":
    main()
