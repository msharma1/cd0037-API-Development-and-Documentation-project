import React, { Component } from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor(props) {
    super();
    this.state = {
      questions: [],
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
      page: 1,
    };
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`,
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions || [],
          totalQuestions: result.total_questions || 0,
          categories: result.categories || {},
          currentCategory: result.current_category || null,
        });
      },
      error: (error) => {
        console.error('Unable to load questions:', error);
      },
    });
  };

  selectPage = (num) => {
    this.setState({ page: num }, this.getQuestions);
  };

  createPagination = () => {
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10);
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => this.selectPage(i)}
        >
          {i}
        </span>
      );
    }
    return pageNumbers;
  };

  getByCategory = (id) => {
    $.ajax({
      url: `/categories/${id}/questions`,
      type: 'GET',
      success: (result) => {
        this.setState({
          questions: result.questions || [],
          totalQuestions: result.total_questions || 0,
          currentCategory: result.current_category || null,
        });
      },
      error: (error) => {
        console.error('Unable to load category questions:', error);
      },
    });
  };

  submitSearch = (searchTerm) => {
    if (!searchTerm || searchTerm.trim() === '') {
      alert('Please enter a valid search term.');
      return;
    }
  
    console.log('Searching for:', searchTerm); // Debugging log
  
    $.ajax({
      url: `/questions/search`,  // Ensure this matches the backend route
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ searchTerm: searchTerm.trim() }),
      success: (result) => {
        console.log('Search result:', result); // Debugging log
  
        if (!result.questions || result.questions.length === 0) {
          alert('No questions found for the given search term.');
        }
        this.setState({
          questions: result.questions || [],
          totalQuestions: result.total_questions || 0,
          currentCategory: result.current_category || null,
        });
      },
      error: (xhr, status, error) => {
        console.error('Search API request failed:', xhr.responseText);
        alert('Unable to load search results. Please try again.');
      },
    });
  };
  
  questionAction = (id) => (action) => {
    if (action === 'DELETE' && window.confirm('Are you sure you want to delete this question?')) {
      $.ajax({
        url: `/questions/${id}`,
        type: 'DELETE',
        success: () => this.getQuestions(),
        error: (error) => {
          console.error('Unable to delete question:', error);
        },
      });
    }
  };

  render() {
    return (
      <div className='question-view'>
        <div className='categories-list'>
          <h2 onClick={this.getQuestions}>Categories</h2>
          <ul>
            {this.state.categories &&
              Object.keys(this.state.categories).map((id) => (
                <li key={id} onClick={() => this.getByCategory(id)}>
                  {this.state.categories[id]}
                  <img
                    className='category'
                    alt={this.state.categories[id] ? this.state.categories[id].toLowerCase() : ''}
                    src={this.state.categories[id] ? `${this.state.categories[id].toLowerCase()}.svg` : ''}
                  />
                </li>
              ))}
          </ul>
          <Search submitSearch={this.submitSearch} />
        </div>
        <div className='questions-list'>
          <h2>Questions</h2>
          {this.state.questions.map((q) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category] || 'Unknown'}
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className='pagination-menu'>{this.createPagination()}</div>
        </div>
      </div>
    );
  }
}

export default QuestionView;
