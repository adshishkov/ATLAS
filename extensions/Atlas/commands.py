import disnake

from disnake.ext import commands
from datetime import datetime
from typing import Optional
from utils.atlas_version import AtlasVersion


class AtlasCommands(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        self.atlas_version = AtlasVersion()


    #COMMAND UPDATE VERSION BOT
    @commands.slash_command(
        name = "update",
        description = "Обновить версию бота в базе данных"
    )
    @commands.default_member_permissions(administrator = True)
    @commands.has_guild_permissions(administrator = True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def update(
        self,
        interaction: disnake.ApplicationCommandInteraction,
        major: Optional[int] = commands.Param(
            name = "основная",
            description = "Введите основную версию бота."
        ),
        minor: Optional[int] = commands.Param(
            name = "минорная",
            description = "Укажите минорную версию бота."
        ),
        maintenance: Optional[int] = commands.Param(
            name = "патч",
            description = "Укажите версию патча бота."
        )
    ):
        await interaction.response.defer(ephemeral = True)
        if interaction.author.id == 717833963703369740:
            date = disnake.utils.format_dt(datetime.now(), style = "d")
            time = disnake.utils.format_dt(datetime.now(), style = "t")
            relative_time = disnake.utils.format_dt(datetime.now(), style = "R")
            await self.atlas_version.create_table_version()
            await self.atlas_version.add_bot_to_table_version(self.bot.user)
            await self.atlas_version.update_bot_version(self.bot.user, major, minor, maintenance, date, time, relative_time)
            embed = disnake.Embed(
                title = "Обновление версии Atlas",
                description =   "> Обновление версии Atlas успешно завершено!\n\n"
                                f":a: | **Обновил:** {interaction.author.mention}\n"
                                f":green_book: | **Версия**: **{major}.{minor}.{maintenance}**\n"
                                f":date: | **Дата**: {date} \n"
                                f":alarm_clock: | **Время**: {time}\n"
                                f":up: | **Обновлено**: {relative_time}",
                color = 0x00FF7F,
                timestamp = datetime.now()
            )
            embed.set_thumbnail(file = disnake.File("assets/Images/Atlas/Commands/update.png"))
            embed.set_footer(
                    text = f"© {self.bot.user.name}, {datetime.now().year} | Все права защищены.",
                    icon_url = self.bot.user.display_avatar.url)
            message = await interaction.channel.send(embed = embed)
            # Create thread
            try:
                thread = await message.create_thread(
                    name = f"📑 | Список обновлений {major}.{minor}.{maintenance}",
                    auto_archive_duration = 10080  # In the archive in 7 days
                )                  
                await thread.send("Обратите внимание, что в данной ветке действуют такие же правила, как и на обычные каналы!")
            except Exception as e:
                print(f"Ошибка при создании ветки: {e}")
                await interaction.followup.send("Не удалось создать ветку для обновления", ephemeral = True)
            await interaction.edit_original_message("Сообщение успешно отправлено")
        else:
            return await interaction.edit_original_message(content = "**Ошибка:** У вас нет прав на использование этой команды")


def setup(bot):
    bot.add_cog(AtlasCommands(bot))
