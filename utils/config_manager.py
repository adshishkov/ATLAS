import aiosqlite
import json
from typing import Any
from models.guild_config import GuildConfig

class ConfigManager:
    """Менеджер для работы с настройками серверов в БД"""
    def __init__(self, db_path: str = "databases/config.db"):
        self.db_path = db_path
    
    async def setup_database(self):
        """Создание таблицы для настроек"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS guild_configs (
                    guild_id INTEGER PRIMARY KEY,
                    settings TEXT NOT NULL DEFAULT '{}',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.commit()
    
    async def get_config(self, guild_id: int) -> GuildConfig:
        """Получить конфиг сервера с автоматическим обновлением структуры"""
        config = GuildConfig(guild_id)
        is_new = False
        
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT settings FROM guild_configs WHERE guild_id = ?",
                (guild_id,)
            )
            result = await cursor.fetchone()
            
            if result:
                settings_data = json.loads(result[0])
                config.from_dict(settings_data)
                
                # Обновляем структуру до актуальной версии
                updated = await self._update_config_structure(config)
                if updated:
                    await self._save_config_internal(db, config)
            else:
                # Создаем запись для нового сервера
                is_new = True
        
        # Сохраняем новый конфиг (если он новый)
        if is_new:
            await self.save_config(config)
        
        return config
    
    async def _update_config_structure(self, config: GuildConfig) -> bool:
        """Обновляет структуру настроек до актуальной версии"""
        default_config = GuildConfig(config.guild_id).to_dict()
        current_settings = config.to_dict()
        
        # Рекурсивно обновляем структуру
        updated = self._update_nested_dict(current_settings, default_config)
        
        if updated:
            config.from_dict(current_settings)
            return True
        return False
    
    def _update_nested_dict(self, current: dict, default: dict) -> bool:
        """Рекурсивно обновляет словарь, добавляя отсутствующие ключи"""
        updated = False
        for key, value in default.items():
            if key not in current:
                current[key] = value
                updated = True
            elif isinstance(value, dict) and isinstance(current[key], dict):
                if self._update_nested_dict(current[key], value):
                    updated = True
        return updated
    
    async def _save_config_internal(self, db: aiosqlite.Connection, config: GuildConfig) -> None:
        """Внутренний метод для сохранения конфига (уже в открытом соединении)"""
        settings_json = json.dumps(config.to_dict())
        await db.execute('''
            INSERT OR REPLACE INTO guild_configs (guild_id, settings)
            VALUES (?, ?)
        ''', (config.guild_id, settings_json))
        await db.commit()
    
    async def save_config(self, config: GuildConfig) -> None:
        """Сохранить конфиг сервера"""
        async with aiosqlite.connect(self.db_path) as db:
            await self._save_config_internal(db, config)
    
    async def update_setting(self, guild_id: int, key: str, value: Any) -> None:
        """Обновить конкретную настройку"""
        config = await self.get_config(guild_id)
        config.set(key, value)
        await self.save_config(config)