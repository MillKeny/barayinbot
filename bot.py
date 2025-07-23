from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ApplicationBuilder, InlineQueryHandler, ContextTypes, CommandHandler
from parser import getDefs
from token import BOT_TOKEN
import uuid

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.lower()

    if not query:
        return

    print(f"{update.inline_query.from_user.first_name} ({update.inline_query.from_user.username}): {query}")
    defs = getDefs(query)
    if not any(defs.values()):
        defs = getDefs(query.capitalize())


    results = []

    n = 0
    for k, v in defs.items():
        for i in v:
            n+=1
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=k,
                    description=str(n) + '. ' + i,
                    input_message_content=InputTextMessageContent(
                        message_text = f"<b>Բառ՝</b><blockquote>{query}</blockquote>\n<b>Բացատրություն՝</b><blockquote><b>{k + '\n'}</b>{str(n) + '. ' + i}</blockquote>",
                        parse_mode = "HTML"
                    )
                )
            )

    if not results:
        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=query,
                description="Այսպիսի բառ գոյություն չունի :(",
                input_message_content=InputTextMessageContent(
                    message_text=f"<b>Բառ՝</b><blockquote>{query}</blockquote>\n<b>Բացատրություն՝</b><blockquote>Այսպիսի բառ գոյություն չունի :(</blockquote>",
                    parse_mode="HTML"
                )
            )
        )

    await update.inline_query.answer(results[:15], cache_time=0)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
Հայերեն բառարան, որը աշխատում է ցանկացած Տելեգրամյան չատում (inline)!

Ուղղակի գրիր որտեղ ուզում ես՝ 
@barayinbot [քո բառը]

(by @millkeny)
                                    """)
    print(f"\n{update.message.from_user.first_name} (@{update.message.from_user.username}): /start\n")

app = ApplicationBuilder().token(BOT_TOKEN).build()
print("Bot is working!\n")
app.add_handler(CommandHandler("start", start))
app.add_handler(InlineQueryHandler(inline_query_handler))
app.run_polling()