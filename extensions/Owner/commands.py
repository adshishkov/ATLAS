import disnake

from disnake.ext import commands


class OwnerCommands(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot


    ### CLEARDM
    @commands.command()
    async def cleardm(self, ctx, message_id):
        if ctx.author.id == 717833963703369740:
            channel = ctx.channel
            message = await channel.fetch_message(message_id)
            if message.author == ctx.bot.user:
                await message.delete()
        else:
            return


    ### CLEAR
    @commands.command(name = "clear")
    @commands.default_member_permissions(administrator = True)
    @commands.has_guild_permissions(administrator = True)
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def clear(self, ctx, msg: int, member = "everyone", *, txt = None):
        await ctx.message.delete()
        member_object_list = []
        if member != "everyone":
            member_list = [x.strip() for x in member.split(",")]
            for member in member_list:
                if "@" in member:
                    member = member[3 if "!" in member else 2:-1]
                if member.isdigit():
                    member_object = ctx.guild.get_member(int(member))
                else:
                    member_object = ctx.guild.get_member_named(member)
                if not member_object:
                    return await ctx.send(f"{ctx.author.mention}, указанный пользователь не найден.", delete_after = 3)
                else:
                    member_object_list.append(member_object)
        if msg < 100:
            async for message in ctx.message.channel.history(limit = msg):
                try:
                    if txt:
                        if not txt.lower() in message.content.lower():
                            continue
                    if member_object_list:
                        if not message.author in member_object_list:
                            continue
                    await message.delete()
                except disnake.Forbidden:
                    await ctx.send(f"{ctx.author.mention}, у вас нет прав на использование данной команды.", delete_after = 3)
        else:
            await ctx.send(f"{ctx.author.mention}, нельзя удалять более 100 сообщений.")


def setup(bot):
    bot.add_cog(OwnerCommands(bot))
