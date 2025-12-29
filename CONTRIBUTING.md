# Contributing to Wekeza Bank Analytics

Thank you for your interest in contributing to the Wekeza Bank Analytics Framework! This document provides guidelines for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow:
- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Accept responsibility for mistakes

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment
4. Create a new branch for your feature or bugfix

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/WekezaBank.git
cd WekezaBank

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Install the package in editable mode
pip install -e .
```

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Python version and OS
- Relevant logs or error messages

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- A clear and descriptive title
- A detailed description of the proposed functionality
- Examples of how the enhancement would be used
- Why this enhancement would be useful

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Easy issues suitable for beginners
- `help wanted` - Issues that need attention

## Coding Standards

### Python Style Guide

Follow PEP 8 style guide:

```bash
# Format code with black
black wekeza_analytics/

# Check with flake8
flake8 wekeza_analytics/

# Type checking with mypy
mypy wekeza_analytics/
```

### Code Structure

```python
"""
Module docstring describing the module's purpose.
"""

import standard_library
import third_party_library
from wekeza_analytics import local_module


class MyClass:
    """
    Class docstring.
    
    Attributes:
        attribute_name: Description
    """
    
    def __init__(self, param: str):
        """
        Initialize the class.
        
        Args:
            param: Description of parameter
        """
        self.attribute = param
    
    def method(self, arg: int) -> bool:
        """
        Method description.
        
        Args:
            arg: Description of argument
            
        Returns:
            Description of return value
            
        Raises:
            ValueError: Description of when this is raised
        """
        pass
```

### Naming Conventions

- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private methods/attributes: `_leading_underscore`

## Testing

All contributions should include tests:

```python
# tests/test_new_feature.py
import pytest
from wekeza_analytics.analytics import NewFeature


class TestNewFeature:
    """Test suite for NewFeature"""
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        feature = NewFeature()
        result = feature.process()
        assert result is not None
    
    def test_edge_case(self):
        """Test edge case"""
        feature = NewFeature()
        with pytest.raises(ValueError):
            feature.process(invalid_input=True)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=wekeza_analytics --cov-report=html

# Run specific test file
pytest tests/test_analytics.py

# Run with verbose output
pytest -v
```

### Test Coverage

Aim for at least 80% test coverage for new code:

```bash
pytest --cov=wekeza_analytics --cov-report=term-missing
```

## Documentation

### Docstrings

All public modules, classes, methods, and functions should have docstrings:

```python
def calculate_metric(data: pd.DataFrame, period: str = 'daily') -> dict:
    """
    Calculate metrics for the given data.
    
    This function calculates various metrics based on the input data
    and aggregates them by the specified period.
    
    Args:
        data: DataFrame with columns ['date', 'amount', 'customer_id']
        period: Aggregation period ('daily', 'weekly', 'monthly')
        
    Returns:
        Dictionary containing calculated metrics:
        - total: Total amount
        - average: Average amount
        - count: Number of records
        
    Raises:
        ValueError: If data is empty or period is invalid
        
    Example:
        >>> data = pd.DataFrame({'date': [...], 'amount': [...]})
        >>> metrics = calculate_metric(data, period='weekly')
        >>> print(metrics['total'])
        1000.0
    """
    pass
```

### README Updates

Update the README.md if your contribution:
- Adds new features
- Changes existing functionality
- Adds new dependencies
- Changes usage patterns

### API Documentation

Update `docs/API_REFERENCE.md` for:
- New public classes or methods
- Changed method signatures
- New parameters or return types

## Pull Request Process

1. **Create a Branch**
   ```bash
   git checkout -b feature/my-new-feature
   # or
   git checkout -b fix/issue-123
   ```

2. **Make Your Changes**
   - Write code following the coding standards
   - Add tests for your changes
   - Update documentation as needed

3. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```
   
   Use clear commit messages:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Refactor:` for code refactoring
   - `Docs:` for documentation changes
   - `Test:` for test additions/changes

4. **Push to Your Fork**
   ```bash
   git push origin feature/my-new-feature
   ```

5. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template
   - Link related issues

### Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows the project's coding standards
- [ ] All tests pass (`pytest`)
- [ ] Test coverage is maintained or improved
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] No unnecessary files are included
- [ ] Code is properly formatted (`black`, `flake8`)
- [ ] Type hints are included where appropriate

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Description of testing performed

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code follows style guidelines
- [ ] All tests pass

## Related Issues
Closes #123
```

## Review Process

1. A maintainer will review your PR
2. Address any requested changes
3. Once approved, a maintainer will merge your PR
4. Your contribution will be included in the next release

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

## Questions?

If you have questions:
- Open an issue with the `question` label
- Contact the maintainers
- Check existing documentation

Thank you for contributing to Wekeza Bank Analytics! 🎉
