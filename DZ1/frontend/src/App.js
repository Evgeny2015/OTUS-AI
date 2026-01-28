import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch questions from backend
  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/v1/questions');
        setQuestions(response.data.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch questions');
        setLoading(false);
      }
    };

    fetchQuestions();
  }, []);

  // Handle answer changes
  const handleAnswerChange = (questionId, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Format answers for submission
    const formattedAnswers = Object.entries(answers).map(([questionId, answer]) => ({
      question_id: parseInt(questionId),
      answer: answer
    }));

    try {
      await axios.post('http://localhost:8000/api/v1/answers', {
        answers: formattedAnswers
      });
      setSubmitted(true);
    } catch (err) {
      setError('Failed to submit answers');
    }
  };

  // Render different question types
  const renderQuestion = (question) => {
    switch (question.type) {
      case 'text':
        return (
          <textarea
            value={answers[question.id] || ''}
            onChange={(e) => handleAnswerChange(question.id, e.target.value)}
            required
          />
        );
      case 'single_choice':
        return (
          <div className="options">
            {question.options.map((option, index) => (
              <label key={index}>
                <input
                  type="radio"
                  name={`question_${question.id}`}
                  value={option}
                  checked={answers[question.id] === option}
                  onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                  required
                />
                {option}
              </label>
            ))}
          </div>
        );
      case 'multiple_choice':
        return (
          <div className="options">
            {question.options.map((option, index) => (
              <label key={index}>
                <input
                  type="checkbox"
                  value={option}
                  checked={answers[question.id] && answers[question.id].includes(option)}
                  onChange={(e) => {
                    const currentAnswers = answers[question.id] || [];
                    if (e.target.checked) {
                      handleAnswerChange(question.id, [...currentAnswers, option]);
                    } else {
                      handleAnswerChange(question.id, currentAnswers.filter(a => a !== option));
                    }
                  }}
                />
                {option}
              </label>
            ))}
          </div>
        );
      default:
        return (
          <input
            type="text"
            value={answers[question.id] || ''}
            onChange={(e) => handleAnswerChange(question.id, e.target.value)}
            required
          />
        );
    }
  };

  if (loading) {
    return <div className="container"><div className="loading">Loading questions...</div></div>;
  }

  if (error) {
    return <div className="container"><div className="error">Error: {error}</div></div>;
  }

  if (submitted) {
    return (
      <div className="container">
        <div className="thank-you">
          <h2>Спасибо!</h2>
          <p>Ваши ответы были успешно отправлены.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <h1>Опрос</h1>
      <form onSubmit={handleSubmit}>
        {questions.map((question) => (
          <div key={question.id} className="question">
            <h3>{question.text}</h3>
            {renderQuestion(question)}
          </div>
        ))}
        <button type="submit">Отправить ответы</button>
      </form>
    </div>
  );
}

export default App;