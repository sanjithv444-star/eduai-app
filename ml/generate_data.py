import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_samples=1000, save_path='data/student_data.csv'):
    np.random.seed(42)
    
    # Features
    attendance = np.random.uniform(50, 100, num_samples)
    assignments_completed = np.random.randint(0, 11, num_samples) # Max 10 assignments
    quiz_avg = np.random.uniform(30, 100, num_samples)
    prev_term = np.random.uniform(40, 100, num_samples)
    
    # Introduce some logical correlation to final marks
    # Final marks heavily dependent on all factors
    base_marks = (attendance * 0.3) + (assignments_completed * 10 * 0.2) + (quiz_avg * 0.2) + (prev_term * 0.3)
    
    # Add some noise
    noise = np.random.normal(0, 5, num_samples)
    final_marks = base_marks + noise
    
    # Clip between 0 and 100
    final_marks = np.clip(final_marks, 0, 100)
    
    # Categorize
    categories = []
    for mark in final_marks:
        if mark >= 80:
            categories.append('Excellent')
        elif mark >= 60:
            categories.append('Good')
        else:
            categories.append('Needs Improvement')
            
    # Create DataFrame
    df = pd.DataFrame({
        'attendance_percentage': attendance,
        'assignments_completed': assignments_completed,
        'quiz_average': quiz_avg,
        'previous_term_marks': prev_term,
        'final_exam_marks': final_marks,
        'performance_category': categories
    })
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Save to CSV
    df.to_csv(save_path, index=False)
    print(f"Synthetic data generated and saved to {save_path}")

if __name__ == '__main__':
    generate_synthetic_data()
