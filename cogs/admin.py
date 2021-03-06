import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['g', 'groups'])
    async def group(self, ctx, cmd, *args):
        """Makes new groups (role and channel) for each semester"""
        embed = discord.Embed(color=discord.Colour.orange())
        is_admin = ctx.message.author.guild_permissions.administrator
        # First make sure the author should be allowed to do any of this
        # TODO: Clean up subcommands using proper discord.py implementation
        if is_admin:
            if cmd in ['n', 'new']:
                return await self.new(ctx, *args)
            elif cmd in ['d', 'del', 'delete']:
                return await self.delete(ctx, *args)
            elif cmd in ['c', 'clear']:
                return await self.clear(ctx, *args)
            embed.add_field(name='Command not found!',
                            value='!group new [name] [#] (Make sure [name] includes a "?" if making 2+ groups)\n' +
                                  '!group set [name] (Add yourself to a group)')
            return await ctx.send(embed=embed)
        if cmd in ['s', 'set']:
            return await self.set(ctx, *args)
        # If no command has been run yet...
        embed.add_field(name='Command not found!',
                        value='!group set [name] (Add yourself to a group)')
        return await ctx.send(embed=embed)

    async def new(self, ctx, name, num=None):
        # Wildcard character is '?'
        wildcard = '?'
        # If you have 'saturdays-? {num}', it will check {num} to make that many groups and roles
        # Otherwise it will just make one channel
        embed = discord.Embed(color=discord.Colour.orange())
        if num is None:
            embed.add_field(name='Group successfully created!', value=name)
            await ctx.send(embed)
            return await self.make_group(ctx, name)
        elif wildcard in name:
            category_name = name.replace('-', '').replace(wildcard, '')
            category = await ctx.guild.create_category(category_name)
            # Makes {i} channels and roles, replacing {wildcard} with {i}
            for i in range(int(num)):
                iter_name = name.replace(wildcard, str(i + 1))
                await self.make_group(ctx, iter_name, category)
            embed.add_field(name='Groups successfully created!',
                            value='{first}\n...\n{last}'.format(first=name.replace(wildcard, '1'),
                                                                last=name.replace(wildcard, str(num))))
            return await ctx.send(embed=embed)
        # else
        embed.add_field(name='Group creation failed!',
                        value='Missing wildcard character [{wildcard}]'.format(wildcard=wildcard))
        return await ctx.send(embed=embed)

    async def make_group(self, ctx, name, category=None):
        # Gotta make a role and channel for each
        # Make role
        role = await ctx.guild.create_role(name=name)
        permissions = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        # Make channel with permissions
        await ctx.guild.create_text_channel(name, overwrites=permissions, category=category)
        # Make voice chat with permissions
        await ctx.guild.create_voice_channel(name, overwrites=permissions, category=category)
        return True
        # Use the following if the permissions dict isn't working
        #   channel.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False)
        #   channel.set_permissions(role, read_messages=True, send_messages=True)

    async def set(self, ctx, group):
        embed = discord.Embed(color=discord.Colour.orange())
        for channel in ctx.guild.channels:
            if (group == channel.name and
                    group.lower() not in ['exec', 'president', 'mentor', 'lecture lead', 'jr exec']):
                # It will attempt to give them the role with the same channel name
                embed.add_field(name='Role added!', value=group)
                await ctx.send(embed=embed)
                return await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=group))
        embed.add_field(name='Role could not be added!', value=group)
        return await ctx.send(embed=embed)

    async def delete(self, ctx, *args):
        # TODO: Make "delete" command
        embed = discord.Embed(color=discord.Colour.orange())
        embed.add_field(name='Command is under construction...', value='')
        return await ctx.send(embed=embed)

    async def clear(self, ctx, *args):
        # TODO: Make "clear" command
        embed = discord.Embed(color=discord.Colour.orange())
        embed.add_field(name='Command is under construction...', value='')
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Admin(bot))
