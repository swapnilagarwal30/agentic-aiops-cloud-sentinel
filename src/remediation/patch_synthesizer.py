"""
Module: patch_synthesizer.py
Purpose: Generates unified code patches and self-healing IaC diffs based on RCA conclusions.
"""

from typing import Dict, Any


class PatchSynthesizer:
    @staticmethod
    def generate_remediation_patch(rca_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes a declarative git diff resolving the diagnosed incident.
        """
        target_file = "terraform.tfvars"
        original_content = 'vm_sku = "Standard_B2s"'
        remediated_content = 'vm_sku = "Standard_D4s_v5" # Self-healed: restored dedicated vCPU'

        diff = f"""--- a/{target_file}
+++ b/{target_file}
@@ -14,2 +14,2 @@
-{original_content}
+{remediated_content}
"""

        return {
            "branch_name": "aiops/fix-vmss-sku-saturation-sev1",
            "commit_message": "fix(infra): autonomous auto-remediation for Sev1 VMSS CPU exhaustion",
            "target_file": target_file,
            "original_code": original_content,
            "remediated_code": remediated_content,
            "unified_diff": diff
        }
