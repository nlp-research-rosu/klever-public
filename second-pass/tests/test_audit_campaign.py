import json
import unittest

from tools import check_audit_campaign


class AuditCampaignTests(unittest.TestCase):
    def test_current_campaign_inputs_match_the_lock(self) -> None:
        lock = json.loads(check_audit_campaign.CAMPAIGN_LOCK.read_text())

        checked = check_audit_campaign.check(lock["audit_image_id"])

        self.assertEqual(checked, lock)

    def test_different_resolved_image_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            check_audit_campaign.CampaignError, "audit_image_id"
        ):
            check_audit_campaign.check("sha256:different")


if __name__ == "__main__":
    unittest.main()
