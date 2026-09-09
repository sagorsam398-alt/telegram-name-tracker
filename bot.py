import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# প্রতিটি user-এর আগের নাম/username এখানে রাখা হবে
users = {}

async def check_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.from_user:
        return

    user = update.message.from_user
    user_id = user.id

    new_name = " ".join(
        x for x in [user.first_name, user.last_name] if x
    ).strip()

    new_username = (
        f"@{user.username}" if user.username else "No username"
    )

    old = users.get(user_id)

    # প্রথমবার দেখলে শুধু তথ্য সংরক্ষণ করবে
    if old is None:
        users[user_id] = {
            "name": new_name,
            "username": new_username
        }
        return

    old_name = old["name"]
    old_username = old["username"]

    changed = []

    if old_name != new_name:
        changed.append(f"👤 নাম: {old_name} → {new_name}")

    if old_username != new_username:
        changed.append(
            f"🔹 Username: {old_username} → {new_username}"
        )

    if changed:
        await update.message.reply_text(
            "🔔 Profile Changed\n\n" + "\n".join(changed)
        )

    # নতুন তথ্য সংরক্ষণ
    users[user_id] = {
        "name": new_name,
        "username": new_username
    }


def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN পাওয়া যায়নি!")

    app = Application.builder().token(token).build()

    app.add_handler(
        MessageHandler(filters.ALL, check_profile)
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
