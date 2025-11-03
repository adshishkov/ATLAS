from typing import Dict, Any

class GuildConfig:
    def __init__(self, guild_id: int):
        self.guild_id = guild_id
        self._settings = {
            # Основные настройки
            "prefix": "$",
            # Модули (включены/выключены)
            "modules": {
                "moderation": False,
                "levels": False,
                "economy": False,
                "welcome": False,
                "logging": False,
                "starboard": False,
                "tickets": False,
            },
            # Настройки модерации
            "moderation": {
                "moderation_log_channel": None,
                "reputation_rate": 1.0,
                "role_warn": None,
                "role_warn_2": None,
                "role_mute": None,
                "role_helper": None,
                "role_moderator": None,
                "role_admin": None,
                "role_owner": None
            },
            # Настройки уровней
            "levels": {
                "levels_log_channel": None,
                "announce_levelup": True,
                "xp_rate": 1.0,
                "level_1_role": None,
                "level_5_role": None,
                "level_10_role": None,
                "level_15_role": None,
                "level_20_role": None,
                "level_25_role": None,
                "level_30_role": None,
                "level_40_role": None,
                "level_50_role": None,
                "level_75_role": None,
                "level_100_role": None,
                "level_125_role": None,
                "level_150_role": None,
                "level_200_role": None,
                "level_250_role": None,
                "level_500_role": None,
                "level_1000_role": None,
                "blacklisted_channels": []
            },
            # Настройки экономики
            "economy": {
                "currency_name": "$",
                "message_reward": 5,
                "daily_reward": 1000,
                "work_name_1": "Не установлено",
                "work_reward_1": 1000,
                "work_name_2": "Не установлено",
                "work_reward_2": 5000,
                "work_name_3": "Не установлено",
                "work_reward_3": 10000,
                "work_name_4": "Не установлено",
                "work_reward_4": 20000,
                "work_name_5": "Не установлено",
                "work_reward_5": 50000,
                "work_name_6": "Не установлено",
                "work_reward_6": 100000,
                "work_name_7": "Не установлено",
                "work_reward_7": 200000,
                "work_name_8": "Не установлено",
                "work_reward_8": 500000,
                "work_name_9": "Не установлено",
                "work_reward_9": 1000000,
                "work_cooldown": 3600,
                "work_channel": None,
            },
            # Приветствия
            "welcome": {
                "welcome_log_channel": None,
                "role_welcome": None
            },
            # Логирование
            "logging": {
                "log_channel": None
            },
            # Starboard
            "starboard": {
                "starboard_channel": None,
                "starboard_threshold": 3,
                "starboard_emoji": "⭐"
            },
            # Тикеты
            "tickets": {
                "category": None,
                "tickets_log_channel": None,
                "role_ticket": None
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Получить значение настройки по ключу"""
        keys = key.split('.')
        value = self._settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Установить значение настройки"""
        keys = key.split('.')
        settings = self._settings
        
        for k in keys[:-1]:
            if k not in settings:
                settings[k] = {}
            settings = settings[k]
        
        settings[keys[-1]] = value
    
    def to_dict(self) -> Dict[str, Any]:
        """Вернуть все настройки как словарь"""
        return self._settings.copy()
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Загрузить настройки из словаря"""
        self._settings.update(data)