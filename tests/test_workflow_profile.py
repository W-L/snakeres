from pathlib import Path
import filecmp

from snakeres import workflow_profile



def test_write_profile(standard_rules_processed, output_profile):
    workflow_profile.write_profile(standard_rules_processed, Path("profile.yaml"))
    assert filecmp.cmp('profile.yaml', output_profile, shallow=False)




