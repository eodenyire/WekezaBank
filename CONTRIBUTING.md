# Contributing to Equity Bank Risk Management System

Thank you for your interest in contributing to the Equity Bank Risk Management System! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs
- Include detailed steps to reproduce the issue
- Provide system information (OS, Python version, etc.)
- Include relevant log files or error messages

### Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and its use case
- Explain how it would benefit the system
- Consider backward compatibility

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📋 Development Guidelines

### Code Style
- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Testing
- Write tests for all new functionality
- Ensure existing tests continue to pass
- Use the provided test framework: `python test_system.py`
- Test with sample data: `python test_data/generate_sample_data.py`

### Documentation
- Update README.md for significant changes
- Add docstrings to new functions and classes
- Update CHANGELOG.md for all changes
- Include examples for new features

### Commit Messages
- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Keep the first line under 50 characters
- Include more details in the body if needed

Example:
```
Add anomaly detection to risk scoring

- Implement Isolation Forest algorithm
- Add training data preparation
- Update risk calculation to include anomaly score
- Add tests for anomaly detection functionality
```

## 🏗️ Development Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Local Development
1. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/equity-risk-system.git
   cd equity-risk-system
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r risk_engine/requirements.txt
   ```

4. Run tests:
   ```bash
   python test_system.py --quick
   ```

5. Start development server:
   ```bash
   python start_system.py
   ```

## 🧪 Testing Guidelines

### Running Tests
```bash
# Quick tests
python test_system.py --quick

# Full test suite
python test_system.py

# Generate test data
python test_data/generate_sample_data.py --count 100
```

### Test Categories
- **Database Tests** - Connection and schema validation
- **Risk Scoring Tests** - Algorithm accuracy and edge cases
- **Integration Tests** - External system connections
- **Performance Tests** - Load and scalability testing
- **UI Tests** - Dashboard functionality

### Writing New Tests
- Add tests to `test_system.py`
- Follow existing test patterns
- Test both success and failure cases
- Include edge cases and boundary conditions

## 📁 Project Structure

```
equity-risk-system/
├── risk_engine/          # Core risk processing engine
│   ├── main.py          # Main application entry point
│   ├── risk_models.py   # Risk scoring algorithms
│   ├── database.py      # Database operations
│   ├── integrations.py  # External system integrations
│   └── config.py        # Configuration management
├── dashboard/           # Streamlit web interface
│   └── app.py          # Dashboard application
├── test_data/          # Sample data generation
│   └── generate_sample_data.py
├── docs/               # Documentation
├── infrastructure/     # Docker and deployment configs
└── tests/              # Test files
```

## 🔧 Configuration

### Environment Variables
Create `.env` file in `risk_engine/` directory:
```env
DB_NAME=risk_management.db
HIGH_RISK_THRESHOLD=0.8
MEDIUM_RISK_THRESHOLD=0.5
POLLING_INTERVAL_SECONDS=30
BATCH_SIZE=100
```

### Database Configuration
- Development: SQLite (default)
- Production: PostgreSQL (future)
- Test: In-memory SQLite

## 🚀 Release Process

### Version Numbering
- Follow Semantic Versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version number bumped
- [ ] Performance tested
- [ ] Security reviewed

## 🛡️ Security Guidelines

### Reporting Security Issues
- Do NOT open public issues for security vulnerabilities
- Email security issues to: [security-email]
- Include detailed description and reproduction steps
- Allow time for fix before public disclosure

### Security Best Practices
- Validate all input data
- Use parameterized SQL queries
- Implement proper error handling
- Log security-relevant events
- Follow principle of least privilege

## 📞 Getting Help

### Community Support
- GitHub Discussions for questions
- Issue tracker for bugs and features
- Documentation in `/docs` folder

### Development Questions
- Check existing issues and discussions
- Review documentation first
- Provide minimal reproducible examples
- Include relevant system information

## 📜 Code of Conduct

### Our Standards
- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional communication

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or inflammatory comments
- Personal attacks
- Publishing private information

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to the Equity Bank Risk Management System! 🎉