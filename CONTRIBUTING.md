# Contributing to WelvoxAgent

Welcome! We're excited that you want to contribute to WelvoxAgent. This guide will help you get started.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Getting Started

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/welvox-agent.git
cd welvox-agent
git remote add upstream https://github.com/welvox-ai/welvox-agent.git
```

### 2. Create a Branch
```bash
git checkout -b feature/amazing-feature
```

### 3. Set Up Development Environment
```bash
pnpm install
cp .env.example .env.local

# Start dev environment
docker-compose up -d
pnpm dev
```

## Development Workflow

### Before Making Changes

1. **Sync with upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Check existing issues**
   - Look for [good first issues](https://github.com/welvox-ai/welvox-agent/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
   - Comment that you're working on it

3. **Start a discussion (for major features)**
   - Create a GitHub Discussion
   - Get feedback before implementing

### Making Changes

#### Code Style
- Use TypeScript with strict mode
- Follow ESLint rules: `pnpm lint`
- Format with Prettier: `pnpm format`
- Write meaningful variable names
- Add comments for complex logic only

#### Commit Messages
Format: `type(scope): description`

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style (formatting, missing semicolons, etc.)
- `refactor` - Code refactoring
- `perf` - Performance improvement
- `test` - Adding or updating tests
- `chore` - Build process, dependencies, etc.

Examples:
```
feat(agents): add intent detection with Claude
fix(memory): resolve vector similarity threshold bug
docs(api): add endpoint documentation
```

#### Testing

Write tests for your changes:

```bash
# Run all tests
pnpm test

# Run tests in watch mode
pnpm test --watch

# Run tests with coverage
pnpm test --coverage
```

Example test:
```typescript
import { describe, it, expect } from 'vitest';
import { detectIntent } from '../src/orchestrator';

describe('Intent Detection', () => {
  it('should detect content creation intent', () => {
    const intent = detectIntent('Write a blog post');
    expect(intent).toBe('content_creation');
  });

  it('should detect coding intent', () => {
    const intent = detectIntent('Build me a React component');
    expect(intent).toBe('coding');
  });
});
```

#### Type Safety
Always maintain strict TypeScript:

```bash
pnpm type-check
```

#### Linting
```bash
pnpm lint
pnpm lint --fix  # Auto-fix issues
```

### Submitting Changes

#### 1. Push to Your Fork
```bash
git push origin feature/amazing-feature
```

#### 2. Create a Pull Request
- Use a clear, descriptive title
- Reference related issues: `Closes #123`
- Fill out the PR template
- Ensure all checks pass

#### 3. PR Template
```markdown
## Description
Brief description of changes

## Related Issues
Closes #123

## Changes Made
- Change 1
- Change 2

## Testing
How to test these changes

## Screenshots (if applicable)
Before/after screenshots

## Checklist
- [ ] Tests pass
- [ ] Types check
- [ ] Lint passes
- [ ] Documentation updated
- [ ] No breaking changes
```

#### 4. Review Process
- Address feedback promptly
- Keep discussion professional
- Request re-review after changes
- Two approvals required for merge

## File Structure Guidelines

### Adding a New Skill

1. Create the skill definition in `packages/skills/src/index.ts`
2. Add prompts in `packages/prompts/src/index.ts`
3. Add types to `packages/types/src/index.ts`
4. Add tests in `packages/skills/src/__tests__/`
5. Document in `docs/skills.md`

Example:
```typescript
// packages/skills/src/index.ts
export const MY_NEW_SKILL: Skill = {
  id: 'skill_my_new_skill',
  name: 'My New Skill',
  description: 'What this skill does',
  category: 'automation',
  icon: '⚡',
  version: '1.0.0',
  enabled: true,
  metadata: { /* ... */ },
  prompts: [ /* ... */ ],
  tools: [ /* ... */ ],
  permissions: [ /* ... */ ],
};
```

### Adding an API Endpoint

1. Create route file in `apps/api/routes/`
2. Add types to `packages/types/src/index.ts`
3. Register in `apps/api/main.py`
4. Document in `API_DOCUMENTATION.md`
5. Add tests

Example:
```python
# apps/api/routes/my_feature.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/my-feature", tags=["my-feature"])

@router.get("/")
async def get_my_feature():
    """Get my feature"""
    return {
        "success": True,
        "data": {...}
    }
```

### Adding a React Component

1. Create component in `packages/ui/src/`
2. Export from `packages/ui/src/index.tsx`
3. Add PropTypes/TypeScript types
4. Create Storybook story
5. Document usage
6. Add tests

Example:
```typescript
// packages/ui/src/MyComponent.tsx
import React from 'react';

export interface MyComponentProps {
  title: string;
  onClose?: () => void;
}

export const MyComponent: React.FC<MyComponentProps> = ({
  title,
  onClose,
}) => {
  return (
    <div>
      <h2>{title}</h2>
      {onClose && <button onClick={onClose}>Close</button>}
    </div>
  );
};
```

## Documentation

### Update Documentation When:
- Adding a new feature
- Changing API behavior
- Adding/removing dependencies
- Changing configuration options

### Documentation Locations:
- **Architecture**: `ARCHITECTURE.md`
- **API**: `API_DOCUMENTATION.md`
- **Setup**: `GETTING_STARTED.md`
- **Deployment**: `DEPLOYMENT.md`
- **Contributing**: `CONTRIBUTING.md`

### Writing Good Documentation
- Use clear, concise language
- Include code examples
- Add diagrams when helpful
- Keep documentation up-to-date
- Link to related sections

## Common Tasks

### Adding a Package Dependency
```bash
# Add to specific package
cd packages/agents
pnpm add lodash

# Add to root
cd ..
pnpm add -w -D typescript
```

### Publishing a New Version
```bash
# Update version
pnpm version minor

# Build
pnpm build

# Push
git push origin main
git push origin --tags
```

### Fixing TypeScript Errors
```bash
# Check errors
pnpm type-check

# Fix common issues
pnpm lint --fix
```

## Performance Optimization

When submitting performance improvements:

1. Include benchmark results
2. Show before/after metrics
3. Explain the optimization
4. Ensure no breaking changes

Example:
```markdown
## Performance Improvement
- **Before**: 500ms average response time
- **After**: 200ms average response time
- **Improvement**: 60% faster

**Optimization**: Implemented caching layer
```

## Security Considerations

When submitting security-related changes:

1. Don't disclose vulnerabilities publicly
2. Email security@welvox.ai instead
3. Include reproduction steps
4. Suggest a fix if possible

## Common Issues & Solutions

### Port Already in Use
```bash
lsof -i :8000
kill -9 <PID>
```

### Module Not Found
```bash
pnpm install
pnpm build
```

### Type Errors
```bash
pnpm type-check
# Fix errors, then rerun
```

### Import Issues
Check `tsconfig.json` paths:
```json
{
  "compilerOptions": {
    "paths": {
      "@welvox/*": ["packages/*/src"]
    }
  }
}
```

## Getting Help

- **Issues**: Ask in GitHub Issues
- **Discussions**: Use GitHub Discussions
- **Email**: dev@welvox.ai
- **Discord**: Join our [Discord server](https://discord.gg/welvox)

## Recognition

Contributors are recognized in:
- GitHub contributors page
- Release notes
- Contributors file

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Don't hesitate to ask! We're here to help.

---

## Development Tips

### Useful Commands
```bash
# Format code
pnpm format

# Check everything
pnpm type-check && pnpm lint

# Build everything
pnpm build

# Run tests
pnpm test

# Development mode
pnpm dev
```

### VSCode Extensions
- ESLint
- Prettier
- Thunder Client (for API testing)
- GitHub Copilot (optional)

### Debugging
```typescript
// Add console logs
console.log('Debug:', variable);

// Use debugger
debugger;

// Chrome DevTools
// Open chrome://inspect in Chrome
```

---

Thank you for contributing to WelvoxAgent! 🎉
