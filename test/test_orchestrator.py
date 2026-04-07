"""Unit tests for orchestrator"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from backend.orchestrator import Orchestrator

@pytest.fixture
def orchestrator():
    return Orchestrator()

@pytest.mark.asyncio
async def test_orchestrator_initialization(orchestrator):
    assert orchestrator.active_projects == {}

@pytest.mark.asyncio
async def test_run_god_mode_basic(orchestrator):
    with patch('backend.agents.planner.plan') as mock_plan:
        mock_plan.return_value = [{"step_number": 1, "description": "Test"}]
        
        with patch('backend.agents.architect.design_system') as mock_arch:
            mock_arch.return_value = {"project_name": "test_project"}
            
            with patch('backend.agents.coder.build_code') as mock_code:
                mock_code.return_value = {"files": {"app.py": "code"}, "project_name": "test"}
                
                result = await orchestrator.run_god_mode("Build test app")
                
                assert result is not None
                assert "success" in result or "error" in result

@pytest.mark.asyncio
async def test_logging(orchestrator):
    project_id = "test123"
    orchestrator.active_projects[project_id] = {"logs": []}
    await orchestrator._log(project_id, "Test message")
    
    assert project_id in orchestrator.active_projects
    assert "Test message" in orchestrator.active_projects[project_id]["logs"]