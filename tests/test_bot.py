from tokenfinderbot.tokenfinderbot import TokenBot
import pytest
from dotmap import DotMap


@pytest.fixture
def bot() -> TokenBot:
    """Create an instance of TokenBot

    Returns:
        TokenBot: a bot instance
    """
    return TokenBot()


def test_bot_get_settings(bot: TokenBot) -> None:
    """Test get settings

    Args:
        bot (TokenBot): a bot instance
    """
    settings = bot.get_settings()

    assert {'time_filter', 'liq_mc_filter', 'update_interval', 'db_name'} <= set(settings.toDict()) and {'hours', 'minutes'} <= set(
        settings.time_filter.toDict()) and {'mc_liq_ratio', 'min_liq', 'min_mc'} <= set(settings.liq_mc_filter.toDict())


def test_bot_set_settings(bot: TokenBot) -> None:
    """Test set settings

    Args:
        bot (TokenBot): a bot instance
    """
    settings = bot.get_settings()
    settings.time_filter.hours = 10
    bot.set_settings(settings)
    new_settings = bot.get_settings()

    assert (new_settings.time_filter.hours == 10) and (
        new_settings.time_filter.minutes == settings.time_filter.minutes)


def test_bot_fail_set_settings(bot: TokenBot) -> None:
    """Test error when setting object is invalid

    Args:
        bot (TokenBot): a bot instance
    """
    # setting with no hours key
    settings_dict = {
        'time_filter': {
            # 'hours': 12,
            'minutes': 0
        },
        'liq_mc_filter': {
            'mc_liq_ratio': 1.5,
            'min_liq': 1000,
            'min_mc': 100000
        },
        'update_interval': 15,
        'db_name': 'db'
    }
    settings = DotMap(settings_dict)

    with pytest.raises(KeyError, match="Invalid settings dict"):
        bot.set_settings(settings)
