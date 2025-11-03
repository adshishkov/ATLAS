import disnake
from disnake.ext import commands
from datetime import datetime
from utils.config_manager import ConfigManager

class SettingsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_manager = ConfigManager()
    
    async def cog_load(self):
        await self.config_manager.setup_database()
    
    @commands.slash_command(name = "settings", description = "Управление настройками сервера")
    @commands.has_guild_permissions(administrator = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def settings(self, interaction: disnake.ApplicationCommandInteraction):
        pass
    
    @settings.sub_command(name = "view", description = "Просмотр текущих настроек")
    @commands.has_guild_permissions(administrator = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def settings_view(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        module: str = commands.Param(
            name = "модуль",
            description = "Модуль для просмотра",
            choices = ["модули", "префикс", "модерация", "уровни", "экономика", "приветствие", "логирование", "starboard", "тикеты", "ключи"]
        )
    ):
        await interaction.response.defer(ephemeral = True)
        
        config = await self.config_manager.get_config(interaction.guild_id)
        modules = config.get("modules", {})
        
        embed = disnake.Embed(
            title = f"⚙️ Настройки Atlas",
            description = "Ниже приведены настройки для выбранного модуля.",
            color = 0x242429,
            timestamp = datetime.now()
        )
        
        if module == "модули":
            is_enabled = modules.get("moderation", False)
            embed.add_field(name = "**Модерация:**", value = "`✅` Включен" if is_enabled else "`❌` Выключен", inline = False)
            is_enabled = modules.get("levels", False)
            embed.add_field(name = "**Уровни:**", value = "`✅` Включен" if is_enabled else "`❌` Выключен", inline = False)
            is_enabled = modules.get("economy", False)
            embed.add_field(name = "**Экономика:**", value = "`✅` Включен" if is_enabled else "`❌` Выключен", inline = False)
            is_enabled = modules.get("welcome", False)
            embed.add_field(name = "**Приветствие:**", value = "`✅` Включен" if is_enabled else "`❌` Выключен", inline = False)
            is_enabled = modules.get("logging", False)
            embed.add_field(name = "**Логирование:**", value = "`✅` Включен" if is_enabled else "`❌` Выключен", inline = False)
            is_enabled = modules.get("starboard", False)
            embed.add_field(name = "**Starboard:**", value = "`✅` Включен" if is_enabled else "`❌` Выключен", inline = False)
            is_enabled = modules.get("tickets", False)
            embed.add_field(name = "**Тикеты:**", value = "`✅` Включен" if is_enabled else "`❌` Выключен", inline = False)

        elif module == "префикс":
            embed.add_field(name = "**Префикс:**", value = config.get("prefix"), inline = False)
            
        elif module == "модерация":
            is_enabled = modules.get("moderation", False)
            moderation_settings = config.get("moderation", {})
            embed.add_field(name = "**Система модерации:**", value = "`✅` Включена" if is_enabled else "`❌` Выключена", inline = False)
            embed.add_field(name = "**Канал логирования:**", value = f"<#{moderation_settings.get('moderation_log_channel')}>" if moderation_settings.get('moderation_log_channel') else "Не установлен", inline = False)
            embed.add_field(name = "**Множитель опыта:**", value = moderation_settings.get('reputation_rate', 1.0), inline = False)
            embed.add_field(name = "**Роль Warn:**", value = f"<@&{moderation_settings.get('role_warn')}>" if moderation_settings.get('role_warn') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль Warn 2:**", value = f"<@&{moderation_settings.get('role_warn_2')}>" if moderation_settings.get('role_warn_2') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль Mute:**", value = f"<@&{moderation_settings.get('role_mute')}>" if moderation_settings.get('role_mute') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль Helper:**", value = f"<@&{moderation_settings.get('role_helper')}>" if moderation_settings.get('role_helper') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль Moderator:**", value = f"<@&{moderation_settings.get('role_moderator')}>" if moderation_settings.get('role_moderator') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль Admin:**", value = f"<@&{moderation_settings.get('role_admin')}>" if moderation_settings.get('role_admin') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль Owner:**", value = f"<@&{moderation_settings.get('role_owner')}>" if moderation_settings.get('role_owner') else "Не установлена", inline = False)
            
        elif module == "уровни":
            is_enabled = modules.get("levels", False)
            level_settings = config.get("levels", {})
            embed.add_field(name = "**Система уровней:**", value = "`✅` Включена" if is_enabled else "`❌` Выключена", inline = False)
            embed.add_field(name = "**Канал логирования:**", value = f"<#{level_settings.get('levels_log_channel')}>" if level_settings.get('levels_log_channel') else "Текущий канал", inline = False)
            embed.add_field(name = "**Уведомления:**", value = "✅ Включены" if level_settings.get('announce_levelup') else "❌ Выключены", inline = False)
            embed.add_field(name = "**Множитель опыта:**", value = level_settings.get('xp_rate', 1.0), inline = False)
            embed.add_field(name = "**Роль 1 уровня:**", value = f"<@&{level_settings.get('level_1_role')}>" if level_settings.get('level_1_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 5 уровня:**", value = f"<@&{level_settings.get('level_5_role')}>" if level_settings.get('level_5_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 10 уровня:**", value = f"<@&{level_settings.get('level_10_role')}>" if level_settings.get('level_10_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 15 уровня:**", value = f"<@&{level_settings.get('level_15_role')}>" if level_settings.get('level_15_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 20 уровня:**", value = f"<@&{level_settings.get('level_20_role')}>" if level_settings.get('level_20_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 25 уровня:**", value = f"<@&{level_settings.get('level_25_role')}>" if level_settings.get('level_25_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 30 уровня:**", value = f"<@&{level_settings.get('level_30_role')}>" if level_settings.get('level_30_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 40 уровня:**", value = f"<@&{level_settings.get('level_40_role')}>" if level_settings.get('level_40_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 50 уровня:**", value = f"<@&{level_settings.get('level_50_role')}>" if level_settings.get('level_50_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 75 уровня:**", value = f"<@&{level_settings.get('level_75_role')}>" if level_settings.get('level_75_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 100 уровня:**", value = f"<@&{level_settings.get('level_100_role')}>" if level_settings.get('level_100_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 125 уровня:**", value = f"<@&{level_settings.get('level_125_role')}>" if level_settings.get('level_125_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 150 уровня:**", value = f"<@&{level_settings.get('level_150_role')}>" if level_settings.get('level_150_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 200 уровня:**", value = f"<@&{level_settings.get('level_200_role')}>" if level_settings.get('level_200_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 250 уровня:**", value = f"<@&{level_settings.get('level_250_role')}>" if level_settings.get('level_250_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 500 уровня:**", value = f"<@&{level_settings.get('level_500_role')}>" if level_settings.get('level_500_role') else "Не установлена", inline = False)
            embed.add_field(name = "**Роль 1000 уровня:**", value = f"<@&{level_settings.get('level_1000_role')}>" if level_settings.get('level_1000_role') else "Не установлена", inline = False)
            
        elif module == "экономика":
            is_enabled = modules.get("economy", False)
            economy_settings = config.get("economy", {})
            embed.add_field(name = "**Система экономики:**", value = "`✅` Включена" if is_enabled else "`❌` Выключена", inline = False)
            embed.add_field(name = "**Название валюты:**", value = economy_settings.get('currency_name') if economy_settings.get('currency_name') else "Не установлено", inline = False)
            embed.add_field(name = "**Награда за сообщение:**", value = economy_settings.get('message_reward') if economy_settings.get('message_reward') else "Не установлено", inline = False)
            embed.add_field(name = "**Ежедневная награда:**", value = f"{economy_settings.get('daily_reward')} {economy_settings.get('currency_name')} * Уровень пользователя" if economy_settings.get('daily_reward') else "Не установлена", inline = False)
            embed.add_field(name = "**Название работы [1]:**", value = economy_settings.get('work_name_1') if economy_settings.get('work_name_1') else "Не установлено", inline = False)
            embed.add_field(name = "**Зарплата работы [1]:**", value = economy_settings.get('work_reward_1') if economy_settings.get('work_reward_1') else "Не установлено", inline = False)
            embed.add_field(name = "**Название работы [2]:**", value = economy_settings.get('work_name_2') if economy_settings.get('work_name_2') else "Не установлено", inline = False)
            embed.add_field(name = "**Зарплата работы [2]:**", value = economy_settings.get('work_reward_2') if economy_settings.get('work_reward_2') else "Не установлено", inline = False)
            embed.add_field(name = "**Название работы [3]:**", value = economy_settings.get('work_name_3') if economy_settings.get('work_name_3') else "Не установлено", inline = False)
            embed.add_field(name = "**Зарплата работы [3]:**", value = economy_settings.get('work_reward_3') if economy_settings.get('work_reward_3') else "Не установлено", inline = False)
            embed.add_field(name = "**Название работы [4]:**", value = economy_settings.get('work_name_4') if economy_settings.get('work_name_4') else "Не установлено", inline = False)
            embed.add_field(name = "**Зарплата работы [4]:**", value = economy_settings.get('work_reward_4') if economy_settings.get('work_reward_4') else "Не установлено", inline = False)
            embed.add_field(name = "**Название работы [5]:**", value = economy_settings.get('work_name_5') if economy_settings.get('work_name_5') else "Не установлено", inline = False)
            embed.add_field(name = "**Зарплата работы [5]:**", value = economy_settings.get('work_reward_5') if economy_settings.get('work_reward_5') else "Не установлено", inline = False)
            embed.add_field(name = "**Название работы [6]:**", value = economy_settings.get('work_name_6') if economy_settings.get('work_name_6') else "Не установлено", inline = False)
            embed.add_field(name = "**Зарплата работы [6]:**", value = economy_settings.get('work_reward_6') if economy_settings.get('work_reward_6') else "Не установлено", inline = False)
            embed.add_field(name = "**Название работы [7]:**", value = economy_settings.get('work_name_7') if economy_settings.get('work_name_7') else "Не установлено", inline = False)
            embed.add_field(name = "**Зарплата работы [7]:**", value = economy_settings.get('work_reward_7') if economy_settings.get('work_reward_7') else "Не установлено", inline = False)
            embed.add_field(name = "**Название работы [8]:**", value = economy_settings.get('work_name_8') if economy_settings.get('work_name_8') else "Не установлено", inline = False)
            embed.add_field(name = "**Зарплата работы [8]:**", value = economy_settings.get('work_reward_8') if economy_settings.get('work_reward_8') else "Не установлено", inline = False)
            embed.add_field(name = "**Название работы [9]:**", value = economy_settings.get('work_name_9') if economy_settings.get('work_name_9') else "Не установлено", inline = False)
            embed.add_field(name = "**Зарплата работы [9]:**", value = economy_settings.get('work_reward_9') if economy_settings.get('work_reward_9') else "Не установлено", inline = False)
            embed.add_field(name = "**Cooldown работы:**", value = economy_settings.get('work_cooldown') if economy_settings.get('work_cooldown') else "Не установлено", inline = False)
            embed.add_field(name = "**Канал работы:**", value = f"<#{economy_settings.get('work_channel')}>" if economy_settings.get('work_channel') else "Не установлено", inline = False)

        elif module == "приветствие":
            is_enabled = modules.get("welcome", False)
            welcome_settings = config.get("welcome", {})
            embed.add_field(name = "**Система приветствия:**", value = "`✅` Включена" if is_enabled else "`❌` Выключена", inline = False)
            embed.add_field(name = "**Канал логирования:**", value = f"<#{welcome_settings.get('welcome_log_channel')}>" if welcome_settings.get('welcome_log_channel') else "Не установлено", inline = False)
            embed.add_field(name = "**Начальная роль:**", value = f"<@&{welcome_settings.get('role_welcome')}>" if welcome_settings.get('role_welcome') else "Не установлена", inline = False)

        elif module == "логирование":
            is_enabled = modules.get("logging", False)
            logging_settings = config.get("logging", {})
            embed.add_field(name = "**Система логирования:**", value = "`✅` Включена" if is_enabled else "`❌` Выключена", inline = False)
            embed.add_field(name = "**Канал логирования:**", value = f"<#{logging_settings.get('log_channel')}>" if logging_settings.get('log_channel') else "Не установлено", inline = False)

        elif module == "starboard":
            is_enabled = modules.get("starboard", False)
            starboard_settings = config.get("starboard", {})
            embed.add_field(name = "**Система starboard:**", value = "`✅` Включена" if is_enabled else "`❌` Выключена", inline = False)
            embed.add_field(name = "**Канал starboard:**", value = f"<#{starboard_settings.get('starboard_channel')}>" if starboard_settings.get('starboard_channel') else "Не установлено", inline = False)
            embed.add_field(name = "**Минимальное количество лайков:**", value = starboard_settings.get('starboard_threshold') if starboard_settings.get('starboard_threshold') else "Не установлено", inline = False)
            embed.add_field(name = "**Emoji starboard:**", value = starboard_settings.get('starboard_emoji') if starboard_settings.get('starboard_emoji') else "Не установлено", inline = False)
        
        elif module == "тикеты":
            is_enabled = modules.get("tickets", False)
            ticket_settings = config.get("tickets", {})
            embed.add_field(name = "**Система тикетов:**", value = "`✅` Включена" if is_enabled else "`❌` Выключена", inline = False)
            embed.add_field(name = "**Категория тикетов:**", value = f"<#{ticket_settings.get('category')}>" if ticket_settings.get('category') else "Не установлена", inline = False)
            embed.add_field(name = "**Канал логирования:**", value = f"<#{ticket_settings.get('tickets_log_channel')}>" if ticket_settings.get('tickets_log_channel') else "Не установлено", inline = False)
            embed.add_field(name = "**Роль тикета:**", value = f"<@&{ticket_settings.get('role_ticket')}>" if ticket_settings.get('role_ticket') else "Не установлена", inline = False)
        
        elif module == "ключи":
            embed.add_field(name = "**Основные:**", value = "`prefix`", inline = False)
            embed.add_field(name = "**Модерация:**", value = "`moderation.moderation_log_channel`, `moderation.reputation_rate`, `moderation.role_warn`, `moderation.role_warn_2`, `moderation.role_mute`, `moderation.role_helper`, `moderation.role_moderator`, `moderation.role_admin`, `moderation.role_owner`", inline = False)
            embed.add_field(name = "**Уровни:**", value = "`levels.levels_log_channel`, `levels.announce_levelup`, `levels.xp_rate`, `levels.level_1_role`, `levels.level_5_role`, `levels.level_10_role`, `levels.level_15_role`, `levels.level_20_role`, `levels.level_25_role`, `levels.level_30_role`, `levels.level_40_role`, `levels.level_50_role`, `levels.level_75_role`, `levels.level_100_role`, `levels.level_125_role`, `levels.level_150_role`, `levels.level_200_role`, `levels.level_250_role`, `levels.level_500_role`, `levels.level_1000_role`", inline = False)
            embed.add_field(name = "**Экономика:**", value = "`economy.currency_name`, `economy.message_reward`, `economy.daily_reward`, `economy.work_name_1`, `economy.work_reward_1`, `economy.work_name_2`, `economy.work_reward_2`, `economy.work_name_3`, `economy.work_reward_3`, `economy.work_name_4`, `economy.work_reward_4`, `economy.work_name_5`, `economy.work_reward_5`, `economy.work_name_6`, `economy.work_reward_6`, `economy.work_name_7`, `economy.work_reward_7`, `economy.work_name_8`, `economy.work_reward_8`, `economy.work_name_9`, `economy.work_reward_9`, `economy.work_cooldown`, `economy.work_channel`", inline = False)
            embed.add_field(name = "**Приветствие:**", value = "`welcome.welcome_log_channel`, `welcome.role_welcome`", inline = False)
            embed.add_field(name = "**Логирование:**", value = "`logging.log_channel`", inline = False)
            embed.add_field(name = "**Starboard:**", value = "`starboard.starboard_channel`, `starboard.starboard_threshold`, `starboard.starboard_emoji`", inline = False)
            embed.add_field(name = "**Тикеты:**", value = "`tickets.category`, `tickets.tickets_log_channel`, `tickets.role_ticket`", inline = False)
        
        embed.set_thumbnail(file = disnake.File("assets/Images/Atlas/Commands/settings.png"))
        embed.set_footer(
            text = f"© {self.bot.user.name}, {datetime.now().year} | Все права защищены.",
            icon_url = self.bot.user.display_avatar.url
        )
        await interaction.edit_original_message(embed = embed)
    

    @settings.sub_command(name = "set", description = "Изменить настройку")
    @commands.has_guild_permissions(administrator = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def settings_set(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        key: str = commands.Param(
            name = "ключ", 
            description = "Введите ключ настройки (Примеры в /settings view > ключи)"
        ),
        value: str = commands.Param(name = "значение", description = "Введите новое значение")
    ):
        await interaction.response.defer(ephemeral = True)
        
        id_keys = [
            # Модерация
            'moderation.role_owner', 'moderation.role_admin', 'moderation.role_moderator', 
            'moderation.role_helper', 'moderation.role_mute', 'moderation.role_warn', 
            'moderation.role_warn_2', 'moderation.moderation_log_channel',
            # Уровни
            'levels.levels_log_channel', 'levels.level_1_role', 'levels.level_5_role',
            'levels.level_10_role', 'levels.level_15_role', 'levels.level_20_role', 
            'levels.level_25_role', 'levels.level_30_role', 'levels.level_40_role', 
            'levels.level_50_role', 'levels.level_75_role', 'levels.level_100_role', 
            'levels.level_125_role', 'levels.level_150_role', 'levels.level_200_role', 
            'levels.level_250_role', 'levels.level_500_role', 'levels.level_1000_role',
            # Экономика
            'economy.work_channel',
            # Приветствие
            'welcome.welcome_log_channel', 'welcome.role_welcome',
            # Логирование
            'logging.log_channel',
            # Starboard
            'starboard.starboard_channel',
            # Тикеты
            'tickets.category', 'tickets.tickets_log_channel', 'tickets.role_ticket'
        ]
        if value.lower() in ['true', 'false']:
            parsed_value = value.lower() == 'true'
        elif value.isdigit():
            if any(id_key in key for id_key in id_keys):
                parsed_value = str(value)
            else:
                parsed_value = int(value)
        elif value.replace('.', '').isdigit():
            parsed_value = float(value)
        else:
            parsed_value = value
        
        try:
            await self.config_manager.update_setting(interaction.guild_id, key, parsed_value)
            
            config = await self.config_manager.get_config(interaction.guild_id)
            current_value = config.get(key)
            
            embed = disnake.Embed(
                title = "⚙️ Настройки Atlas",
                description = f"**{key}** изменён\n\n**Новое значение:** `{current_value}`",
                color = 0x242429,
                timestamp = datetime.now()
            )
            embed.set_thumbnail(file = disnake.File("assets/Images/Atlas/Commands/settings.png"))
            embed.set_footer(
                text = f"© {self.bot.user.name}, {datetime.now().year} | Все права защищены.",
                icon_url = self.bot.user.display_avatar.url
            )
            await interaction.edit_original_message(embed = embed)
            
        except Exception as e:
            print(f"Ошибка при установке настройки {key}: {e}")
            embed = disnake.Embed(
                title = "⚙️ Настройки Atlas",
                description = f"Не удалось обновить настройку `{key}`: {str(e)}",
                color = 0xff0000,
                timestamp = datetime.now()
            )
            embed.set_thumbnail(file = disnake.File("assets/Images/Atlas/Commands/settings.png"))
            embed.set_footer(
                text = f"© {self.bot.user.name}, {datetime.now().year} | Все права защищены.",
                icon_url = self.bot.user.display_avatar.url
            )
            await interaction.edit_original_message(embed = embed)
    
    @settings.sub_command(name = "modules", description = "Включить/выключить модули")
    @commands.has_guild_permissions(administrator = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def settings_modules(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        module: str = commands.Param(
            name = "модуль",
            description = "Модуль для управления",
            choices = ["Модерация", "Уровни", "Экономика", "Приветствия", "Логирование", "Starboard", "Тикеты"]
        ),
        status: bool = commands.Param(name = "статус", description = "Включить или выключить")
    ):
        await interaction.response.defer(ephemeral = True)
        
        module_mapping = {
            "Модерация": "moderation",
            "Уровни": "levels", 
            "Экономика": "economy",
            "Приветствия": "welcome",
            "Логирование": "logging",
            "Starboard": "starboard",
            "Тикеты": "tickets"
        }
        
        module_key = module_mapping.get(module)
        
        await self.config_manager.update_setting(
            interaction.guild_id, 
            f"modules.{module_key}", 
            status
        )
        
        status_text = "`✅` Включен" if status else "`❌` Выключен"
        embed = disnake.Embed(
            title = "⚙️ Настройки Atlas",
            description = f"**Модуль {module}:**\n{status_text}",
            color = 0x242429,
            timestamp = datetime.now()
        )
        embed.set_thumbnail(file = disnake.File("assets/Images/Atlas/Commands/settings.png"))
        embed.set_footer(
            text = f"© {self.bot.user.name}, {datetime.now().year} | Все права защищены.",
            icon_url = self.bot.user.display_avatar.url
        )
        await interaction.edit_original_message(embed = embed)


def setup(bot):
    bot.add_cog(SettingsCommands(bot))