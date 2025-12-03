import asyncio
import unittest

from fastapi import HTTPException, status

from api.dependencies.employee_auth import require_employee_code
from api.dependencies.config import conf


class TestEmployeeCode(unittest.TestCase):
    def setUp(self):
        self._old_code = getattr(conf, "employee_code", None)
        conf.employee_code = "kricketot"

    def tearDown(self):
        if self._old_code is None:
            delattr(conf, "employee_code")
        else:
            conf.employee_code = self._old_code

    def test_accepts_correct_code(self):
        try:
            asyncio.run(require_employee_code("kricketot"))
        except HTTPException as exc:
            self.fail(f"require_employee_code raised unexpectedly: {exc}")

    def test_rejects_wrong_code(self):
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(require_employee_code("wrong-code"))

        self.assertEqual(ctx.exception.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_rejects_missing_code(self):
        with self.assertRaises(HTTPException) as ctx:
            asyncio.run(require_employee_code(None))

        self.assertEqual(ctx.exception.status_code, status.HTTP_401_UNAUTHORIZED)


if __name__ == "__main__":
    unittest.main()