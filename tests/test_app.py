"""
Comprehensive Automated Test Suite for Capstone 57
Tests: Database operations, score calculation, evaluation forms, report generation, CSV/Excel export, quiz scoring, input validation.
Author / Student: Reshma Anandhan
"""
import unittest
import os
import io
import json
import sqlite3
import pandas as pd
from app import create_app
from config import Config
from database import get_db_connection, calculate_weighted_score, init_db
from models import ToolModel, TestCaseModel, EvaluationModel, QuizModel, ChecklistModel, BeforeAfterModel

class TestCapstone57(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configure app for testing with an in-memory or dedicated test database
        cls.test_db_path = os.path.join(os.path.dirname(__file__), "test_multimodal.db")
        
        class TestConfig(Config):
            TESTING = True
            DATABASE_PATH = cls.test_db_path
            SECRET_KEY = "test-secret-key"
            
        cls.app = create_app(TestConfig)
        cls.client = cls.app.test_client()
        
        # Initialize test DB
        with cls.app.app_context():
            init_db(force_reseed=True)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_db_path):
            try:
                os.remove(cls.test_db_path)
            except Exception:
                pass

    # 1. Database Operations & Seeds
    def test_database_tables_and_seeds(self):
        """Verifies that all 7 tables exist and are properly populated."""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        tables = ['tools', 'test_cases', 'evaluations', 'before_after_records', 'quiz_questions', 'checklist_audits', 'prompt_library']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            self.assertGreater(count, 0, f"Table {table} should not be empty")
            
        cursor.execute("SELECT COUNT(*) FROM tools")
        self.assertEqual(cursor.fetchone()[0], 4, "Should have exactly 4 AI tools")
        
        cursor.execute("SELECT COUNT(*) FROM test_cases")
        self.assertEqual(cursor.fetchone()[0], 15, "Should have exactly 15 test cases (5 per modality)")
        
        conn.close()

    # 2. Score Calculation Tests
    def test_weighted_score_calculation(self):
        """Validates the 40/25/20/15 weighted score calculation formula."""
        # 100 across all
        score_100 = calculate_weighted_score(100, 100, 100, 100)
        self.assertEqual(score_100, 100.0)
        
        # 0 across all
        score_0 = calculate_weighted_score(0, 0, 0, 0)
        self.assertEqual(score_0, 0.0)
        
        # Test exact weights: Acc=100 (40), Comp=0, Rel=0, Ease=0 -> 40.0
        acc_only = calculate_weighted_score(100, 0, 0, 0)
        self.assertEqual(acc_only, 40.0)
        
        # Test exact weights: Comp=100 (25) -> 25.0
        comp_only = calculate_weighted_score(0, 100, 0, 0)
        self.assertEqual(comp_only, 25.0)
        
        # Realistic student test case: Acc=90, Comp=80, Rel=85, Ease=70
        # (90 * 0.40) + (80 * 0.25) + (85 * 0.20) + (70 * 0.15) = 36 + 20 + 17 + 10.5 = 83.5
        realistic = calculate_weighted_score(90, 80, 85, 70)
        self.assertEqual(realistic, 83.5)

    # 3. Evaluation CRUD & Bounds Validation
    def test_evaluation_crud_operations(self):
        """Tests inserting, reading, updating, and deleting evaluation records."""
        with self.app.app_context():
            # Create
            eval_id = EvaluationModel.create(
                tool_id=1,
                test_case_id=1,
                evaluator_name="Reshma Anandhan",
                response_text="Test response snippet for unit testing.",
                accuracy=92,
                completeness=88,
                relevance=95,
                ease_of_use=90,
                hallucination_detected=False,
                hallucination_details="",
                unsafe_outdated_detected=False,
                unsafe_outdated_details="",
                student_notes="Unit test evaluation note",
                is_demo_data=0
            )
            self.assertIsNotNone(eval_id)
            
            # Read
            record = EvaluationModel.get_by_id(eval_id)
            self.assertIsNotNone(record)
            self.assertEqual(record['accuracy_score'], 92.0)
            self.assertEqual(record['evaluator_name'], "Reshma Anandhan")
            
            # Update
            EvaluationModel.update(
                eval_id=eval_id,
                accuracy=95,
                completeness=90,
                relevance=95,
                ease_of_use=90,
                response_text="Updated response text",
                hallucination_detected=True,
                hallucination_details="Subtle logic gate mislabel",
                unsafe_outdated_detected=False,
                unsafe_outdated_details="",
                student_notes="Updated note"
            )
            updated = EvaluationModel.get_by_id(eval_id)
            self.assertEqual(updated['accuracy_score'], 95.0)
            self.assertEqual(updated['hallucination_detected'], 1)
            
            # Delete
            EvaluationModel.delete(eval_id)
            deleted = EvaluationModel.get_by_id(eval_id)
            self.assertIsNone(deleted)

    # 4. Form Submission and Input Validation via HTTP
    def test_evaluation_form_validation(self):
        """Tests HTTP form validation for score boundaries (0 - 100)."""
        # Test out-of-bounds score (> 100)
        response_high = self.client.post('/evaluate/new', data={
            'tool_id': '1',
            'test_case_id': '1',
            'evaluator_name': 'Tester',
            'response_text': 'Valid text',
            'accuracy_score': '150', # Invalid!
            'completeness_score': '80',
            'relevance_score': '80',
            'ease_of_use_score': '80'
        }, follow_redirects=True)
        self.assertIn(b"must be between 0 and 100", response_high.data)

        # Test negative score (< 0)
        response_neg = self.client.post('/evaluate/new', data={
            'tool_id': '1',
            'test_case_id': '1',
            'evaluator_name': 'Tester',
            'response_text': 'Valid text',
            'accuracy_score': '-10', # Invalid!
            'completeness_score': '80',
            'relevance_score': '80',
            'ease_of_use_score': '80'
        }, follow_redirects=True)
        self.assertIn(b"must be between 0 and 100", response_neg.data)

    # 5. Quiz Grading Engine
    def test_quiz_grading(self):
        """Verifies quiz scoring logic, correct options, and pass threshold."""
        with self.app.app_context():
            questions = QuizModel.get_all()
            self.assertEqual(len(questions), 10, "Quiz must contain exactly 10 questions")
            
            # Create perfect answers dictionary
            perfect_answers = {str(q['id']): q['correct_option'] for q in questions}
            result_perfect = QuizModel.grade(perfect_answers)
            self.assertEqual(result_perfect['correct_answers'], 10)
            self.assertEqual(result_perfect['percentage'], 100.0)
            self.assertTrue(result_perfect['passed'])
            
            # Create all wrong answers
            wrong_answers = {str(q['id']): 'A' if q['correct_option'] != 'A' else 'B' for q in questions}
            result_wrong = QuizModel.grade(wrong_answers)
            self.assertFalse(result_wrong['passed'])
            self.assertLess(result_wrong['percentage'], 60.0)

    # 6. Checklist Risk & Reliability Calculation
    def test_checklist_audit_risk_scoring(self):
        """Validates checklist risk levels and reliability score computation."""
        with self.app.app_context():
            # Zero defects -> Low Risk, 100% Reliability
            audit_id1, risk1, rel1 = ChecklistModel.create(
                "TestTool", "TestTask", False, False, False, False, False, False, False, "Clean output"
            )
            self.assertEqual(risk1, "Low")
            self.assertEqual(rel1, 100.0)
            
            # 5 defects -> Critical Risk
            audit_id2, risk2, rel2 = ChecklistModel.create(
                "TestTool", "FlawedTask", True, True, True, True, True, False, False, "Severely flawed"
            )
            self.assertEqual(risk2, "Critical")
            self.assertLessEqual(rel2, 50.0)

    # 7. Exports: PDF, CSV, Excel
    def test_csv_export(self):
        """Verifies CSV export endpoint returns valid CSV with headers."""
        response = self.client.get('/report/export/csv')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/csv; charset=utf-8')
        csv_text = response.data.decode('utf-8')
        self.assertIn('accuracy_score', csv_text)
        self.assertIn('weighted_score', csv_text)

    def test_excel_export(self):
        """Verifies Excel (.xlsx) export endpoint produces readable Excel workbook."""
        response = self.client.get('/report/export/excel')
        self.assertEqual(response.status_code, 200)
        excel_bytes = io.BytesIO(response.data)
        excel_file = pd.ExcelFile(excel_bytes)
        self.assertIn('Evaluations', excel_file.sheet_names)
        self.assertIn('Tools_Summary', excel_file.sheet_names)

    def test_pdf_export(self):
        """Verifies ReportLab PDF generation generates valid binary PDF header."""
        response = self.client.get('/report/download/pdf')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')
        # Check PDF magic bytes '%PDF'
        self.assertTrue(response.data.startswith(b'%PDF'))
        self.assertGreater(len(response.data), 1000)

    # 8. Web Routes & UI View Endpoints
    def test_all_web_routes(self):
        """Verifies every navigation link and module returns HTTP 200 OK."""
        routes = [
            '/',
            '/dashboard',
            '/tools',
            '/tasks',
            '/evaluations',
            '/evaluate/new',
            '/comparison',
            '/report',
            '/checklist',
            '/quiz',
            '/automation',
            '/before-after',
            '/presentation',
            '/prompts',
            '/api/chart-data'
        ]
        for route in routes:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Route {route} failed with status {res.status_code}")

    # 9. Chart.js API Payload
    def test_api_chart_data(self):
        """Verifies Chart.js JSON API contains expected datasets and labels."""
        response = self.client.get('/api/chart-data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('tools', data)
        self.assertIn('weighted_scores', data)
        self.assertIn('modality_breakdown', data)
        self.assertIn('radar_datasets', data)
        self.assertEqual(len(data['tools']), 4)

if __name__ == '__main__':
    unittest.main()
