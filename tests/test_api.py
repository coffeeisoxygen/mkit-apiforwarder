import schemathesis

schema = schemathesis.openapi.from_url("http://127.0.0.1:8000/openapi.json")
# To show the token in the cURL snippet
schema.config.output.sanitization.update(enabled=False)


@schema.parametrize()
def test_api(case):
    case.call_and_validate(headers={"Authorization": "Bearer secret-token"})
