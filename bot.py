from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ApplicationBuilder, InlineQueryHandler, ContextTypes, CommandHandler
from parser import getDefs
from mytoken import BOT_TOKEN
import uuid

# f"<a href=\"https://hy.wiktionary.org/wiki/{query}\">(wiki)</a>"

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    original_query = update.inline_query.query
    query = original_query.lower()

    if not query:
        return

    # print(f"{update.inline_query.from_user.first_name} ({update.inline_query.from_user.username}): {query}")
    defs = getDefs(query)
    if not any(defs.values()):
        defs = getDefs(query.capitalize())
    if not any(defs.values()):
        defs = getDefs(original_query)


    results = []

    n = 0
    for k, v in defs.items():
        for i in v:
            n+=1
            fordesc = i.replace('<i>', '')
            fordesc = fordesc.replace('</i>', '')
            results.append(
                InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title=k,
                    description=str(n) + '. ' + fordesc,
                    input_message_content=InputTextMessageContent(
                        message_text = (
                            f"Բառ՝\n"
                            f"<blockquote><b>{query}</b></blockquote>\n"
                            f"Բացատրություն՝\n"
                            f"<blockquote><u>{k + '\n'}</u><b>{str(n) + '. ' + i}</b></blockquote>"
                        ),
                        parse_mode = "HTML",
                        disable_web_page_preview=True
                    )
                )
            )

    if not results:
        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=query,
                description="Այսպիսի բառ չգտանք :(",
                input_message_content=InputTextMessageContent(
                    message_text=(   
                        f"Բառ՝\n"
                        f"<blockquote><b>{query}</b></blockquote>\n"
                        f"Բացատրություն՝\n"
                        f"<blockquote><b>Այսպիսի բառ չգտանք :(</b></blockquote>"
                    ),
                    parse_mode="HTML",
                    disable_web_page_preview=True
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