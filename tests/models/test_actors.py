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
