"""Unit tests for agents"""

import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_planner_agent():
    from backend.agents.planner import plan
    
    with patch('backend.core.router.router.call_primary_llm') as mock_qwen:
        mock_qwen.return_value = '[{"step_number":1,"description":"Setup"}]'
        
        result = await plan("Build an app")
        
        assert result is not None
        assert isinstance(result, list)

@pytest.mark.asyncio
async def test_architect_agent():
    from backend.agents.architect import design_system
    
    with patch('backend.core.router.router.call_primary_llm') as mock_qwen:
        mock_qwen.return_value = '{"project_name":"test","folder_structure":{}}'
        
        result = await design_system("Test system")
        
        assert result is not None
        assert "project_name" in result

@pytest.mark.asyncio
async def test_coder_agent():
    from backend.agents.coder import build_code
    
    architecture = {
        "project_name": "test",
        "folder_structure": {"app.py": "main file"}
    }
    
    with patch('backend.core.router.router.call_coder_llm') as mock_ds:
        mock_ds.return_value = "print('Hello')"
        
        result = await build_code(architecture)
        
        assert result is not None
        assert "files" in result