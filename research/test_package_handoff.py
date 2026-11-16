from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from research import package_handoff


class HandoffBoundaryTests(unittest.TestCase):
    def test_private_rows_and_weights_never_enter_payload(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for rel in ('public/report.md', 'private/rows.jsonl', 'private/model.joblib',
                        'Private/nested/labels.json', 'public/__pycache__/module.pyc',
                        'FABLE_HANDOFF_old.zip', 'HANDOFF_MANIFEST.json'):
                p = root/rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text('fixture', encoding='utf-8')
            with patch.object(package_handoff, 'ROOT', root):
                self.assertEqual([p.relative_to(root).as_posix() for p in package_handoff.files()],
                                 ['public/report.md'])


if __name__ == '__main__': unittest.main()
