# Contributing to ResuMAX

Thanks for your interest in contributing! We welcome all contributions.

## Getting Started

1. **Fork the repo** on GitHub
2. **Clone your fork** locally
3. **Create a branch** for your feature: `git checkout -b feature/my-feature`
4. **Make changes** and test locally
5. **Commit** with clear messages: `git commit -m "Add feature X"`
6. **Push** to your fork: `git push origin feature/my-feature`
7. **Create Pull Request** on GitHub

## Development Setup

```bash
cd backend

# Install deps
pip install -r requirements.txt

# Run tests locally
./start_backend.sh  # Terminal 1
python desktop_gui.py  # Terminal 2
```

## Code Guidelines

### Python Style
- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions
- Keep functions under 50 lines

### Testing
- Test your changes with `desktop_gui.py`
- Try multiple resume formats
- Test edge cases (no skills section, etc)

### Commits
- Use present tense: "Add feature" not "Added feature"
- Be specific: "Fix PDF parsing for multi-column resumes"
- Reference issues: "Fix #42"

## What to Contribute

### High Priority
- 🐛 Bug fixes
- 📚 Documentation improvements
- ✨ New resume format support
- 🎨 Better industry detection

### Good First Issues
Look for issues tagged `good-first-issue` on GitHub

### Ideas
- Support more file formats (LinkedIn PDF export, etc)
- Add more industries (legal, education, retail)
- Improve parsing accuracy
- Create browser extension
- Add resume templates
- Multi-language support

## Code of Conduct

- Be respectful and constructive
- Help others learn
- Focus on what's best for the project
- No harassment or discrimination

## Questions?

- Open an issue on GitHub
- Start a discussion
- Reach out to maintainers

## License

By contributing, you agree your code will be licensed under the MIT License.

---