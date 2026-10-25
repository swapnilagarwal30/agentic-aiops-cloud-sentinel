import json
import pytest
from src.agent.sre_agent import AgenticCloudSRE


def test_agentic_sre_workflow():
    with open("tests/fixtures/mock_azure_alert.json", "r", encoding="utf-8") as f:
        alert = json.load(f)

    mock_config = {
        "azure_telemetry": {"workspace_id": "test-law"},
        "gitops_remediation": {"github_repo": "swapnilagarwal30/azure-enterprise-landingzone-tf"}
    }

    sre = AgenticCloudSRE(mock_config)
    result = sre.process_alert(alert)

    assert result["status"] == "MITIGATED_PENDING_APPROVAL"
    assert "Standard_B2s" in result["rca"]["root_cause_explanation"]
    assert "Standard_D4s_v5" in result["patch"]["remediated_code"]
    assert result["pull_request"]["pr_number"] == 42
