import os
import joblib
import pandas as pd

class StudentPerformancePredictor:
    def __init__(self, model_dir='ml/models'):
        self.model_dir = model_dir
        self.regressor = None
        self.classifier = None
        self.load_models()
        
    def load_models(self):
        reg_path = os.path.join(self.model_dir, 'marks_predictor.pkl')
        clf_path = os.path.join(self.model_dir, 'category_predictor.pkl')
        
        if os.path.exists(reg_path) and os.path.exists(clf_path):
            self.regressor = joblib.load(reg_path)
            self.classifier = joblib.load(clf_path)
        else:
            print("Models not found. Please train models first.")
            
    def predict(self, attendance, assignments, quiz, prev_term):
        if not self.regressor or not self.classifier:
            # Fallback dummy predictions if models aren't trained yet
            dummy_mark = (attendance * 0.3) + (assignments * 10 * 0.2) + (quiz * 0.2) + (prev_term * 0.3)
            dummy_mark = min(100, max(0, dummy_mark))
            if dummy_mark >= 80:
                dummy_cat = 'Excellent'
            elif dummy_mark >= 60:
                dummy_cat = 'Good'
            else:
                dummy_cat = 'Needs Improvement'
            return dummy_mark, dummy_cat
            
        features = pd.DataFrame({
            'attendance_percentage': [attendance],
            'assignments_completed': [assignments],
            'quiz_average': [quiz],
            'previous_term_marks': [prev_term]
        })
        
        predicted_mark = self.regressor.predict(features)[0]
        predicted_category = self.classifier.predict(features)[0]
        
        return predicted_mark, predicted_category

    def get_recommendations(self, category, predicted_mark):
        if category == 'Excellent':
            return "Keep up the great work! Consider looking into advanced topics or helping peers."
        elif category == 'Good':
            return "You are doing well. Focus on areas where you lost marks in quizzes to push for Excellent."
        else:
            return "You need to focus on core concepts. Please review all fundamental materials and attend all classes."

predictor = StudentPerformancePredictor()
