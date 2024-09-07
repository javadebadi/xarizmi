import pytest

from xarizmi.models.actors import Actor
from xarizmi.models.actors import ExchangeActor
from xarizmi.models.actors import InvestorActor
from xarizmi.models.actors import TraderActor


class TestActor:

    def test(self) -> None:
        actor = Actor(asset=1e10)
        assert isinstance(actor, Actor)

    def test_add_funds(self) -> None:
        actor = Actor(asset=1e10)
        actor.add_funds(1e10)
        assert actor.asset == 2e10

    def test_withdraw_funds(self) -> None:
        actor = Actor(asset=1e10)
        actor.withdraw_funds(1e10)
        assert actor.asset == 0

    def test__check_funds_is_non_negative(self) -> None:
        # Given an actor
        actor = Actor(asset=1e10)
        # When we want to withdraw a negative funds
        # Then I should see ValueError raised
        with pytest.raises(ValueError) as exc_info:
            actor.withdraw_funds(funds=-1e10)
            assert (
                str(exc_info.value)
                == "The given funds '-1e10' is not non-negative"
            )


class TestExchangeActor:

    def test(self) -> None:
        actor = ExchangeActor(asset=1e10)
        assert isinstance(actor, Actor)
        assert isinstance(actor, ExchangeActor)


class TestTraderActor:

    def test(self) -> None:
        actor = TraderActor(asset=1e6)
        assert isinstance(actor, Actor)
        assert isinstance(actor, TraderActor)


class TestInvestorActor:

    def test(self) -> None:
        actor = InvestorActor(asset=1e6)
        assert isinstance(actor, Actor)
        assert isinstance(actor, InvestorActor)
