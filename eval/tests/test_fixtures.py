from eval.harness.fixtures import check_predicates, PredicateError


_DEAL = {
    "status": "Open",
    "contacts": [{"name": "Bob", "role": "Decision Maker"}],
    "amount": 30000,
}


def test_deal_status_predicate_holds():
    ok, reason = check_predicates([{"deal_status": ["Open"]}], _DEAL)
    assert ok is True


def test_deal_status_predicate_drifted():
    deal = dict(_DEAL, status="Closed won")
    ok, reason = check_predicates([{"deal_status": ["Open"]}], deal)
    assert ok is False
    assert "status" in reason.lower()


def test_no_contact_role_holds_when_role_absent():
    ok, _ = check_predicates([{"no_contact_role": "Champion"}], _DEAL)
    assert ok is True


def test_no_contact_role_fails_when_role_present():
    deal = dict(_DEAL, contacts=[{"name": "Al", "role": "Champion"}])
    ok, reason = check_predicates([{"no_contact_role": "Champion"}], deal)
    assert ok is False
    assert "Champion" in reason


def test_unknown_predicate_raises():
    try:
        check_predicates([{"frobnicate": True}], _DEAL)
        assert False
    except PredicateError:
        pass
