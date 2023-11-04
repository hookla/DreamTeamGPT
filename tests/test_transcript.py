from unittest import TestCase

from dream_team_gpt.meeting import Transcript


class TestTranscript(TestCase):
    def setUp(self):
        self.idea = "Best selling toy for kids"
        self.transcript = Transcript(self.idea)

    def test_can_be_used_as_string(self):
        self.assertIsInstance(self.transcript, str)
        raised = False
        try:
            assert str(self.transcript).startswith(
                f"We are here to discuss the following idea:\n{self.idea}"
            )
            assert self.idea in str(self.transcript)
        except AttributeError:
            raised = True
        self.assertFalse(raised, "Exception raised")

    def test_opinions_can_be_added(self):
        assert not self.transcript.opinions

        self.transcript += "Must be safe to use"
        self.transcript.add_opinion("Should be affordable")

        self.assertEquals(
            self.transcript.opinions, ["Must be safe to use", "Should be affordable"]
        )
