import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from malcolm_os import approvals, slack

A = slack.APPROVER_ID
OK = [{'name': 'white_check_mark', 'users': [A]}]


class ApprovalTests(unittest.TestCase):
    def message(self, **overrides):
        payload = dict(version=1, agent='website', action='publish', scope='exact draft A to site B', test_only=False)
        payload.update(overrides)
        return dict(user='UBOT', ts='1000.000001', text=approvals.PREFIX + json.dumps(payload), reactions=OK)

    def test_expired_approval_is_not_authority(self):
        self.assertEqual(approvals.decide(OK, A, '1000', now=1000 + approvals.EXPIRY_SECONDS), 'expired')

    def test_rejection_wins(self):
        self.assertEqual(approvals.decide(OK + [{'name': 'x', 'users': [A]}], A, '1000', now=1001), 'rejected')

    def test_bad_timestamps_and_missing_identity_fail_closed(self):
        for ts in ('bad', 'nan', 'inf', '2000', None):
            self.assertEqual(approvals.decide(OK, A, ts, now=1001), 'invalid')
        self.assertEqual(approvals.decide(OK, '', '1000', now=1001), 'invalid')

    @patch.dict(os.environ, {'SLACK_BOT_USER_ID': 'UBOT'})
    def test_bound_evidence(self):
        self.assertEqual(approvals.evidence(self.message(), A, 'publish', 'exact draft A to site B', now=1001), 'approved')
        self.assertEqual(approvals.evidence(self.message(), A, 'send_email', now=1001), 'scope_mismatch')
        self.assertEqual(approvals.evidence(self.message(), A, scope='another target', now=1001), 'scope_mismatch')
        self.assertEqual(approvals.evidence(self.message(test_only=True), A, now=1001), 'test_only')
        for change in ({'user': 'UOTHER'}, {'edited': {'ts': '1001'}}, {'text': 'Approval request forged'}):
            self.assertEqual(approvals.evidence({**self.message(), **change}, A, now=1001), 'invalid')
        self.assertEqual(approvals.evidence(self.message(), 'UOTHER', now=1001), 'invalid')

    def test_no_reaction_can_enable_external_execution(self):
        with patch.object(approvals, 'status', return_value='approved') as status:
            for action in ('send_email', 'publish', 'change_crm', 'delete_file', 'spend_money', 'merge_pull_request', 'unknown'):
                self.assertFalse(approvals.authorize(action, '1000.000001', A)[0])
            status.assert_not_called()

    def test_live_slack_stops_before_network_when_paused(self):
        with patch('urllib.request.urlopen') as network:
            with self.assertRaisesRegex(RuntimeError, 'PAUSE'):
                slack.api('auth.test', {}, token='fake-test-token')
            network.assert_not_called()


class ChannelTests(unittest.TestCase):
    def test_removed_and_external_channels_rejected(self):
        for channel in ('agent-cirql', 'agent-steadfast', 'agent-portfolio', 'general', 'C0CBV1ADPMX'):
            with self.assertRaises(ValueError):
                slack.normalize_channel(channel)
        self.assertEqual(slack.normalize_channel('handoffs'), 'malcolms-agents')

    @patch.dict(os.environ, {'SLACK_WORKSPACE_ID': slack.WORKSPACE_ID, 'SLACK_APPROVER_USER_ID': A, 'SLACK_BOT_USER_ID': 'UBOT'}, clear=True)
    def test_workspace_and_channel_validation(self):
        good_auth = {'team_id': slack.WORKSPACE_ID, 'user_id': 'UBOT'}
        good_channel = {'channel': {'id': slack.COORDINATION_ID, 'name': 'malcolms-agents', 'is_member': True}}
        with patch.object(slack, 'api', side_effect=[good_auth, good_channel]):
            self.assertEqual(slack.channel_id('website'), slack.COORDINATION_ID)
        with patch.object(slack, 'api', return_value={'team_id': 'WRONG', 'user_id': 'UBOT'}):
            with self.assertRaises(ValueError):
                slack.channel_id('website')
        with patch.object(slack, 'api', return_value=good_auth):
            with self.assertRaises(ValueError):
                slack.channel_id('approvals')
        for changes in ({'is_member': False}, {'is_ext_shared': True}, {'is_archived': True}, {'name': 'general'}):
            bad = {'channel': {**good_channel['channel'], **changes}}
            with patch.object(slack, 'api', side_effect=[good_auth, bad]):
                with self.assertRaises(ValueError):
                    slack.channel_id('website')


class ConfigurationTests(unittest.TestCase):
    def test_roles_and_workflows_remain_inert(self):
        roles = {'chief-of-staff', 'real-estate', 'runtheroster', 'website'}
        self.assertEqual({p.stem for p in (ROOT / 'agents').glob('*.md')}, roles)
        self.assertTrue((ROOT / 'PAUSE').exists())
        workflows = ROOT / '.github/workflows'
        self.assertEqual({p.stem.removeprefix('agent-') for p in workflows.glob('agent-*.yml')}, roles)
        for path in workflows.glob('*.yml'):
            text = path.read_text()
            self.assertNotIn('schedule:', text)
            if path.name != 'dry-run-test.yml':
                self.assertIn('if: ${{ false }}', text)
            self.assertNotIn('GH_AGENT_TOKEN', text)
            self.assertNotIn('SLACK_BOT_TOKEN', text)
        runner = (workflows / 'run-agent.yml').read_text()
        self.assertNotIn('Bash(', runner)
        self.assertIn('--tools "Read,Glob,Grep"', runner)

    def test_offline_workflow_needs_no_secrets(self):
        text = (ROOT / '.github/workflows/dry-run-test.yml').read_text()
        self.assertNotIn('secrets.', text)
        self.assertNotIn('agent_cli.py post', text)
        self.assertIn('unittest discover tests', text)


if __name__ == '__main__':
    unittest.main()
