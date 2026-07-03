# WelvoxAgent Skill Development Guide

## What is a Skill?

A **skill** is a specialized AI capability that can be combined with other skills to solve complex problems. Skills are modular, reusable, and discoverable.

Each skill consists of:
1. **Metadata** - Name, description, category
2. **Input Schema** - What data it accepts
3. **Output Schema** - What data it returns
4. **Prompt Template** - Instructions for the LLM
5. **Tool Dependencies** - External integrations needed
6. **Permissions** - Access control

## Anatomy of a Skill

### Basic Structure

```python
# packages/skills/my_skill.py

from pydantic import BaseModel, Field
from typing import List, Optional

# 1. Define input schema
class MySkillInput(BaseModel):
    text: str = Field(..., description="Input text")
    language: str = Field(default="en", description="Language code")

# 2. Define output schema
class MySkillOutput(BaseModel):
    result: str = Field(..., description="Processed result")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score")

# 3. Define the skill
class MySkill:
    id = "my_skill"
    name = "My Skill"
    category = "custom"
    description = "Does something cool"
    
    # Prompt template for the LLM
    prompt_template = """
You are an expert at {task}.
Your goal is to {goal}.

Input: {input}

Provide your response in this format:
Result: <your result>
Confidence: <0-1>
"""
    
    input_schema = MySkillInput
    output_schema = MySkillOutput
    
    # Tools this skill can use
    required_tools = ["web_search", "code_execution"]
    
    # Permissions required
    permissions = ["read", "write", "execute"]
    
    async def execute(self, input_data: MySkillInput) -> MySkillOutput:
        """Execute the skill"""
        # Your implementation here
        return MySkillOutput(
            result="Processed result",
            confidence=0.95
        )
```

## Creating a New Skill - Step by Step

### 1. Define Your Skill's Purpose

Ask yourself:
- What specific task does this skill perform?
- What inputs does it need?
- What outputs does it produce?
- What tools or integrations does it require?
- Who should be able to use this skill?

Example:
- **Purpose**: Analyze customer support emails
- **Inputs**: Email text, customer info
- **Outputs**: Sentiment, category, suggested response
- **Tools**: Gmail, sentiment analysis API
- **Permissions**: read:email, write:email

### 2. Create the Schema Files

```python
# packages/skills/email_analyzer/schemas.py

from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class EmailAnalyzerInput(BaseModel):
    email_id: str
    sender: str
    subject: str
    body: str
    
class EmailAnalyzerOutput(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    priority: Literal["low", "medium", "high", "urgent"]
    category: str
    suggested_response: str
    confidence_score: float
```

### 3. Write the Prompt Template

```python
# packages/skills/email_analyzer/prompts.py

ANALYZE_EMAIL_PROMPT = """
You are an expert customer support analyst.

Analyze the following customer email and provide:
1. Overall sentiment (positive, negative, or neutral)
2. Priority level (low, medium, high, or urgent)
3. Issue category
4. A professional suggested response

EMAIL:
From: {sender}
Subject: {subject}
---
{body}
---

Provide your analysis in JSON format:
{{
  "sentiment": "...",
  "priority": "...",
  "category": "...",
  "suggested_response": "..."
}}
"""
```

### 4. Implement the Skill

```python
# packages/skills/email_analyzer/skill.py

import json
import logging
from typing import Optional

from llm.client import get_llm_client
from .schemas import EmailAnalyzerInput, EmailAnalyzerOutput
from .prompts import ANALYZE_EMAIL_PROMPT

logger = logging.getLogger(__name__)

class EmailAnalyzerSkill:
    id = "email_analyzer"
    name = "Email Analyzer"
    description = "Analyzes customer emails for sentiment, priority, and category"
    category = "communication"
    enabled = True
    
    input_schema = EmailAnalyzerInput
    output_schema = EmailAnalyzerOutput
    required_tools = ["gmail", "sentiment_api"]
    permissions = ["read:email", "write:email"]
    
    async def execute(self, input_data: EmailAnalyzerInput) -> EmailAnalyzerOutput:
        """Analyze an email"""
        try:
            # Get LLM client
            llm = get_llm_client()
            
            # Format prompt
            prompt = ANALYZE_EMAIL_PROMPT.format(
                sender=input_data.sender,
                subject=input_data.subject,
                body=input_data.body
            )
            
            # Call LLM
            response = await llm.generate(
                prompt=prompt,
                temperature=0.3,  # Deterministic for analysis
                max_tokens=500
            )
            
            # Parse response
            analysis = json.loads(response)
            
            # Validate
            output = EmailAnalyzerOutput(
                sentiment=analysis["sentiment"],
                priority=analysis["priority"],
                category=analysis["category"],
                suggested_response=analysis["suggested_response"],
                confidence_score=0.92
            )
            
            logger.info(f"Email {input_data.email_id} analyzed successfully")
            return output
            
        except Exception as e:
            logger.error(f"Error analyzing email: {e}")
            raise
    
    async def validate(self, input_data: EmailAnalyzerInput) -> bool:
        """Validate input before execution"""
        return len(input_data.body) > 10
    
    async def transform_output(self, output: EmailAnalyzerOutput) -> dict:
        """Transform output for external consumption"""
        return output.model_dump()
```

### 5. Register the Skill

```python
# packages/skills/__init__.py

from .email_analyzer.skill import EmailAnalyzerSkill
from .coding_assistant.skill import CodingAssistantSkill
from .research_agent.skill import ResearchAgentSkill

# Skill registry
AVAILABLE_SKILLS = [
    EmailAnalyzerSkill(),
    CodingAssistantSkill(),
    ResearchAgentSkill(),
    # ... more skills
]

def get_skill(skill_id: str):
    """Get skill by ID"""
    for skill in AVAILABLE_SKILLS:
        if skill.id == skill_id:
            return skill
    return None

def list_skills(category: Optional[str] = None):
    """List all skills, optionally filtered by category"""
    if category:
        return [s for s in AVAILABLE_SKILLS if s.category == category]
    return AVAILABLE_SKILLS
```

### 6. Write Tests

```python
# packages/skills/email_analyzer/test_skill.py

import pytest
from .skill import EmailAnalyzerSkill
from .schemas import EmailAnalyzerInput

@pytest.fixture
def skill():
    return EmailAnalyzerSkill()

@pytest.fixture
def sample_input():
    return EmailAnalyzerInput(
        email_id="email_123",
        sender="customer@example.com",
        subject="Issue with order",
        body="I've been waiting 2 weeks for my order and still haven't received it!"
    )

@pytest.mark.asyncio
async def test_analyze_email(skill, sample_input):
    output = await skill.execute(sample_input)
    
    assert output.sentiment in ["positive", "negative", "neutral"]
    assert output.priority in ["low", "medium", "high", "urgent"]
    assert output.priority == "high"  # This is urgent!
    assert len(output.suggested_response) > 0
    assert 0 <= output.confidence_score <= 1

@pytest.mark.asyncio
async def test_validate_input(skill):
    # Valid input
    valid = EmailAnalyzerInput(
        email_id="123",
        sender="test@example.com",
        subject="Test",
        body="This is a valid email body with sufficient length"
    )
    assert await skill.validate(valid) == True
    
    # Invalid input (too short)
    invalid = EmailAnalyzerInput(
        email_id="123",
        sender="test@example.com",
        subject="Test",
        body="short"
    )
    assert await skill.validate(invalid) == False

def test_transform_output(skill, sample_input):
    output = EmailAnalyzerOutput(
        sentiment="negative",
        priority="high",
        category="logistics",
        suggested_response="We apologize...",
        confidence_score=0.95
    )
    transformed = skill.transform_output(output)
    
    assert isinstance(transformed, dict)
    assert "sentiment" in transformed
```

## Default Skills Reference

### 1. Universal Assistant
**Category**: Core  
**Purpose**: General-purpose AI conversation  
**Inputs**: Text message  
**Outputs**: Text response  
**Tools**: None

### 2. Coding Assistant
**Category**: Development  
**Purpose**: Code generation, debugging, refactoring  
**Inputs**: Description, language, context  
**Outputs**: Code, explanation  
**Tools**: GitHub, Stack Overflow API

### 3. Research Agent
**Category**: Research  
**Purpose**: Deep research on any topic  
**Inputs**: Query, depth level  
**Outputs**: Summary, sources, findings  
**Tools**: Web search, academic APIs

### 4. File Analyzer
**Category**: Productivity  
**Purpose**: Analyze documents, code, data  
**Inputs**: File content  
**Outputs**: Summary, insights, recommendations  
**Tools**: None

### 5. Content Creator
**Category**: Marketing  
**Purpose**: Create blog posts, social content, emails  
**Inputs**: Topic, style, target audience  
**Outputs**: Content, variations, hashtags  
**Tools**: None

### 6. Data Analyst
**Category**: Analytics  
**Purpose**: Analyze data and create visualizations  
**Inputs**: Data, analysis type  
**Outputs**: Insights, charts, recommendations  
**Tools**: Python execution, charting APIs

## Advanced Patterns

### Chaining Skills

```python
class ComplexWorkflow:
    async def execute(self, user_request: str):
        # Step 1: Research skill gathers information
        research_skill = get_skill("research_agent")
        research_output = await research_skill.execute(
            ResearchInput(query=user_request)
        )
        
        # Step 2: Content creator makes content
        content_skill = get_skill("content_creator")
        content = await content_skill.execute(
            ContentInput(
                topic=user_request,
                background=research_output.summary
            )
        )
        
        # Step 3: Social media skill creates variations
        social_skill = get_skill("social_media_manager")
        variations = await social_skill.execute(
            SocialInput(content=content.text)
        )
        
        return {
            "research": research_output,
            "content": content,
            "social_variations": variations
        }
```

### Using Tool Integrations

```python
class GitHubIssueCreatorSkill:
    required_tools = ["github"]
    
    async def execute(self, input_data):
        # Get tool
        github_tool = get_tool("github")
        
        # Use tool to authenticate
        user_repos = await github_tool.call(
            action="list_repos",
            parameters={"username": input_data.github_username}
        )
        
        # Create issue
        issue = await github_tool.call(
            action="create_issue",
            parameters={
                "repo": input_data.repo_name,
                "title": input_data.title,
                "body": input_data.description
            }
        )
        
        return IssueOutput(issue_url=issue.html_url)
```

### Memory Integration

```python
class LearnFromFeedbackSkill:
    async def execute(self, input_data):
        # Get memory manager
        memory = get_memory_manager()
        
        # Store feedback in semantic memory
        await memory.store_semantic(
            entity_type="skill_feedback",
            entity_name=f"feedback_{input_data.id}",
            relationships={
                "improves_skill": input_data.skill_id,
                "from_user": input_data.user_id,
                "sentiment": input_data.sentiment
            }
        )
        
        # Search related feedback
        similar = await memory.search(
            query=f"feedback about {input_data.skill_id}",
            limit=5
        )
        
        return FeedbackOutput(
            stored=True,
            similar_feedback=similar
        )
```

## Testing Skills

### Unit Tests

```bash
pytest packages/skills/my_skill/test_skill.py -v
```

### Integration Tests

```bash
pytest packages/skills/test_integration.py -v
```

### Performance Tests

```bash
pytest packages/skills/test_performance.py --benchmark
```

## Publishing a Skill

1. Ensure all tests pass
2. Document input/output schemas
3. Add examples
4. Submit PR to repository
5. Community review
6. Merge and publish

## Skill Best Practices

✅ **Do:**
- Keep skills focused and single-purpose
- Use clear, descriptive names
- Validate all inputs
- Handle errors gracefully
- Write comprehensive tests
- Document with examples
- Use type hints

❌ **Don't:**
- Create god skills that do everything
- Skip input validation
- Ignore error cases
- Write untested code
- Hardcode credentials
- Create dependencies between skills
- Assume specific LLM behavior

## Skill Performance Tips

1. **Caching**: Cache LLM responses for common queries
2. **Streaming**: Use streaming for long responses
3. **Parallel**: Execute independent steps in parallel
4. **Optimization**: Use smaller models for simple tasks
5. **Monitoring**: Track execution time and errors

## Troubleshooting

### Skill not being called

- Check if skill is registered
- Verify skill ID matches
- Check required tools are configured
- Ensure user has permissions

### Poor output quality

- Improve prompt template
- Add examples to prompt
- Adjust temperature/tokens
- Use different model
- Add validation and retry logic

### Performance issues

- Profile skill execution
- Add caching
- Reduce model context
- Use async operations
- Optimize database queries

---

**Happy skill building! 🚀**
