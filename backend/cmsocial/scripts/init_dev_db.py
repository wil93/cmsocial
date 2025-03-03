# -*- coding: utf-8 -*-

from cms.db import SessionGen, Task, Contest, Statement, Dataset, Admin
from cms.db.filecacher import FileCacher
from cmsocial.db import SocialContest, SocialTask

dummy_pdf = b"%PDF-1.0\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/Resources<<>>/MediaBox[0 0 9 9]>>endobj\nxref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000052 00000 n\n0000000101 00000 n\ntrailer<</Root 1 0 R/Size 4>>\nstartxref\n174\n%%EOF"


def main():
    with SessionGen() as s:
        admin = Admin(
            name="Admin",
            username="admin",
            authentication="plaintext:admin",
            permission_all=True,
        )
        contest = Contest(name="dev", description="Dev Contest")
        social_contest = SocialContest(
            Contest=contest,
            cookie_domain="olinfo.it",
            analytics="fake-analytics-id",
            forum="https://forum.olinfo.it",
            top_left_name="Dev",
            title="Dev Contest",
        )
        file_cacher = FileCacher()
        task1 = Task(
            name="test1",
            title="Test task 1",
            contest=contest,
        )
        dataset1 = Dataset(
            description="test dataset",
            time_limit=1.5,
            memory_limit=20971520,
            task_type="Batch",
            task_type_parameters="{}",
            score_type="Sum",
            score_type_parameters="{}",
            task=task1,
        )
        task1.active_dataset = dataset1
        statement1 = Statement(
            digest=file_cacher.put_file_content(dummy_pdf), language="en", task=task1
        )
        social_task1 = SocialTask(task=task1)

        s.add_all([admin, contest, social_contest, task1, statement1, social_task1])
        s.commit()
