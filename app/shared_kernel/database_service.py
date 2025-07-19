"""
Database Service Layer
File: app/shared_kernel/database_service.py
Purpose: Database operations for tech domains
"""

import sqlite3
from typing import List, Optional
from app.shared_kernel.db_models import TechDomainEntity, TechDomainQuestionEntity

class TechDomainDBService:
    def __init__(self, db_path: str = "./app_data/techcoach.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tech_domains table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tech_domains (
                name TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create tech_domain_questions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tech_domain_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain_name TEXT NOT NULL,
                question_text TEXT NOT NULL,
                user_answer TEXT,
                generated_answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (domain_name) REFERENCES tech_domains(name) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()
    
    def get_all_tech_domains(self) -> List[TechDomainEntity]:
        """Get all tech domains from database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, created_at, updated_at 
            FROM tech_domains 
            ORDER BY created_at ASC
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            TechDomainEntity(
                name=row["name"],
            )
            for row in rows
        ]
    
    def create_tech_domain(self, name: str) -> TechDomainEntity:
        """Create a new tech domain with name as primary key"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO tech_domains (name)
                VALUES (?)
            ''', (name,))
            conn.commit()
            
            # Fetch the newly created domain
            cursor.execute('SELECT name FROM tech_domains WHERE name = ?', (name,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return TechDomainEntity(
                    name=row["name"],
                )
            raise ValueError("Failed to create tech domain")
        except sqlite3.IntegrityError:
            conn.close()
            raise ValueError("Tech domain already exists")

    
    def delete_tech_domain(self, name: str) -> bool:
        """Delete a tech domain"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM tech_domains WHERE name = ?', (name,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected > 0


class TechDomainQuestionDBService:
    """Database service for tech domain questions"""

    def __init__(self, db_path: str = "./app_data/techcoach.db"):
        self.db_path = db_path
        # Note: Database initialization is handled by TechDomainDBService

    def create_question(
        self,
        domain_name: str,
        question_text: str,
        generated_answer: Optional[str] = None
    ) -> TechDomainQuestionEntity:
        """Create a new question for a tech domain"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO tech_domain_questions (domain_name, question_text, generated_answer)
                VALUES (?, ?, ?)
            ''', (domain_name, question_text, generated_answer))

            question_id = cursor.lastrowid
            conn.commit()

            # Fetch the newly created question
            cursor.execute('''
                SELECT id, domain_name, question_text, user_answer, generated_answer,
                       created_at, updated_at
                FROM tech_domain_questions
                WHERE id = ?
            ''', (question_id,))

            row = cursor.fetchone()
            conn.close()

            if row:
                return TechDomainQuestionEntity(
                    id=row["id"],
                    domain_name=row["domain_name"],
                    question_text=row["question_text"],
                    user_answer=row["user_answer"],
                    generated_answer=row["generated_answer"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"]
                )
            raise ValueError("Failed to create question")

        except sqlite3.Error as e:
            conn.close()
            raise ValueError(f"Database error: {str(e)}")

    def get_questions_by_domain(self, domain_name: str) -> List[TechDomainQuestionEntity]:
        """Get all questions for a specific tech domain"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, domain_name, question_text, user_answer, generated_answer,
                   created_at, updated_at
            FROM tech_domain_questions
            WHERE domain_name = ?
            ORDER BY created_at ASC
        ''', (domain_name,))

        rows = cursor.fetchall()
        conn.close()

        return [
            TechDomainQuestionEntity(
                id=row["id"],
                domain_name=row["domain_name"],
                question_text=row["question_text"],
                user_answer=row["user_answer"],
                generated_answer=row["generated_answer"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
            for row in rows
        ]

    def update_user_answer(self, question_id: int, user_answer: str) -> bool:
        """Update user answer for a specific question"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE tech_domain_questions SET user_answer = ? WHERE id = ?
            ''', (user_answer, question_id))

            affected = cursor.rowcount
            conn.commit()
            conn.close()

            return affected > 0

        except sqlite3.Error as e:
            conn.close()
            raise ValueError(f"Database error: {str(e)}")

    def update_generated_answer(self, question_id: int, generated_answer: str) -> bool:
        """Update generated answer for a specific question"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE tech_domain_questions SET generated_answer = ? WHERE id = ?
            ''', (generated_answer, question_id))

            affected = cursor.rowcount
            conn.commit()
            conn.close()

            return affected > 0

        except sqlite3.Error as e:
            conn.close()
            raise ValueError(f"Database error: {str(e)}")

    def get_question_by_id(self, question_id: int) -> Optional[TechDomainQuestionEntity]:
        """Get a specific question by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, domain_name, question_text, user_answer, generated_answer,
                   created_at, updated_at
            FROM tech_domain_questions
            WHERE id = ?
        ''', (question_id,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return TechDomainQuestionEntity(
                id=row["id"],
                domain_name=row["domain_name"],
                question_text=row["question_text"],
                user_answer=row["user_answer"],
                generated_answer=row["generated_answer"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
        return None

    def delete_question(self, question_id: int) -> bool:
        """Delete a specific question"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM tech_domain_questions WHERE id = ?', (question_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()

        return affected > 0

    def delete_questions_by_domain(self, domain_name: str) -> int:
        """Delete all questions for a specific domain"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM tech_domain_questions WHERE domain_name = ?', (domain_name,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()

        return affected