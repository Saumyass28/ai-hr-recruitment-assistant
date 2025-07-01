# ✅ backend/mcq_generator.py (COMPLETE AND FINAL)

import json
import random
from typing import List, Dict, Any

class MCQGenerator:
    def __init__(self):
        self.question_bank = self._initialize_question_bank()

    def _initialize_question_bank(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            'python': [
                {
                    'question': 'Which Python framework is commonly used for web development?',
                    'options': ['Django', 'NumPy', 'Pandas', 'Matplotlib'],
                    'correct': 0,
                    'difficulty': 'easy',
                    'explanation': 'Django is a high-level Python web framework that encourages rapid development.'
                },
                {
                    'question': 'What is the correct way to create a virtual environment in Python?',
                    'options': ['python -m venv myenv', 'python create venv', 'pip install venv', 'python venv create'],
                    'correct': 0,
                    'difficulty': 'medium',
                    'explanation': 'The venv module is the standard way to create virtual environments in Python 3.3+.'
                },
                {
                    'question': 'Which of the following is used for data manipulation in Python?',
                    'options': ['Flask', 'Django', 'Pandas', 'Requests'],
                    'correct': 2,
                    'difficulty': 'easy',
                    'explanation': 'Pandas is a powerful data manipulation and analysis library for Python.'
                },
                {
                    'question': 'What is a Python decorator?',
                    'options': ['A design pattern', 'A function that modifies another function', 'A data type', 'A loop construct'],
                    'correct': 1,
                    'difficulty': 'hard',
                    'explanation': 'Decorators are a way to modify or enhance functions without changing their code.'
                }
            ],
            'sql': [
                {
                    'question': 'Which SQL command is used to retrieve data from a database?',
                    'options': ['INSERT', 'UPDATE', 'SELECT', 'DELETE'],
                    'correct': 2,
                    'difficulty': 'easy',
                    'explanation': 'SELECT statement is used to query and retrieve data from database tables.'
                },
                {
                    'question': 'What does INNER JOIN do in SQL?',
                    'options': ['Combines all rows from both tables', 'Returns only matching rows from both tables', 'Returns all rows from left table', 'Deletes matching rows'],
                    'correct': 1,
                    'difficulty': 'medium',
                    'explanation': 'INNER JOIN returns only the rows that have matching values in both tables.'
                },
                {
                    'question': 'Which SQL clause is used to filter results?',
                    'options': ['ORDER BY', 'GROUP BY', 'WHERE', 'HAVING'],
                    'correct': 2,
                    'difficulty': 'easy',
                    'explanation': 'WHERE clause is used to filter records based on specified conditions.'
                },
                {
                    'question': 'What is database normalization?',
                    'options': ['Backing up data', 'Organizing data to reduce redundancy', 'Encrypting data', 'Indexing tables'],
                    'correct': 1,
                    'difficulty': 'hard',
                    'explanation': 'Normalization is the process of organizing data to minimize redundancy and dependency.'
                }
            ],
            'javascript': [
                {
                    'question': 'Which method is used to add an element to the end of an array in JavaScript?',
                    'options': ['push()', 'pop()', 'shift()', 'unshift()'],
                    'correct': 0,
                    'difficulty': 'easy',
                    'explanation': 'The push() method adds one or more elements to the end of an array.'
                },
                {
                    'question': 'What does "this" keyword refer to in JavaScript?',
                    'options': ['The current function', 'The global object', 'The calling object', 'The parent object'],
                    'correct': 2,
                    'difficulty': 'medium',
                    'explanation': 'The "this" keyword refers to the object that is calling the function.'
                },
                {
                    'question': 'What is a closure in JavaScript?',
                    'options': ['A loop construct', 'A function with access to outer scope', 'A data type', 'An error handler'],
                    'correct': 1,
                    'difficulty': 'hard',
                    'explanation': 'A closure gives you access to an outer function\'s scope from an inner function.'
                }
            ],
            'git': [
                {
                    'question': 'What is the purpose of "git clone" command?',
                    'options': ['Create a new branch', 'Copy a repository', 'Merge branches', 'Delete repository'],
                    'correct': 1,
                    'difficulty': 'easy',
                    'explanation': 'git clone creates a copy of a remote repository on your local machine.'
                },
                {
                    'question': 'Which command is used to stage changes in Git?',
                    'options': ['git commit', 'git push', 'git add', 'git pull'],
                    'correct': 2,
                    'difficulty': 'easy',
                    'explanation': 'git add stages changes for the next commit.'
                },
                {
                    'question': 'What does "git rebase" do?',
                    'options': ['Creates a backup', 'Rewrites commit history', 'Deletes branches', 'Merges conflicts'],
                    'correct': 1,
                    'difficulty': 'hard',
                    'explanation': 'git rebase moves or combines commits to create a cleaner project history.'
                }
            ],
            'docker': [
                {
                    'question': 'What is Docker primarily used for?',
                    'options': ['Version control', 'Containerization', 'Database management', 'Web hosting'],
                    'correct': 1,
                    'difficulty': 'easy',
                    'explanation': 'Docker is a platform for developing, shipping, and running applications in containers.'
                },
                {
                    'question': 'Which file is used to define Docker container configuration?',
                    'options': ['docker.json', 'Dockerfile', 'container.yml', 'docker.config'],
                    'correct': 1,
                    'difficulty': 'medium',
                    'explanation': 'Dockerfile contains instructions for building Docker images.'
                },
                {
                    'question': 'What is the difference between Docker image and container?',
                    'options': ['No difference', 'Image is running instance, container is template', 'Container is running instance, image is template', 'Both are the same thing'],
                    'correct': 2,
                    'difficulty': 'medium',
                    'explanation': 'An image is a template, while a container is a running instance of that image.'
                }
            ],
            'aws': [
                {
                    'question': 'What does EC2 stand for in AWS?',
                    'options': ['Elastic Compute Cloud', 'Enhanced Computing Center', 'Extended Cloud Computing', 'Elastic Container Cloud'],
                    'correct': 0,
                    'difficulty': 'easy',
                    'explanation': 'EC2 (Elastic Compute Cloud) provides scalable computing capacity in the cloud.'
                },
                {
                    'question': 'Which AWS service is used for object storage?',
                    'options': ['EC2', 'RDS', 'S3', 'Lambda'],
                    'correct': 2,
                    'difficulty': 'easy',
                    'explanation': 'S3 (Simple Storage Service) is AWS\'s object storage service.'
                },
                {
                    'question': 'What is AWS Lambda used for?',
                    'options': ['Database hosting', 'Serverless computing', 'Load balancing', 'DNS management'],
                    'correct': 1,
                    'difficulty': 'medium',
                    'explanation': 'AWS Lambda lets you run code without provisioning or managing servers.'
                }
            ],
            'react': [
                {
                    'question': 'What is JSX in React?',
                    'options': ['A database', 'JavaScript XML syntax extension', 'A testing framework', 'A state management tool'],
                    'correct': 1,
                    'difficulty': 'easy',
                    'explanation': 'JSX is a syntax extension for JavaScript that looks similar to XML/HTML.'
                },
                {
                    'question': 'What are React hooks?',
                    'options': ['Event handlers', 'Functions that let you use state in functional components', 'CSS classes', 'HTTP requests'],
                    'correct': 1,
                    'difficulty': 'medium',
                    'explanation': 'Hooks are functions that let you "hook into" React state and lifecycle features.'
                }
            ],
            'node.js': [
                {
                    'question': 'What is Node.js?',
                    'options': ['A database', 'JavaScript runtime built on Chrome\'s V8 engine', 'A web browser', 'A CSS framework'],
                    'correct': 1,
                    'difficulty': 'easy',
                    'explanation': 'Node.js is a JavaScript runtime that allows you to run JavaScript on the server side.'
                },
                {
                    'question': 'What is npm?',
                    'options': ['Node Package Manager', 'New Programming Method', 'Network Protocol Manager', 'Node Performance Monitor'],
                    'correct': 0,
                    'difficulty': 'easy',
                    'explanation': 'npm is the default package manager for Node.js.'
                }
            ],
            'general': [
                {
                    'question': 'What is the main advantage of using version control systems?',
                    'options': ['Faster code execution', 'Track changes and collaboration', 'Reduce file size', 'Automatic testing'],
                    'correct': 1,
                    'difficulty': 'easy',
                    'explanation': 'Version control systems help track changes, manage collaboration, and maintain code history.'
                },
                {
                    'question': 'Which software development methodology emphasizes iterative development?',
                    'options': ['Waterfall', 'Agile', 'Sequential', 'Linear'],
                    'correct': 1,
                    'difficulty': 'easy',
                    'explanation': 'Agile methodology focuses on iterative development and customer collaboration.'
                },
                {
                    'question': 'What does API stand for?',
                    'options': ['Application Programming Interface', 'Advanced Programming Integration', 'Automated Process Integration', 'Application Process Interface'],
                    'correct': 0,
                    'difficulty': 'easy',
                    'explanation': 'API defines how different software components should interact with each other.'
                },
                {
                    'question': 'What is the purpose of unit testing?',
                    'options': ['Test entire application', 'Test individual components', 'Test user interface', 'Test database connections'],
                    'correct': 1,
                    'difficulty': 'medium',
                    'explanation': 'Unit testing involves testing individual components or modules in isolation.'
                },
                {
                    'question': 'Which of the following is a NoSQL database?',
                    'options': ['MySQL', 'PostgreSQL', 'MongoDB', 'SQLite'],
                    'correct': 2,
                    'difficulty': 'easy',
                    'explanation': 'MongoDB is a document-based NoSQL database.'
                },
                {
                    'question': 'What is the difference between frontend and backend development?',
                    'options': ['No difference', 'Frontend is client-side, backend is server-side', 'Frontend is harder', 'Backend is visual'],
                    'correct': 1,
                    'difficulty': 'easy',
                    'explanation': 'Frontend deals with user interface, backend handles server-side logic and data.'
                }
            ]
        }

    def generate_mcqs(self, job_description: str, job_skills: List[str], num_questions: int = 10, difficulty: str = "medium") -> List[Dict[str, Any]]:
        """
        Generate MCQs based on job description and skills
        
        Args:
            job_description: The job description text (for context)
            job_skills: List of skills extracted from job description
            num_questions: Number of questions to generate (default: 10)
            difficulty: Difficulty level - "easy", "medium", or "hard" (default: "medium")
        
        Returns:
            List of MCQ dictionaries
        """
        if not job_skills:
            return self._get_general_questions(num_questions, difficulty)

        selected_questions = []
        question_id = 1

        # Normalize and shuffle skills
        normalized_skills = [skill.lower().strip() for skill in job_skills]
        shuffled_skills = normalized_skills.copy()
        random.shuffle(shuffled_skills)

        # First, try to get questions for each skill
        questions_per_skill = max(1, num_questions // len(set(normalized_skills)))
        
        for skill in shuffled_skills:
            if len(selected_questions) >= num_questions:
                break
                
            # Check for exact matches and partial matches
            skill_questions = []
            
            # Direct match
            if skill in self.question_bank:
                skill_questions = self.question_bank[skill].copy()
            else:
                # Partial matching for compound skills
                for bank_skill in self.question_bank.keys():
                    if bank_skill in skill or skill in bank_skill:
                        skill_questions.extend(self.question_bank[bank_skill].copy())
            
            if skill_questions:
                # Filter by difficulty if specified
                if difficulty.lower() != "medium":
                    skill_questions = [q for q in skill_questions if q.get('difficulty', 'medium').lower() == difficulty.lower()]
                
                # If no questions match difficulty, fall back to all questions
                if not skill_questions:
                    if skill in self.question_bank:
                        skill_questions = self.question_bank[skill].copy()
                
                random.shuffle(skill_questions)
                
                # Take questions for this skill
                for question in skill_questions[:questions_per_skill]:
                    if len(selected_questions) >= num_questions:
                        break
                    question_with_id = question.copy()
                    question_with_id['id'] = question_id
                    question_with_id['category'] = skill.title()
                    # Ensure correct_answer field matches expected format
                    question_with_id['correct_answer'] = question_with_id['correct'] + 1
                    selected_questions.append(question_with_id)
                    question_id += 1

        # Fill remaining slots with general questions
        if len(selected_questions) < num_questions:
            remaining_needed = num_questions - len(selected_questions)
            general_questions = self._get_general_questions(remaining_needed, difficulty, question_id)
            selected_questions.extend(general_questions)

        # Shuffle final questions
        random.shuffle(selected_questions)

        # Re-number questions after shuffle
        for i, question in enumerate(selected_questions, 1):
            question['id'] = i

        return selected_questions[:num_questions]

    def _get_general_questions(self, num_questions: int, difficulty: str = "medium", start_id: int = 1) -> List[Dict[str, Any]]:
        """Get general programming questions"""
        general_questions = self.question_bank['general'].copy()
        
        # Filter by difficulty if specified
        if difficulty.lower() != "medium":
            filtered = [q for q in general_questions if q.get('difficulty', 'medium').lower() == difficulty.lower()]
            if filtered:
                general_questions = filtered
        
        random.shuffle(general_questions)

        selected = []
        for i, question in enumerate(general_questions[:num_questions]):
            question_with_id = question.copy()
            question_with_id['id'] = start_id + i
            question_with_id['category'] = 'General Programming'
            # Ensure correct_answer field matches expected format
            question_with_id['correct_answer'] = question_with_id['correct'] + 1
            selected.append(question_with_id)

        return selected