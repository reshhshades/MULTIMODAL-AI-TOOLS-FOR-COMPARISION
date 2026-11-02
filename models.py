"""
Data Models and Database Query Services for Capstone 57
Student: Reshma Anandhan
"""
from database import get_db_connection, calculate_weighted_score
from config import Config
import pandas as pd

class ToolModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        tools = conn.execute("SELECT * FROM tools ORDER BY id ASC").fetchall()
        conn.close()
        return [dict(t) for t in tools]

    @staticmethod
    def get_by_id(tool_id):
        conn = get_db_connection()
        tool = conn.execute("SELECT * FROM tools WHERE id = ?", (tool_id,)).fetchone()
        conn.close()
        return dict(tool) if tool else None

    @staticmethod
    def get_with_metrics():
        """Returns tools enriched with aggregated scores, ranking, and failure counts."""
        conn = get_db_connection()
        query = """
        SELECT 
            t.*,
            COUNT(e.id) as total_evaluations,
            ROUND(AVG(e.accuracy_score), 1) as avg_accuracy,
            ROUND(AVG(e.completeness_score), 1) as avg_completeness,
            ROUND(AVG(e.relevance_score), 1) as avg_relevance,
            ROUND(AVG(e.ease_of_use_score), 1) as avg_ease_of_use,
            ROUND(AVG(e.weighted_score), 1) as avg_weighted_score,
            SUM(e.hallucination_detected) as total_hallucinations,
            SUM(e.unsafe_outdated_detected) as total_unsafe_outdated
        FROM tools t
        LEFT JOIN evaluations e ON t.id = e.tool_id
        GROUP BY t.id
        ORDER BY avg_weighted_score DESC
        """
        tools = conn.execute(query).fetchall()
        conn.close()
        return [dict(t) for t in tools]

class TestCaseModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cases = conn.execute("SELECT * FROM test_cases ORDER BY id ASC").fetchall()
        conn.close()
        return [dict(c) for c in cases]

    @staticmethod
    def get_by_id(case_id):
        conn = get_db_connection()
        case = conn.execute("SELECT * FROM test_cases WHERE id = ?", (case_id,)).fetchone()
        conn.close()
        return dict(case) if case else None

    @staticmethod
    def get_by_modality(modality):
        conn = get_db_connection()
        cases = conn.execute("SELECT * FROM test_cases WHERE modality = ? ORDER BY id ASC", (modality.upper(),)).fetchall()
        conn.close()
        return [dict(c) for c in cases]

class EvaluationModel:
    @staticmethod
    def get_all(tool_id=None, modality=None, is_demo=None):
        conn = get_db_connection()
        query = """
        SELECT e.*, t.name as tool_name, t.badge_color as tool_badge,
               tc.case_code, tc.modality, tc.title as task_title, tc.difficulty
        FROM evaluations e
        JOIN tools t ON e.tool_id = t.id
        JOIN test_cases tc ON e.test_case_id = tc.id
        WHERE 1=1
        """
        params = []
        if tool_id:
            query += " AND e.tool_id = ?"
            params.append(tool_id)
        if modality:
            query += " AND tc.modality = ?"
            params.append(modality.upper())
        if is_demo is not None:
            query += " AND e.is_demo_data = ?"
            params.append(1 if is_demo else 0)
            
        query += " ORDER BY e.id DESC"
        evals = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(e) for e in evals]

    @staticmethod
    def get_by_id(eval_id):
        conn = get_db_connection()
        query = """
        SELECT e.*, t.name as tool_name, tc.case_code, tc.modality, tc.title as task_title
        FROM evaluations e
        JOIN tools t ON e.tool_id = t.id
        JOIN test_cases tc ON e.test_case_id = tc.id
        WHERE e.id = ?
        """
        evaluation = conn.execute(query, (eval_id,)).fetchone()
        conn.close()
        return dict(evaluation) if evaluation else None

    @staticmethod
    def create(tool_id, test_case_id, evaluator_name, response_text,
               accuracy, completeness, relevance, ease_of_use,
               hallucination_detected, hallucination_details,
               unsafe_outdated_detected, unsafe_outdated_details,
               student_notes, is_demo_data=0):
        
        weighted = calculate_weighted_score(accuracy, completeness, relevance, ease_of_use)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO evaluations 
        (tool_id, test_case_id, evaluator_name, response_text, accuracy_score, completeness_score, relevance_score, ease_of_use_score, weighted_score, hallucination_detected, hallucination_details, unsafe_outdated_detected, unsafe_outdated_details, student_notes, is_demo_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tool_id, test_case_id, evaluator_name, response_text,
            float(accuracy), float(completeness), float(relevance), float(ease_of_use),
            weighted,
            1 if hallucination_detected else 0, hallucination_details,
            1 if unsafe_outdated_detected else 0, unsafe_outdated_details,
            student_notes, is_demo_data
        ))
        eval_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return eval_id

    @staticmethod
    def update(eval_id, accuracy, completeness, relevance, ease_of_use,
               response_text, hallucination_detected, hallucination_details,
               unsafe_outdated_detected, unsafe_outdated_details, student_notes):
        
        weighted = calculate_weighted_score(accuracy, completeness, relevance, ease_of_use)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE evaluations SET
            accuracy_score = ?,
            completeness_score = ?,
            relevance_score = ?,
            ease_of_use_score = ?,
            weighted_score = ?,
            response_text = ?,
            hallucination_detected = ?,
            hallucination_details = ?,
            unsafe_outdated_detected = ?,
            unsafe_outdated_details = ?,
            student_notes = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """, (
            float(accuracy), float(completeness), float(relevance), float(ease_of_use),
            weighted, response_text,
            1 if hallucination_detected else 0, hallucination_details,
            1 if unsafe_outdated_detected else 0, unsafe_outdated_details,
            student_notes, eval_id
        ))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def delete(eval_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM evaluations WHERE id = ?", (eval_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_overall_summary():
        conn = get_db_connection()
        query = """
        SELECT 
            COUNT(DISTINCT tool_id) as total_tools,
            COUNT(DISTINCT test_case_id) as total_tasks_evaluated,
            COUNT(id) as total_evaluations,
            ROUND(AVG(accuracy_score), 1) as overall_avg_accuracy,
            ROUND(AVG(weighted_score), 1) as overall_avg_weighted,
            SUM(hallucination_detected) as total_hallucinations,
            SUM(unsafe_outdated_detected) as total_unsafe_outdated
        FROM evaluations
        """
        row = conn.execute(query).fetchone()
        
        # Best performing tool overall
        best_tool_row = conn.execute("""
        SELECT t.name, ROUND(AVG(e.weighted_score), 1) as score
        FROM evaluations e
        JOIN tools t ON e.tool_id = t.id
        GROUP BY t.id
        ORDER BY score DESC
        LIMIT 1
        """).fetchone()

        best_tool_name = best_tool_row['name'] if best_tool_row else "N/A"
        best_tool_score = best_tool_row['score'] if best_tool_row else 0.0

        conn.close()
        summary = dict(row) if row else {}
        summary['best_performing_tool'] = best_tool_name
        summary['best_performing_score'] = best_tool_score
        return summary

    @staticmethod
    def get_category_modality_matrix():
        """Returns accuracy and weighted score by tool and modality for chart visualization."""
        conn = get_db_connection()
        query = """
        SELECT 
            t.name as tool_name,
            tc.modality,
            ROUND(AVG(e.accuracy_score), 1) as avg_accuracy,
            ROUND(AVG(e.weighted_score), 1) as avg_weighted,
            ROUND(AVG(e.completeness_score), 1) as avg_completeness,
            ROUND(AVG(e.relevance_score), 1) as avg_relevance,
            ROUND(AVG(e.ease_of_use_score), 1) as avg_ease
        FROM evaluations e
        JOIN tools t ON e.tool_id = t.id
        JOIN test_cases tc ON e.test_case_id = tc.id
        GROUP BY t.id, tc.modality
        ORDER BY t.id, tc.modality
        """
        rows = conn.execute(query).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_best_per_modality():
        """Finds the best performing AI tool for IMAGE, DOCUMENT, and AUDIO."""
        conn = get_db_connection()
        modalities = ['IMAGE', 'DOCUMENT', 'AUDIO']
        best_map = {}
        for mod in modalities:
            row = conn.execute("""
            SELECT t.name, ROUND(AVG(e.weighted_score), 1) as score, ROUND(AVG(e.accuracy_score), 1) as acc
            FROM evaluations e
            JOIN tools t ON e.tool_id = t.id
            JOIN test_cases tc ON e.test_case_id = tc.id
            WHERE tc.modality = ?
            GROUP BY t.id
            ORDER BY score DESC
            LIMIT 1
            """, (mod,)).fetchone()
            if row:
                best_map[mod] = {
                    "tool": row['name'],
                    "score": row['score'],
                    "accuracy": row['acc']
                }
            else:
                best_map[mod] = {"tool": "N/A", "score": 0.0, "accuracy": 0.0}
        conn.close()
        return best_map

class BeforeAfterModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        query = """
        SELECT b.*, t.name as tool_name, tc.case_code, tc.title as task_title, tc.modality
        FROM before_after_records b
        JOIN tools t ON b.tool_id = t.id
        JOIN test_cases tc ON b.test_case_id = tc.id
        ORDER BY b.id ASC
        """
        records = conn.execute(query).fetchall()
        conn.close()
        return [dict(r) for r in records]

class QuizModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        questions = conn.execute("SELECT * FROM quiz_questions ORDER BY question_number ASC").fetchall()
        conn.close()
        return [dict(q) for q in questions]

    @staticmethod
    def grade(user_answers):
        """
        Grades user answers dictionary: {question_id: 'A'/'B'/'C'/'D'}.
        Returns detailed scoring results with explanations.
        """
        questions = QuizModel.get_all()
        correct_count = 0
        details = []
        for q in questions:
            qid_str = str(q['id'])
            user_opt = user_answers.get(qid_str, "").strip().upper()
            is_correct = (user_opt == q['correct_option'])
            if is_correct:
                correct_count += 1
            details.append({
                "id": q['id'],
                "number": q['question_number'],
                "question": q['question'],
                "options": {
                    "A": q['option_a'],
                    "B": q['option_b'],
                    "C": q['option_c'],
                    "D": q['option_d']
                },
                "user_selected": user_opt,
                "correct_option": q['correct_option'],
                "is_correct": is_correct,
                "explanation": q['explanation'],
                "category": q['category']
            })
        percentage = round((correct_count / len(questions)) * 100, 1) if questions else 0
        return {
            "total_questions": len(questions),
            "correct_answers": correct_count,
            "percentage": percentage,
            "passed": percentage >= 60.0,
            "details": details
        }

class ChecklistModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        audits = conn.execute("SELECT * FROM checklist_audits ORDER BY id DESC").fetchall()
        conn.close()
        return [dict(a) for a in audits]

    @staticmethod
    def create(tool_name, task_name, has_incorrect, has_missing, has_hallucinations,
               has_unsafe, has_outdated, has_source_issues, has_privacy_risks, notes=""):
        
        flags = [has_incorrect, has_missing, has_hallucinations, has_unsafe, has_outdated, has_source_issues, has_privacy_risks]
        issue_count = sum(1 for f in flags if f)
        
        # Calculate reliability score (100 - (issue_count * 14.28))
        reliability = max(0.0, round(100.0 - (issue_count * 14.28), 1))
        
        if issue_count == 0:
            risk = "Low"
        elif issue_count <= 2:
            risk = "Moderate"
        elif issue_count <= 4:
            risk = "High"
        else:
            risk = "Critical"
            
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO checklist_audits
        (tool_name, task_name, has_incorrect_info, has_missing_info, has_hallucinations, has_unsafe_advice, has_outdated_info, has_source_reliability_issues, has_privacy_risks, risk_level, reliability_score, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tool_name, task_name,
            1 if has_incorrect else 0,
            1 if has_missing else 0,
            1 if has_hallucinations else 0,
            1 if has_unsafe else 0,
            1 if has_outdated else 0,
            1 if has_source_issues else 0,
            1 if has_privacy_risks else 0,
            risk, reliability, notes
        ))
        conn.commit()
        audit_id = cursor.lastrowid
        conn.close()
        return audit_id, risk, reliability

class PromptLibraryModel:
    @staticmethod
    def get_all(category=None):
        conn = get_db_connection()
        if category:
            prompts = conn.execute("SELECT * FROM prompt_library WHERE category = ? ORDER BY id ASC", (category.upper(),)).fetchall()
        else:
            prompts = conn.execute("SELECT * FROM prompt_library ORDER BY id ASC").fetchall()
        conn.close()
        return [dict(p) for p in prompts]
