from discord.ext import commands
import yfinance as yf

class Stocks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="stock", help="Fetches the stock price for a given ticker e.g. '!stock AAPL 1y'.")
    async def stock(self, ctx, ticker: str, period: str = "5d"):
       
        if not period in ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]:
            await ctx.send(f"Invalid period: {period}. Please use one of the following: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max.")
            return
        
        if period == "5d":
            await ctx.send("Note: 5d is the default period if none is specified.\n" \
            "You can specify other periods like '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd' and 'max' to get more historical data.")
        try:
            await ctx.send(f"Fetching stock data for {ticker.upper()} over period: {period}...")
            stock = yf.Ticker(ticker.upper())
            stock_info = stock.info
            current_price = stock_info.get("currentPrice")
            hist = stock.history(period=period) 
        
            if current_price is not None and not hist.empty:
                await ctx.send(f"The current price of {ticker} is ${current_price:.2f}")

                latest = hist.iloc[-1]
                oldest = hist.iloc[0]
                change = ((latest['Close'] - oldest['Close']) / oldest['Close']) * 100
                summary = f"📊 **{period.upper()} Summary:**\n"
                summary += f"```\n"
                summary += f"Open:   ${oldest['Open']:.2f}\n"
                summary += f"Close:  ${latest['Close']:.2f}\n"
                summary += f"High:   ${hist['High'].max():.2f}\n"
                summary += f"Low:    ${hist['Low'].min():.2f}\n"
                summary += f"Change: {change:+.2f}%\n"
                summary += f"```"
                
                await ctx.send(summary)


            else:
                await ctx.send(f"Could not retrieve price for ticker symbol: {ticker}")
                
        
        except Exception as e:
            await ctx.send(f"An error occurred while fetching the stock data: {e}")


async def setup(bot):
    await bot.add_cog(Stocks(bot))