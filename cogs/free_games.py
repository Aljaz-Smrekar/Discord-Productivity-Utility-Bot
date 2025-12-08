import discord
from discord.ext import commands
import requests as req
import requests
import datetime


class Free_Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def fetch_free_games(self):
        url = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=NZ&allowCountries=NZ"
        response = requests.get(url)
        data = response.json()
        # print(data)
        free_games = []
        now = datetime.datetime.utcnow().isoformat()

        for game in data["data"]["Catalog"]["searchStore"]["elements"]:
            promotions = game.get("promotions")
            if not promotions:
                continue

            current = promotions.get("promotionalOffers")
            if not current:
                continue

            offer = current[0]["promotionalOffers"][0]
            start = offer["startDate"]
            end = offer["endDate"]

            if start <= now <= end:
                free_games.append({
                    "title": game["title"],
                    "description": game.get("description", "No description"),
                    "startDate": start,
                    "endDate": end,
                    "image": game["keyImages"][0]["url"] if game.get("keyImages") else None,
                    "url": f"https://store.epicgames.com/en-US/p/{game['productSlug']}"
                })

        return free_games

    @commands.command(name="free_games")
    async def free_games(self, ctx):
        games = self.fetch_free_games()

        if not games:
            await ctx.send("❌ No free games right now.")
            return

        # Send one embed per game
        for g in games:
            embed = discord.Embed(
                title=g["title"],
                description=g["description"][:1500],  # avoid limits
                color=0x00FF00,
            )

            embed.add_field(name="Free Until", value=g["endDate"], inline=False)
            embed.add_field(name="Link", value=g["url"], inline=False)

            if g["image"]:
                embed.set_thumbnail(url=g["image"])

            await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(Free_Games(bot))