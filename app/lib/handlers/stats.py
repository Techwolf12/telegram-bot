from telegram import Update
from telegram.ext import CallbackContext

from app.lib.handlers.base import BaseHandler, app_context
from app.models import Channel


class StatsCommand(BaseHandler):
    @app_context
    def handler(self, update: Update, context: CallbackContext):
        chat_id = update.message.chat_id

        channel_name = None
        if context.args:
            channel_name = " ".join(context.args)

        if self.can_get_stats(
            context.bot, chat_id, update.message.from_user.id, channel_name
        ):
            pass  # TODO
        else:
            update.message.reply_text("You don't have permission to get stats")

    def can_get_stats(self, bot, chat_id, user_id, channel_name):
        if not channel_name:
            return True

        channel = Channel.query.filter(Channel.name == channel_name).one_or_none()
        if not channel:
            return False

        user_status = bot.get_chat_member(chat_id, user_id).status
        return user_status == "admin"
