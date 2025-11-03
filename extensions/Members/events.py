import disnake
import random

from disnake.ext import commands
from datetime import datetime
from utils.config_manager import ConfigManager

class MemberEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_manager = ConfigManager()
    
    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        """Обработка входа участника на сервер"""
        try:
            config = await self.config_manager.get_config(member.guild.id)
            
            if not config.get("modules.welcome", False):
                return
            
            welcome_settings = config.get("welcome", {})
            channel_id = welcome_settings.get("welcome_log_channel")
            role_id = welcome_settings.get("role_welcome")
            
            if not channel_id or not role_id:
                return
            
            channel_id_int = int(channel_id)
            channel = member.guild.get_channel(channel_id_int)
            role_id_int = int(role_id)
            role = member.guild.get_role(role_id_int)
            
            if not channel or not role:
                return
            
            
            await member.add_roles(role)
            
            user_date_register = disnake.utils.format_dt(member.created_at, style="d")
            user_date_joined = disnake.utils.format_dt(member.joined_at, style="d")

            GREETING_VARIANTS = [
                "присоединился к нам!",
                "запрыгивает на сервер!",
                "теперь с нами!",
                "проскальзывает на сервер!",
                "примкнул к нам!",
                "пополнил наши ряды!",
                "присоединяется к нашей пати!",
                "уже здесь!"
            ]

            log_embed = disnake.Embed(
                description=(
                    f"{member.mention} {random.choice(GREETING_VARIANTS)}\n"
                    f"> :identification_card: **Пользователь:** {member.name}\n"
                    f"> :id: **ID:** `{member.id}`\n"
                    f"> :calendar_spiral: **Зарегистрирован:** {user_date_register}\n"
                    f"> :calendar_spiral: **Присоединился:** {user_date_joined}\n"
                    f"* Всего пользователей: {len(member.guild.members)}"
                ),
                color=0x009b76,
                timestamp=datetime.now()
            )
            
            avatar = member.display_avatar.url
            if avatar:
                log_embed.set_thumbnail(url=avatar)

            log_embed.set_footer(
                text=f"© {self.bot.user.name}, {datetime.now().year} | Все права защищены.",
                icon_url=self.bot.user.display_avatar.url
            )
            await channel.send(embed=log_embed)
            
        except Exception as e:
            print(f"Ошибка в системе приветствия: {e}")


    @commands.Cog.listener() 
    async def on_member_remove(self, member: disnake.Member):
        """Обработка выхода участника с сервера"""
        try:
            config = await self.config_manager.get_config(member.guild.id)
            
            if not config.get("modules.welcome", False):
                return
            
            welcome_settings = config.get("welcome", {})
            channel_id = welcome_settings.get("welcome_log_channel")
            
            if not channel_id:
                return
            
            channel_id_int = int(channel_id)
            channel = member.guild.get_channel(channel_id_int)
            
            if not channel:
                return
            
            FAREWELL_VARIANTS = [
                "покинул сервер.",
                "спрыгнул с сервера.",
                "теперь не с нами.",
                "ускользнул с сервера.",
                "покинул наши ряды.",
                "покидает наше пати.",
                "похители инопланетяне.",
                "похоже убежал."
            ]
            log_embed = disnake.Embed(
                description = (
                    f"{member.mention} {random.choice(FAREWELL_VARIANTS)}\n"
                    f"> :identification_card: **Пользователь:** {member.name}\n"
                    f"> :id: **ID:** `{member.id}`\n"
                    f"* Всего пользователей: {len(member.guild.members)}"
                ),
                color = 0x9b2d30,
                timestamp = datetime.now()
            )
            
            avatar = member.display_avatar.url
            if avatar:
                log_embed.set_thumbnail(url = avatar)

            log_embed.set_footer(
                    text = f"© {self.bot.user.name}, {datetime.now().year} | Все права защищены.",
                    icon_url = self.bot.user.display_avatar.url
            )
            await channel.send(embed = log_embed)
            
        except Exception as e:
            print(f"Ошибка в welcome системе: {e}")


    @commands.slash_command(name = "test")
    async def test(self, inter:disnake.ApplicationCommandInteraction, member: disnake.Member):
        """Обработка входа участника на сервер"""
        try:
            config = await self.config_manager.get_config(member.guild.id)
            
            if not config.get("modules.welcome", False):
                return
            
            welcome_settings = config.get("welcome", {})
            channel_id = welcome_settings.get("welcome_log_channel")
            role_id = welcome_settings.get("role_welcome")
            
            if not channel_id or not role_id:
                return
            
            channel_id_int = int(channel_id)
            channel = member.guild.get_channel(channel_id_int)
            role_id_int = int(role_id)
            role = member.guild.get_role(role_id_int)
            
            if not channel or not role:
                return
            
            
            await member.add_roles(role)
            
            user_date_register = disnake.utils.format_dt(member.created_at, style="d")
            user_date_joined = disnake.utils.format_dt(member.joined_at, style="d")

            GREETING_VARIANTS = [
                "присоединился к нам!",
                "запрыгивает на сервер!",
                "теперь с нами!",
                "проскальзывает на сервер!",
                "примкнул к нам!",
                "пополнил наши ряды!",
                "присоединяется к нашей пати!",
                "уже здесь!"
            ]

            log_embed = disnake.Embed(
                description=(
                    f"{member.mention} {random.choice(GREETING_VARIANTS)}\n"
                    f"> :identification_card: **Пользователь:** {member.name}\n"
                    f"> :id: **ID:** `{member.id}`\n"
                    f"> :calendar_spiral: **Зарегистрирован:** {user_date_register}\n"
                    f"> :calendar_spiral: **Присоединился:** {user_date_joined}\n"
                    f"* Всего пользователей: {len(member.guild.members)}"
                ),
                color=0x009b76,
                timestamp=datetime.now()
            )
            
            avatar = member.display_avatar.url
            if avatar:
                log_embed.set_thumbnail(url=avatar)

            log_embed.set_footer(
                text=f"© {self.bot.user.name}, {datetime.now().year} | Все права защищены.",
                icon_url=self.bot.user.display_avatar.url
            )
            await channel.send(embed=log_embed)
            await inter.response.send_message("Приветственное сообщение отправлено!")
            
        except Exception as e:
            print(f"Ошибка в системе приветствия: {e}")

def setup(bot):
    bot.add_cog(MemberEvents(bot))