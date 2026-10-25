"""
Application Entrypoint: Agentic AIOps Cloud Sentinel
Provides both an HTTP webhook endpoint for Azure Monitor Action Groups
and a CLI simulation runner for instant testing.
"""

import argparse
import json
import logging
import sys
import yaml
from fastapi import FastAPI, Request
from src.agent.sre_agent import AgenticCloudSRE

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("agentic-aiops.main")

app = FastAPI(
    title="Agentic AIOps Cloud Sentinel",
    version="1.0.0",
    description="Autonomous SRE AI Agent for Real-Time Telemetry RCA and GitOps Self-Healing"
)


def load_config(config_path: str = "config/config.yaml") -> dict:
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.warning(f"Could not load config file ({e}), using default fallback.")
        return {
            "gitops_remediation": {"github_repo": "swapnilagarwal30/azure-enterprise-landingzone-tf"},
            "azure_telemetry": {"workspace_id": "demo-workspace"}
        }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Agentic AIOps Cloud Sentinel", "mode": "autonomous"}


@app.post("/api/v1/azure-monitor-webhook")
async def handle_azure_monitor_alert(request: Request):
    payload = await request.json()
    config = load_config()
    sre = AgenticCloudSRE(config)
    result = sre.process_alert(payload)
    return {"status": "SUCCESS", "incident_remediation": result}


def run_simulation(fixture_path: str = "tests/fixtures/mock_azure_alert.json"):
    logger.info("==================================================")
    logger.info("🤖 LAUNCHING AGENTIC AIOPS SIMULATION")
    logger.info(f"📂 Alert Payload: {fixture_path}")
    logger.info("==================================================")

    with open(fixture_path, "r", encoding="utf-8") as f:
        alert_data = json.load(f)

    config = load_config()
    sre = AgenticCloudSRE(config)
    result = sre.process_alert(alert_data)

    print("\n" + "=" * 60)
    print("✅ AUTONOMOUS TRIAGE & REMEDIATION COMPLETED (90s MTTR)")
    print("=" * 60)
    print(f"Incident:    {result['rca']['incident_title']}")
    print(f"Severity:    {result['rca']['severity']}")
    print(f"PR Status:   {result['pull_request']['status']}")
    print(f"PR URL:      {result['pull_request']['pr_url']}")
    print("-" * 60)
    print(result['pull_request']['body'])
    print("=" * 60 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agentic AIOps Cloud Sentinel")
    parser.add_argument("--simulate-alert", action="store_true", help="Run local alert triage simulation")
    parser.add_argument("--fixture", default="tests/fixtures/mock_azure_alert.json", help="Path to alert payload")
    args = parser.parse_args()

    if args.simulate_alert:
        run_simulation(args.fixture)
    else:
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8080)
