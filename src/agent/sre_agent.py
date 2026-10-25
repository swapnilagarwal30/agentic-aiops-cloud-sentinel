"""
Module: sre_agent.py
Purpose: Autonomous Multi-Agent SRE orchestrating alert triage, telemetry correlation,
         KQL diagnostics, root-cause analysis, and self-healing pull requests.
"""

from typing import Dict, Any
import logging
from src.analyzers.kql_analyzer import KQLTelemetryAnalyzer
from src.analyzers.git_analyzer import GitCommitCorrelator
from src.remediation.patch_synthesizer import PatchSynthesizer
from src.remediation.pr_creator import RemediationPRCreator

logger = logging.getLogger("agentic-aiops.agent")


class AgenticCloudSRE:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.kql = KQLTelemetryAnalyzer(config.get("azure_telemetry", {}).get("workspace_id", ""))
        self.git = GitCommitCorrelator(config.get("gitops_remediation", {}).get("github_repo", ""))
        self.pr = RemediationPRCreator(config.get("gitops_remediation", {}).get("github_repo", ""))

    def process_alert(self, alert_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes end-to-end autonomous triage, RCA, and self-healing workflow.
        """
        essentials = alert_payload.get("data", {}).get("essentials", {})
        alert_rule = essentials.get("alertRule", "Unknown Alert")
        severity = essentials.get("severity", "Sev2")
        target_id = essentials.get("alertTargetIDs", ["unknown-resource"])[0]

        logger.info(f"🚨 Ingested Alert: '{alert_rule}' [{severity}] on '{target_id}'")

        # Step 1: Telemetry Analysis via KQL
        telemetry = self.kql.query_resource_telemetry(target_id)

        # Step 2: Correlate with Git Commit History
        suspicious_commits = self.git.inspect_recent_deployments()

        # Step 3: Synthesize Root-Cause Analysis (RCA)
        rca = {
            "incident_title": f"Resolve {alert_rule}",
            "severity": severity,
            "target_resource": target_id,
            "root_cause_explanation": (
                f"**Root Cause:** Commit `{suspicious_commits[0]['commit_sha']}` by `{suspicious_commits[0]['author']}` "
                f"downscaled the compute SKU to `Standard_B2s`. Under current production load, CPU credits were exhausted, "
                f"leading to severe CPU saturation ({telemetry['metrics']['current_avg_utilization']}%) "
                f"and consecutive application memory exceptions.\n\n"
                f"**Resolution Strategy:** Automatically revert the VMSS SKU back to dedicated general-purpose "
                f"`{telemetry['recommended_sku_upgrade']}`."
            )
        }

        # Step 4: Synthesize Code Patch
        patch = PatchSynthesizer.generate_remediation_patch(rca)

        # Step 5: Open Automated Remediation PR
        pr_result = self.pr.open_remediation_pr(rca, patch)

        return {
            "incident_id": essentials.get("alertId", "mock-alert-123"),
            "status": "MITIGATED_PENDING_APPROVAL",
            "rca": rca,
            "patch": patch,
            "pull_request": pr_result
        }
